import numpy as np
from tqdm import tqdm
from typing import Union
from .utils import get_mid


def cpa(bytes_num, plaintexts, traces, mask_scheme=None, mask=-1)->np.ndarray:
    '''
    CPA 
    
    `A function to implement correlation power analysis.`
    
    Args:
        `bytes_num`: input the number of the key bytes you want to attack.
        `plaintexts`: input the plaintext array type is numpy arrary.
        `traces`: traces array just like plaintexts.
        `mask_scheme`: please input your mask scheme, TODO: this arg will be used in next version :)
        `mask`: input your mask list, shape = (1, n).
        
    Returns: 
        `ndarry`: return guess key list.
    
    Raises:
        for version 0.x, there does not have any raises, we do not check any inputs just give u a tips.
    Case:
        >>> guess_keys, data = cat.cpa(1, [[1],[2],[3],[4]], [[23], [44], [55], [77]], 'bool', mask=-1)
        
    > It is just a example, you need replace the plaintexts and traces to real data.
    '''
    guess_keys = np.zeros(shape=(bytes_num))
    traces_num = traces.shape[0]
    for byte in range(bytes_num):
        data = []
        for k in tqdm(range(256), desc="[+] byte: " + str(byte)):
            targets = np.zeros(shape=(traces_num))
            for index in range(traces_num):
                targets[index] = get_mid(plaintexts[index][byte], k, mask, mask_scheme)
            data.append(max(pcc(targets, traces)))
        guess_keys[byte] = np.argmax(data)
    return guess_keys

def pcc(targets:np.array, traces:np.array):
    '''
    ### Pearson correlation coeffcuent
    
    return abs value, whether it is positive or negative
    '''
    point_num = traces.shape[1]
    pearson_list = np.zeros(point_num)
    for num in range(point_num):
        pearson_list[num] = pearson(targets, traces[:, num])
    return pearson_list

def pearson(x:np.array, y:np.array):
    x = (x-np.mean(x,axis=0))/np.std(x,axis=0)
    x = x/np.linalg.norm(x,axis=0)
    y = (y-np.mean(y,axis=0))/np.std(y,axis=0)
    y = y/np.linalg.norm(y,axis=0)
    m = np.dot(x.T,y)
    return abs(m)


def rank(predictions, targets, key:int, num_trace:int, interval:int):
    '''
    ### key rank
    `A function to calc right key rank`
    
    Args:
    `predictions`: key prediction array.
    `targets`    : range every keys prediction.
    `key`        : key value(for byte).
    `num_trace`  : traces number for prediction.
    `interval`   : rank interval.
    
    Returns:
        key rank ndarray.
    '''
    rank_time = np.zeros(int(num_trace/interval))
    pred = np.zeros(256)
    idx = np.random.randint(predictions.shape[0], size=num_trace)
    for i, p in enumerate(idx):
        for k in range(predictions.shape[1]): #256
            pred[k] += predictions[p, targets[p, k]]
        
        if i % interval == 0:
            ranked = np.argsort(pred)[::-1]
            rank_time[int(i/interval)] = list(ranked).index(key)
    return rank_time