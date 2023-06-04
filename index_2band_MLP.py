# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 21:43:00 2022

@author: Administrator
"""
import numpy as np
import pandas as pd
from tqdm import tqdm
import numba
from sklearnex import patch_sklearn
patch_sklearn()
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import KFold

model=MLPRegressor(max_iter=1000)
kf = KFold(n_splits=3, shuffle=True, random_state=1)
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
EPS = 1e-32 

def MLP(X,y):    

    X=scaler.fit_transform(X)
    r2=[]
    for train_index, test_index in kf.split(X):
        #print("modeling star:",model_str)
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
def TDVI( r, n):
    num = 1.5 * (n - r)
    denom = (n**2.0 + r + 0.5)**0.5
    return num / (denom + EPS)  
@numba.jit
def NIRv(r, n):
    return compute_normalized_difference_index(n, r) * n  
@numba.jit
def MSI( n, s1):
    return s1 / (n + EPS)
@numba.jit
def MGRVI( g, r):
    return compute_normalized_difference_index(g**2.0, r**2.0)
@numba.jit
def IPVI(r, n):
    return n / (n + r + EPS)
@numba.jit
def EVI2_(n, r):
    num = 2.5 * (n - r)
    denom = n + 2.4 * r + 6
    return num / (denom + EPS)  
@numba.jit
def DVI(r, n):
    return n - r
@numba.jit
def CIG(g, n):
    index = n / (g + EPS)
    index -= 1.0
    return index
@numba.jit
def CSI(n, s2):
    return n / (s2 + EPS)
@numba.jit
def BAIe(r, n):
    index = (0.1 - r)**2.0
    index += (0.06 - n)**2.0
    return 1.0 / (index + EPS)
@numba.jit
def ARI(g, re1):
    index = 1 / (g + EPS)
    index -= 1 / (re1 + EPS)
    return index

@numba.jit
def creat_dict(n=176):
    list_all=[]
    for i in  range(0,n-1,1):
        for j in range(i+1,n,1):
            list_all.append([i,j])
    return list_all


def bandindex_2(X_resampled, y_resampled, list_all, start,end, df, colums):
    list_all=list_all[start:end]
    i_index=0
    for i_ in tqdm(list_all):
        df_row=start+i_index
        i,j=i_
        x_i = X_resampled.T[i]
        x_j = X_resampled.T[j]
    
        func_list = [compute_normalized_difference_index, TDVI, NIRv, MSI, 
                     MGRVI, IPVI, EVI2_, DVI, CIG, CSI, BAIe, ARI]
        
        for fun_idx in range(12):
            df["{} Band1".format(df_row)] = i
            df["{} Band2".format(df_row)] = j
            yield_k(x_i, x_j, y_resampled, func_list, df, fun_idx, df_row, colums,)
        i_index=i_index+1
    

def yield_k(x_i, x_j, y_resampled, func_list, df, idx, l, columns):
    func = func_list[idx]
    x_ = func(x_i, x_j)
    key = f'{l} {columns[idx+2]}'
    df[key] = MLP(x_.reshape(-1, 1),y_resampled)

def err_call_back(err):
    print(f'~ error：{str(err)}')

if __name__ == '__main__':
    from multiprocessing import Manager
    #data_all = pd.read_feather(r"./dataset.feather")
    data_all=pd.read_csv(r"./dataset.csv",index_col=(0))
    X_resampled=data_all.iloc[:,:-1].values
    y_resampled=data_all.iloc[:,-1].values
    
    column=[ 'Band1', 'Band2', 'NDVI', 'TDVI','NIRv','MSI','MGRVI','IPVI2',
            'EVI2','DVI','CIG','CSI','BAIE','ARI']

    df_2 = pd.DataFrame(columns=column)
    manager = Manager()
    res = manager.dict()
    
    list_all=creat_dict(n=176)
    n_processes=32
    lenth=int(len(list_all)/n_processes)
    
    from multiprocessing import Pool

    with Pool(processes=n_processes) as pool:    
        for j in range(n_processes):
            start=j*lenth
            end=(j+1)*lenth
            if j==(n_processes-1):
                end=len(list_all)
            pool.apply_async(bandindex_2,(X_resampled, y_resampled, list_all, start,end, res, column),error_callback=err_call_back)            
        pool.close()
        pool.join()
        #break
    print("*******************************")
    
    for key, value in res.items():
        row, col = key.split()
        row = int(row)
        df_2.loc[row, col] = value

    print(df_2.tail(10))
    df_2.to_csv(r"./2band_MLP_R2_final2.csv", encoding='utf_8_sig')

    

