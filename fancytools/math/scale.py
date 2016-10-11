
def scale(arr, mn=0, mx=1):
    ''' 
    Apply min-max scaling (normalize)
    then scale to (mn,mx) 
    '''
    amn = arr.min()
    amx = arr.max()
    #normalize:
    arr = (arr-amn) / (amx-amn)
    #scale:
    if amn != mn or amx != mx:
        arr *= mx-mn
        arr += mn
    return arr
   
    
    
    
if __name__ == '__main__':
    import numpy as np
    
    #scale this array, so that it fits between 2-3:
    arr = np.linspace(0.5,10,5)
    arr2 =  scale(arr, 2, 3) 
    
    assert np.allclose(arr2, np.linspace(2,3,5))