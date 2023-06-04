# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 21:43:00 2022

@author: Administrator
"""
#from scipy.stats import spearmanr
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
        #print("开始建模:",model_str)
        train_x, train_y=X[train_index],y[train_index]
        test_x, test_y=X[test_index],y[test_index]
        model.fit(train_x, train_y)        
        ans = model.predict(test_x)
        r2.append(r2_score(test_y, ans))        
    r2=np.array(r2)
    return r2.mean()

@numba.jit
def compute_normalized_difference_index(band1, band2):
    return (band1 - band2) / (band1 + band2 + EPS)

@numba.jit
def ARI2( g, re1, n):
    index = 1 / (g + EPS)
    index -= 1 / (re1 + EPS)
    index = index * n
    return index
@numba.jit
def ARVI(b, r, n):
    return compute_normalized_difference_index(n, r - 2.5 * (r - b))
@numba.jit
def BaI( r, n, s1):
    index = r + s1
    index -= n
    return index
@numba.jit
def EBBI(n, s1, t1):
    num = s1 - n
    denom = (10.0 * ((s1 + t1)**0.5))
    return num / (denom + EPS)    
@numba.jit
def EVI(b, r, n):
    num = 2.5 * (n - r)
    denom = n + 6 * r - 7.5 * b + 1
    return num / (denom + EPS)
@numba.jit
def GBNDVI(b, g, n):
    return compute_normalized_difference_index(n, g + b)
@numba.jit
def GLI(b, g, r):
    return compute_normalized_difference_index(2.0 * g, r + b)
@numba.jit
def MBI(n, s1, s2):
    index = compute_normalized_difference_index(s1, s2 + n)
    index += 0.5
    return index
@numba.jit
def PSRI(b, r, re2):
    return (r - b) / (re2 + EPS)
@numba.jit
def SWI(g, n, s1):
    num = g * (n - s1)
    denom = (g + n) * (n + s1)
    return num / (denom + EPS)
@numba.jit
def creat_dict(n=176):
    list_all=[]
    for i in  range(0,n-2,1):
        for j in range(i+1,n-1,1):
            for k in range(j+1,n,1):
                list_all.append([i,j,k])
    return list_all

def bandindex_3(X_resampled, y_resampled, list_all, start,end, df, colums):
    df_tem = pd.DataFrame(columns=colums)
    list_all=list_all[start:end]
    i_index=0
    func_list =[ARI2,ARVI,BaI,EBBI,EVI, GBNDVI, GLI, MBI, PSRI,SWI]
    for i_ in tqdm(list_all):
        df_row=start+i_index
        i,j,k_=i_

        x_i = X_resampled.T[i]
        x_j = X_resampled.T[j]
        x_k = X_resampled.T[k_]                
        
        df_tem.loc[int(df_row), "Band1"] = i
        df_tem.loc[int(df_row), "Band2"] = j
        df_tem.loc[int(df_row), "Band3"] = k_
        
        for fun_idx in range(len(func_list)):
            func = func_list[fun_idx]
            x_ = func(x_i, x_j, x_k)
            df_tem.loc[int(df_row), str(colums[fun_idx+3])]=MLP(x_.reshape(-1, 1),y_resampled)
            
            #yield_k(x_i, x_j, x_k, y_resampled, func_list, df, fun_idx, df_row, colums,)
        i_index=i_index+1
    df[str(start)+"_"+str(end)]=df_tem                    



def yield_k(x_i, x_j,x_k, y_resampled, func_list, df, idx, l, columns):
    func = func_list[idx]
    x_ = func(x_i, x_j, x_k)
    key = str(l)+" "+str(columns[idx+3])
    df[key] = MLP(x_.reshape(-1, 1),y_resampled)
    

def err_call_back(err):
    print(f' error：{str(err)}')

    
if __name__ == '__main__':
    from multiprocessing import Manager
    data_all= pd.read_csv(r"./dataset.csv",index_col=(0))

    X_resampled=data_all.iloc[:,:-1].values
    y_resampled=data_all.iloc[:,-1].values
    column=[ 'Band1', 'Band2', 'Band3','ARI2_R2', 'ARVI_R2', 'BaI_R2', 'EBBI_R2', 'EVI_R2', 'GBNDVI_R2', 'GLI_R2', 'MBI_R2', 'PSRI_R2', 'SWI_R2']
    df_3 = pd.DataFrame(columns=column)
    manager = Manager()
    res = manager.dict()
    
    list_all=creat_dict(n=176)
    n_processes=128
    lenth=int(len(list_all)/n_processes)
    
    
    from multiprocessing import Pool

    with Pool(processes=n_processes) as pool:    
        for j in range(n_processes):
            start=j*lenth
            end=(j+1)*lenth
            if j==(n_processes-1):
                end=len(list_all)
            pool.apply_async(bandindex_3,(X_resampled, y_resampled, list_all, start,end, res, column),error_callback=err_call_back)
            
        pool.close()
        pool.join()
        print("*******************************")
    
    #line=1
    for key, value in res.items():
        df_3=pd.concat([df_3,value])
        print(df_3.tail(3))
    df_3.to_csv(r"./band3_MLP_R2_final.csv", encoding='utf_8_sig')
    #df_3.reset_index(drop=True).to_feather(r"./final_三波段指数_MLP_R2.feather")
    
    
    

    


