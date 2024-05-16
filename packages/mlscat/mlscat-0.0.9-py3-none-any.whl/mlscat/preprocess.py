import numpy as np
from sklearn import preprocessing

'''
This is data preprocess module.
'''

def minmax(x, y, data):
    '''
    ### minmax
    
    `A function scale the data to x, y`
    
    Args:
    `x`: begain.
    `y`: end.
    `data`: scaled data.
    
    Returns:
        data array.
    '''

    scale = preprocessing.MinMaxScaler(feature_range=(x, y))
    scaled_data = scale.fit_transform(data)
    return scaled_data


def convert_bin_label(labels) -> np.ndarray:
    '''
    ### convert_bin_label   

    Args:
    `labels`: normal labels array.

    Returns:
        bin labels array.
        
    Examples:
    >>> convert_bin_label([10,2])
    array[[0. 0. 0. 0. 1. 0. 1. 0.]
          [0. 0. 0. 0. 0. 0. 1. 0.]]
    '''
    result = np.zeros(shape=(len(labels), 8))
    for index, label in enumerate(labels):
        bin_label = bin(int(label))[2:].zfill(8)
        bin_arr_label = [int(x) for x in bin_label]
        result[index] = bin_arr_label
    return result