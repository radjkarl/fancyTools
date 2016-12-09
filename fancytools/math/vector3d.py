import numpy as np
from numpy.linalg import norm



def vectorAngle(vec1,vec2):
    '''
    vector (x,y,z) or vector field of shape (3,x,y)
    '''
    if vec1.ndim == 1:
        assert vec2.ndim == 3
        vec1 = vectorToField(vec1, vec2.shape[:2])

    if vec2.ndim == 1:
        assert vec1.ndim == 3
        vec2 = vectorToField(vec2, vec1.shape[1:])
    a = np.arccos(
                np.einsum('ijk,ijk->jk', vec1,vec2)
                /( norm(vec1,axis=0) * norm(vec2,axis=0) ) )
    #take smaller of both possible angles:
    ab = np.abs(np.pi-a)
    with np.errstate(invalid='ignore'):
        i = a>ab
    a[i] = ab[i]
    return a

def vectorToField(vec, shape):
    s0,s1 = shape
    out = np.empty(shape=(3,s0,s1))
    out[0] = vec[0]
    out[1] = vec[1]
    out[2] = vec[2]
    return out


if __name__ == '__main__':
    print('todo')