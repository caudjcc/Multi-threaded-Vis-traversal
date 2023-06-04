# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 21:43:00 2022

@author: Administrator
"""

import numpy as np
import pandas as pd
from tqdm import tqdm
EPS = 1e-32 
import numba
from sklearnex import patch_sklearn
patch_sklearn()
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

model=MLPRegressor(max_iter=1000)
kf = KFold(n_splits=3, shuffle=True, random_state=1)

def MLP(X,y):
    X=scaler.fit_transform(X)
    r2=[]
    for train_index, test_index in kf.split(X):
        train_x, train_y=X[train_index],y[train_index]
        test_x, test_y=X[test_index],y[test_index]
        model.fit(train_x, train_y)        
        ans = model.predict(test_x)
        r2.append(r2_score(test_y, ans))        
    r2=np.array(r2)
    #print()
    return r2.mean()

@numba.jit
def compute_normalized_difference_index(band1, band2):
    return (band1 - band2) / (band1 + band2 + EPS)

@numba.jit
def BI(b, r, n, s1):
    return compute_normalized_difference_index(s1 + r, n + b)    
@numba.jit
def BLFEI(g, r, s1, s2):
    return compute_normalized_difference_index((g + r + s2) / 3.0, s1)
@numba.jit
def DBI(b, r, n, t1):
    index = (b - t1) / (b + t1 + EPS)
    index -= (n - r) / (n + r + EPS)
    return index
@numba.jit
def _DBSI(g, r, n, s1):
    index = (s1 - g) / (s1 + g + EPS)
    index -= (n - r) / (n + r + EPS)
    return index
@numba.jit
def EMBI(g, n, s1, s2):
    item1 = compute_normalized_difference_index(s1, s2 + n)
    item1 += 0.5
    item2 = compute_normalized_difference_index(g, s1)
    return (item1 - item2 - 0.5) / (item1 + item2 + 1.5 + EPS)
@numba.jit
def FCVI( b, g, r, n):
    return n - ((r + g + b) / 3.0)
@numba.jit
def GARI(b, g, r, n):
    num = n - (g - (b - r))
    denom = n - (g + (b - r))
    return num / (denom + EPS)
@numba.jit
def WRI(g, r, n, s1):
    return (g + r) / (n + s1 + EPS)    

@numba.jit
def creat_dict(n=176):
    list_all=[]
    for i in  range(0,n-3,2):
        for j in range(i+1,n-2,2):
            for k in range(j+1,n-1,2):
                for l in range(k+1,n,2):
                    list_all.append([i,j,k,l])
    return list_all



def bandindex_4(X_resampled, y_resampled, list_all, start,end, df, colums):#158,159
    df_tem = pd.DataFrame(columns=colums)
    func_list =[BLFEI, BI, DBI, _DBSI, EMBI, FCVI, GARI, WRI]
    list_all=list_all[start:end]
    i_index=0
    for i_ in tqdm(list_all):
        df_row=start+i_index

        i,j,k_,l=i_
        x_i = X_resampled.T[i]
        x_j = X_resampled.T[j]
        x_k = X_resampled.T[k_]
        x_l = X_resampled.T[l]
        func_list =[BLFEI, BI, DBI, _DBSI, EMBI, FCVI, GARI, WRI]
        df_tem.loc[int(df_row), "Band1"] = i
        df_tem.loc[int(df_row), "Band2"] = j
        df_tem.loc[int(df_row), "Band3"] = k_
        df_tem.loc[int(df_row), "Band4"] = l
    
        for fun_idx in range(len(func_list)):

            func = func_list[fun_idx]
            x_ = func(x_i, x_j, x_k, x_l)
            df_tem.loc[int(df_row), str(colums[fun_idx+4])]=MLP(x_.reshape(-1, 1),y_resampled)
        i_index=i_index+1                    
    df[str(start)+"_"+str(end)]=df_tem

def err_call_back(err):
    print(f'~ error：{str(err)}')

    
if __name__ == '__main__':

    data_all= pd.read_csv(r"./dataset.csv",index_col=(0))

    X_resampled=data_all.iloc[:,:-1].values
    y_resampled=data_all.iloc[:,-1].values
    column=[ 'Band1', 'Band2', 'Band3', 'Band4','BLFEI_R2', 'BI_R2','DBI_R2', '_DBSI_R2','EMBI_R2', 'FCVI_R2','GARI_R2', 'WRI_R2']
    df_4 = pd.DataFrame(columns=column)
    from multiprocessing import Manager
    manager = Manager()
    res = manager.dict()
    list_all=creat_dict(n=176)
    n_processes=256   
    lenth=int(len(list_all)/n_processes)
    
    from multiprocessing import Pool        
    with Pool(processes=n_processes) as pool:    
        for j in range(n_processes):
            start=j*lenth
            end=(j+1)*lenth
            if j==(n_processes-1):
                end=len(list_all)
            pool.apply_async(bandindex_4,(X_resampled, y_resampled, list_all, start,end, res, column),error_callback=err_call_back)
            
        pool.close()
        pool.join()

    print("*******************************")
        
    for key, value in res.items():
        df_4=pd.concat([df_4,value])        
        print(df_4.tail(3))
    df_4.to_csv(r"./band4_MLP_R2.csv",encoding='utf-8')
    #df_4=pd.DataFrame(df_4,dtype=(float))
    #df_4.reset_index(drop=True).to_feather(r"./20221229_四波段指数_MLP_R2.feather")


