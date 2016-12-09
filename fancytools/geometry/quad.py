'''
various functions on 2d 4-corner polygons (quads)
'''



def scaleToBoxParam(quad, shape):
    '''
    so, you have a [quad] ((x0,y0),,,) inside a box [shape](width,height)
    
    this function gives you center [x,y], and scale factor [x,y]
    you would need to apply to [quad] in order to scale it to the same shape as the box
    
    
    !quad corners needs to be sorted like in example
    '''
    
    #get edge middle points
    x0 = 0.5*(quad[0][0]+quad[1][0])
    x1 = 0.5*(quad[2][0]+quad[3][0])
    
    y0 = 0.5*(quad[0][1]+quad[3][1])
    y1 = 0.5*(quad[1][1]+quad[2][1])
    
    cx = (x0*shape[0]) / (x0-x1+shape[0])
    cy = (y0*shape[1]) / (y0-y1+shape[1])

    fx = abs(cx/(x0-cx))
    fy = abs(cy/(y0-cy))

    return (fx,fy), (cx,cy)
 
 
    
if __name__ == '__main__':
    from fancytools.geometry.polygon import scale
    import pylab as plt
    import numpy as np
    import sys
    
    quad =np.array(((820,3947),(827,1138),(3223,1161), (3195,3942)))
    s = (4096, 4096)
    
    f,c = scaleToBoxParam(quad, s) 
    quad2 = scale(quad, f, c)

    if 'no_window' not in sys.argv:

        box = (0,s[0],s[0],0,0), (0,0,s[1],s[1],0)
        
        quad = np.append(quad, [quad[0]], axis=0)
        quad2 = np.append(quad2, [quad2[0]], axis=0)
        #quad = np.array(quad)
        plt.plot(box[0],box[1], label='bounding box')    
        plt.plot(quad[:,0],quad[:,1], label='given quad')
        plt.plot(quad2[:,0],quad2[:,1], label='scaled quad')
        plt.plot(c[0],c[1], 'o', label='found center')

        plt.legend()
        plt.show()
    