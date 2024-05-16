from pywfn.base import Mol,Atom
import numpy as np
from pywfn.data import Elements
from functools import lru_cache
elements=Elements()
from pywfn.utils import printer
from pywfn.atomprop import lutils,AtomCaler
from pywfn import maths
from typing import Literal
from pywfn.maths import CM2PM

Chrgs=Literal['mulliken','lowdin','hirshfeld']

class Calculator(AtomCaler):
    def __init__(self,mol:"Mol"):
        self.logTip:str=''
        self.mol=mol
        self.chrg:Chrgs='mulliken'
    
    def calculate(self,chrg:Chrgs)->np.ndarray:
        if chrg=='mulliken':
            return self.mulliken()
        if chrg=='lowdin':
            return self.lowdin()
        if chrg=='hirshfeld':
            return self.hirshfeld()
    
    def mulliken(self,num:bool=False,PM:np.ndarray=None):
        """
        计算目录mulliken电荷
        num：是否只保留电子数
        """
        # 计算密度矩阵
        self.logTip='Mulliken电荷分布'
        if PM is None:PM=self.mol.PM
        # 矩阵乘法的迹的加和=矩阵对应元素乘积之和
        PS=PM@self.mol.SM
        EV=np.diagonal(PS)
        atoms=self.mol.atoms
        charges=np.zeros(len(atoms))
        for a,atom in enumerate(atoms):
            a1,a2=atom.obtBorder
            elect=EV[a1:a2].sum()
            if num:
                charges[a]=elect
            else:
                charges[a]=atom.atomic-elect
        return charges
    
    def lowdin(self,num:bool=False,PM:np.ndarray=None):
        """
        计算每个原子的lowdin电荷
        """
        self.logTip='Lowdin电荷分布'
        if PM is None:PM=self.mol.PM
        SM=self.mol.SM
        # 计算矩阵的1/2次方
        v, Q=np.linalg.eig(SM)
        V=np.diag(v)
        V_=V**0.5
        Q_=np.linalg.inv(Q)
        SM_half=Q@(V_@Q_)
        SPS=SM_half@(PM@SM_half)
        eleNums=np.diagonal(SPS)
        charges=np.zeros(len(self.mol.atoms))
        for a,atom in enumerate(self.mol.atoms):
            u,l=atom.obtBorder
            eleNum=eleNums[u:l].sum()
            if num:
                charges[a]=eleNum
            else:
                charges[a]=atom.atomic-eleNum
        return charges
    
    def hirshfeld(self):
        """
        计算原子的Hirshfeld电荷，目前还未成功（分子的电子密度计算不正确）
        """
        from pywfn.spaceProp import wfn
        wfnCaler=wfn.Calculator(self.mol)
        self.mol.bohr=True
        from pywfn.data import sphGrid,radDens
        coords=sphGrid.gridData[:,:3]# 原点为0的坐标
        weight=sphGrid.gridData[:,3]
        npos=len(coords)
        atoms:list[int]=self.mol.atoms.indexs
        chargs=np.zeros(shape=(len(atoms)))
        for a1,atom1 in enumerate(self.mol.atoms): # 计算每一个原子的电荷
            pos=coords+atom1.coord # 该原子周围点的空间坐标
            # molDens=self.mol.get_dens(atoms,obts,coord)*weight # 计算分子的电子密度
            molDens=np.zeros(npos) # 计算分子的电子密度
            proDens=np.zeros(npos)
            for a2,atom2 in enumerate(self.mol.atoms): #计算前置分子密度
                radius=np.linalg.norm(pos-atom2.coord,axis=1) #所有坐标对应的半径
                dens1=radDens.get_radDens(atom2.atomic,radius)*weight # 插值法计算提前存储好的密度
                proDens+=dens1
                if a2==a1:atmDens=dens1
                dens2=wfnCaler.atmDens(atom2.idx,pos-atom2.coord)*weight
                molDens+=dens2
                print(f'{dens1.sum():.4f},{dens2.sum():.4f}')
            ratio=np.divide(atmDens,proDens,out=np.zeros_like(atmDens),where=proDens!=0)
            chargs[a1]=np.sum(ratio*(molDens-proDens))
            atmQ,proQ,molQ=np.sum(atmDens),np.sum(proDens),np.sum(molDens)
            print(f'{atmQ=:.4f},{proQ=:.4f},{molQ=:.4f}')
        chargs=[atom.atomic-val for atom,val in zip(self.mol.atoms,chargs)]
        return chargs
    
    def hirshfeld2(self):
        """第二种计算hirshfeld电荷的方法"""
        from pywfn.data import sphGrid,radDens
        from pywfn.spaceProp import wfn
        coords=sphGrid.gridData[:,:3]# 原点为0的坐标
        weight=sphGrid.gridData[:,3]
        pos=[]
        wei=[]
        for atom in self.mol.atoms:
            pos.append(coords+atom.coord)
            wei.append(weight)
        pos=np.vstack(pos)
        natm=len(self.mol.atoms)
        wei=np.hstack(wei)/natm
        
        wfnCaler=wfn.Calculator(self.mol)
        chars=[]
        molDens=wfnCaler.molDens(pos)
        print(np.min(molDens),np.max(molDens)),print(np.sum(molDens*wei))
        proDens=np.zeros_like(molDens)
        for _,atom in enumerate(self.mol.atoms):
            radius=np.linalg.norm(pos-atom.coord,axis=1)
            proDens+=radDens.get_radDens(atom.atomic,radius)
        print(np.min(proDens),np.max(proDens)),print(np.sum(proDens*wei))
        pass
        for _,atom in enumerate(self.mol.atoms):
            atmDens=wfnCaler.atmDens(atom.idx,pos)
            ratio=np.divide(atmDens,proDens,out=np.zeros_like(atmDens),where=proDens!=0)
            dens=ratio*molDens
            char=sum(dens*wei)
            chars.append(char)
        chars=np.array(chars)
        k=sum(self.mol.atoms.atomics)/sum(chars)
        chars*=k
        chars=[atom.atomic-char for atom,char in zip(self.mol.atoms,chars)]
        return np.array(chars)/20
    
    def dirCharge(self,chrg:Chrgs,atms:list[int],dirs:list[np.ndarray]=None)->np.ndarray:
        """计算不同方向的电荷[n,5](atm,x,y,z,val)"""
        atms_,dirs_=fit_dirs(self.mol,atms,dirs)
        assert len(atms_)==len(dirs_),"长度需要一致"
        dirVal=np.zeros(shape=(len(dirs_),5))
        obts=self.mol.O_obts
        for d in range(len(dirs_)):
            atm=atms_[d]
            dir_=dirs_[d]
            CMp=self.mol.projCM(obts,[atm],[dir_],False,False) # 获取投影后的轨道系数
            PMp=CM2PM(CMp,obts,self.mol.oE)
            if chrg=='mulliken':
                val=self.mulliken(num=True,PM=PMp)[atm-1]
            elif chrg=='lowdin':
                val=self.lowdin(num=True,PM=PMp)[atm-1]
            x,y,z=dir_
            dirVal[d]=[atm,x,y,z,val]

        return dirVal

    def resStr(self)->str:
        """获取结果的打印内容"""
        satoms=lutils.atomIdxs(self.mol.atoms)
        charges=self.calculate()
        return lutils.atomValueStr(self.mol,satoms,charges)
    
    def onShell(self):
        from pywfn.utils import parse_atmList
        printer.info('1. mulliken电荷')
        printer.info('2. lowdin电荷')
        printer.info('3. 方向性电荷')
        while True:
            opt=input('请选择电荷类型:')
            if opt=='':break
            if opt=='1':
                charges=self.mulliken()
                for i,v in enumerate(charges):
                    print(f'{i+1}: {v}')
            if opt=='2':
                charges=self.lowdin()
                for i,v in enumerate(charges):
                    print(f'{i+1}: {v}')
            if opt=='3':
                printer.info('1. Mulliken[*]; 2. lowdin')
                opt=input('请选择方向性电荷类型:')
                if opt not in ['1','2']:return
                if opt=='1':charg='mulliken'
                if opt=='2':charg='lowdin'
                numStr=input('请输入要计算的原子索引：')
                atms=parse_atmList(numStr)
                charges=self.dirCharge(charg,atms)
                for a,x,y,z,v in charges:
                    print(f'{a}: {x},{y},{z}  {v}')
    
def fit_dirs(mol:Mol,atms:list[int],dirs:list[np.ndarray]):
    """
    矫正方向，如果没有指定方向的话，计算每个原子可能的反应方向
    """
    if dirs is None:
        from pywfn.atomprop import direction
        dirCaler=direction.Calculator(mol)
        atms_=[]
        dirs_=[]
        for atm in atms:
            resDirs=dirCaler.reaction(atm)
            dirs_.append(resDirs)
            atms_+=[atm]*len(resDirs)
        dirs_=np.vstack(dirs_)
    else:
        atms_=atms
        dirs_=dirs
    return atms_,dirs_