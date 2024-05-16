import numpy as np
import h5py

'''
This is a load data module.
'''


'''
load ascad,chesctf,DPAv42.et datasets
'''

def load_data(dataset_name, path) -> dict:
    '''
    ### load_data
    
    Args:
    `dataset_name`: dataset name like: ascad, chesctf.
    `path`: dataset's absolute path.

    Returns:
        data dict.

    Example:
    >>> result = load_data('ASCAD', '/home/xxx/ASCAD.h5')
    >>> result.keys()
    dict_keys(['profiling_traces', 'profiling_labels', 'profiling_plaintext', 'profiling_key', 'attack_traces', 'attack_labels', 'attack_plaintext', 'attack_key'])
    '''
    result = {}
    if str.lower(dataset_name) == 'ascad':
        with h5py.File(path, 'r') as hf:
            result['profiling_traces'] = np.array(hf['Profiling_traces/traces'], dtype=np.float32)
            result['profiling_labels'] = np.array(hf['Profiling_traces/labels'], dtype=np.float32)
            result['profiling_plaintext'] = np.array(hf['Profiling_traces/metadata'][:]['plaintext'], dtype=np.int16)
            result['profiling_key'] = np.array(hf['Profiling_traces/metadata'][:]['key'], dtype=np.int16)
            
            # Load attack traces
            result['attack_traces'] = np.array(hf['Attack_traces/traces'], dtype=np.float32)
            result['attack_labels'] = np.array(hf['Attack_traces/labels'], dtype=np.int16)
            result['attack_plaintext'] = np.array(hf['Attack_traces/metadata'][:]['plaintext'], dtype=np.int16)
            result['attack_key'] = np.array(hf['Attack_traces/metadata'][:]['key'], dtype=np.int16)
    return result