# Made by Elouan Créach

import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import matplotlib.path as mpltPath
import numpy as np
import pyvista
import time
import math
import matplotlib
from shapely.geometry import LineString
from scipy.spatial import Delaunay

#from concave_hull import alpha_shape

Tstart = time.time()

#result of dividing by zero:
infinity = 99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999

def get_lines(polydat):
    pnt_list = []
    lin_list = []
    n_lin = int(polydat.n_lines)
    lin = polydat.lines

    for p in polydat.points:
        pnt = [ float(p[0]) , float(p[1]) , float(p[2]) ]
        pnt_list.append(pnt)

    count = 0
    while len(lin_list) < n_lin:
        num = int(lin[0]) #number of points in the line
        count += 1 #del lin[0]
        for i in range(num-1): #-1 because we got rid of the 1st number
            lin_list.append( [ pnt_list[ lin[count] ] , pnt_list[ lin[count+1] ] ] )
            count += 1 #del lin[0]
        count += 1 #del lin[0]

    return lin_list

def normal(p1,p2,p3): #vectorial product
    v1=[ p2[0]-p1[0] , p2[1]-p1[1] , p2[2]-p1[2] ]
    v2=[ p3[0]-p1[0] , p3[1]-p1[1] , p3[2]-p1[2] ]

    a = v1[1]*v2[2]-v1[2]*v2[1]
    b = v1[2]*v2[0]-v1[0]*v2[2]
    c = v1[0]*v2[1]-v1[1]*v2[0]

    return [a,b,c]

def normal2(l1,l2, rounding = None): #vectorial product
    v1=[ l1[1][0]-l1[0][0] , l1[1][1]-l1[0][1] , l1[1][2]-l1[0][2] ]
    v2=[ l2[1][0]-l2[0][0] , l2[1][1]-l2[0][1] , l2[1][2]-l2[0][2] ]

    a = v1[1]*v2[2]-v1[2]*v2[1]
    b = v1[2]*v2[0]-v1[0]*v2[2]
    c = v1[0]*v2[1]-v1[1]*v2[0]

    if rounding == None:
        return [a,b,c]
    else:
        return [ round(a,rounding) , round(b,rounding) , round(c,rounding) ]

def facet(f,p1,p2,p3):#,vn):
    vn = normal(p1,p2,p3)
    f.write(''.join(["          facet normal ",str(vn[0])," ",str(vn[1])," ",str(vn[2]),"\n"]))
    f.write("            outer loop\n")
    f.write(''.join(["              vertex ",str(p1[0]),' ',str(p1[1]),' ',str(p1[2]),'\n']))
    f.write(''.join(["              vertex ",str(p2[0]),' ',str(p2[1]),' ',str(p2[2]),'\n']))
    f.write(''.join(["              vertex ",str(p3[0]),' ',str(p3[1]),' ',str(p3[2]),'\n']))
    f.write("            endloop\n")
    f.write("          endfacet\n")

def write_stl(f,tri,x,y,z,edge_points,z_min,p_centre, **kwargs): #progress_bar is a boolean
    progress_bar = bool(kwargs.get('pb', None))  #https://stackoverflow.com/questions/9539921/how-do-i-create-a-python-function-with-optional-arguments
    extra_triangles = kwargs.get('extra_triangles', None)
    if progress_bar:
        counter = 0
        print('  writing top surface:\n(',' '*98,')\n ',end='')
        t00 = time.time()
    '''
    print('tri: ',tri,
          '\nx:',len(x),x,
          '\ny:',len(y),y,
          '\nz:',len(z),z)
    '''
    for t in tri:
        p1 = [ x[t[0]] , y[t[0]] , z[t[0]] ]
        p2 = [ x[t[1]] , y[t[1]] , z[t[1]] ]
        p3 = [ x[t[2]] , y[t[2]] , z[t[2]] ]
        facet(f,p1,p2,p3)

        if progress_bar:
            counter += 1            
            if counter % int(len(tri)/100) == 0:
                print('=',end='')
    if progress_bar:
        print(' ',round(time.time()-t00,3),'sec')

    #if progress_bar:
        counter = 0
        print('\n  writing sides & bottom:\n(',' '*25,')\n ',end='')
        t00 = time.time()
    
    
    #print('edge_points : ',edge_points)
    if type(edge_points[0]) != list and type(edge_points[0]) != tuple: #edge_points only contains indexes
        edge_points.append(edge_points[0])
        for i in range(len(edge_points)):# 
            if i != (len(edge_points)-1):
                i1 = edge_points[i]
                i2 = edge_points[i+1]

                #side
                p2 = [ x[i1] , y[i1] , z[i1] ]
                p1 = [ x[i2] , y[i2] , z[i2] ]
                p3 = [ x[i1] , y[i1] , z_min ]
                facet(f,p1,p2,p3)


                p1 = [ x[i1] , y[i1] , z_min ]
                p2 = [ x[i2] , y[i2] , z_min ]
                p3 = [ x[i2] , y[i2] , z[i2] ]
                facet(f,p1,p2,p3)

                #bottom
                facet(f,p1,p2,p_centre)

                if progress_bar:          
                    if i % int(len(edge_points)/25) == 0:
                        print('=',end='')
        if progress_bar:
            print(' ',round(time.time()-t00,3),'sec')

    else: #if edge_points contains edge lines: tuple with indexes of 2 points ( i1 , i2 )
        for i in range(len(edge_points)):
            l = edge_points[i]
            i1 = l[0]
            i2 = l[1]

            #side
            p2 = [ x[i1] , y[i1] , z[i1] ]
            p1 = [ x[i2] , y[i2] , z[i2] ]
            p3 = [ x[i1] , y[i1] , z_min ]
            facet(f,p1,p2,p3)


            p1 = [ x[i1] , y[i1] , z_min ]
            p2 = [ x[i2] , y[i2] , z_min ]
            p3 = [ x[i2] , y[i2] , z[i2] ]
            facet(f,p1,p2,p3)

            #bottom
            facet(f,p1,p2,p_centre)


            if progress_bar:          
                if i % int(len(edge_points)/25) == 0:
                    print('=',end='')
        if progress_bar:
            print(' ',round(time.time()-t00,3),'sec')

    if type(extra_triangles ) == list:
        for tr in extra_triangles:
            facet(f, tr[0], tr[1], tr[2] )


def edit_stl(file_name,tri,points):

    f= open(file_name,"r")
    string = f.read()
    f.close()

    lines = string.split('\n')
    lines = lines[:-1]
    string = '\n'.join(lines) #removing the last line of the stla file which is "        endsolid"
    print('len(string):',len(string))
    #f.write("        endsolid")
    f= open(file_name,"w")
    #f.write("solid xyz_to_stl\n")
    f.write(string)

    print('len(tri): ',len(tri))
    print('tri[:10]: ',tri[:10])
    print('len(points): ',len(points))
    print('points: ',points)

    for t in tri:
        p1 = points[ t[0] ] 
        p2 = points[ t[1] ] 
        p3 = points[ t[2] ] 
        
        facet(f,p1,p2,p3)

    f.write("endsolid")
    f.close()           
        


def _2D_line_equation(l):
    if ( l[1][0] - l[0][0] ) != 0:
        a = ( l[1][1] - l[0][1] ) / ( l[1][0] - l[0][0] )
    else:
        a = infinity
    b = l[0][1] - a*l[0][0]
    # y = a*x + b
    return a,b

def point_on_3D_line_x(l,x,y): #https://fr.planetcalc.com/8253/
    x0 = l[0][0]
    y0 = l[0][1]
    z0 = l[0][2]
    x1 = l[1][0]
    y1 = l[1][1]
    z1 = l[1][2]

    if (x1 - x0) != 0:
        t = ( x - x0 ) / (x1 - x0)
        y = y0 + (y1-y0)*t
        z = z0 + (z1-z0)*t
        return [x,y,z]
    
    elif(y1 - y0) != 0:
        t = ( y - y0 ) / (y1 - y0)
        x = x0 + (x1-x0)*t
        z = z0 + (z1-z0)*t
        return [x,y,z]
    
    else:
        return[infinity,infinity,infinity]

def plane_equation(p1,p2,p3):
    n = normal(p1,p2,p3)
    a = n[0]
    b = n[1]
    c = n[2]

    d = -( a*p1[0] + b*p1[1] + c*p1[2] )
    #ax + by + cz + d = 0
    return a,b,c,d


print("heWO PurPLe SheP IS HeRE haHA Oh GOLly")



def intersect(l1 , l2): # l1 is a real 3D line ; l2 is the projection of an infinit flat surface
    #                     l2 can be a point [p1,p1] and it will detect if the point is on l1
    if l2[0] != l2[1]:
        a1 , b1 = _2D_line_equation(l1)
        a2 , b2 = _2D_line_equation(l2)

        if (a1 - a2) != 0:
            x = (b2-b1) / (a1 - a2)
        else:
            x = infinity
        y = a1*x + b1

        x10 = l1[0][0]
        x11 = l1[1][0]
        y10 = l1[0][1]
        y11 = l1[1][1]
        z10 = l1[0][2]
        z11 = l1[1][2]

        x20 = l2[0][0]
        x21 = l2[1][0]
        y20 = l2[0][1]
        y21 = l2[1][1]

        #make sure the intersection is on the segment and not far off into the distance
        if (x <= x10 and x >= x11) or (x >= x10 and x <= x11):
            if (x <= x20 and x >= x21) or (x >= x20 and x <= x21):
                if (y <= y10 and y >= y11) or (y >= y10 and y <= y11):
                    if (y <= y20 and y >= y21) or (y >= y20 and y <= y21):

                        a3 , b3 = _2D_line_equation([[x10,z10],[x11,z11]])
                        z = a3*x + b3

                        return [x,y,z]
        return False

    else: #if we check the intersection of a point and the segment

        a , b = _2D_line_equation(l1)

        x10 = l1[0][0]
        x11 = l1[1][0]
        y10 = l1[0][1]
        y11 = l1[1][1]
        z10 = l1[0][2]
        z11 = l1[1][2]

        x = l2[0][0]
        y = l2[0][1]

        if y == a*x + b:
            #we now need to calculate z
            ##https://fr.planetcalc.com/8253/
            z = (z11-z10)*(x-x10) / (x11-x10) + z10
            return [x,y,z]

        else:
            return False


def simple_resize( xi, xa, yi, ya, points ):  #points = [x_list,y_list,z_list]
    print('xi: ',xi)
    print('xa: ',xa)
    print('yi: ',yi)
    print('ya: ',ya)
    xy_final_pnt = []
    final_pnts = [ [] , [] , [] ]
    for i in range(len(points[0])):
        x = points[0][i]
        y = points[1][i]
        z = points[2][i]
        #print(i,end='|')
        if xi<=x and x<=xa:
            if yi<=y and y<=ya:
                #print('!',end='')
                
                final_pnts[0].append(x) #x
                final_pnts[1].append(y) #y
                final_pnts[2].append(z) #z
                
                xy_final_pnt.append([x,y])
    return final_pnts , xy_final_pnt
    
def resize( xi, xa, yi, ya, points, α): #xi = xmin ; xa = xmax ; list [[x],[y],[z]]
    margin = 50 # how far out of the zone do we take points, in metres?
    pnts = [[],[],[]]
    final_pnts = [[],[],[]]
    xy_point = []
    xy_final_pnt = []

    #defining the lines that form the border of the file
    lxi = [[xi,yi] , [xi,ya]]
    lxa = [[xa,yi] , [xa,ya]]
    lyi = [[xi,yi] , [xa,yi]]
    lya = [[xi,ya] , [xa,ya]]

    border = [ lxi , lxa , lyi , lya ]


    #keeping only the points we might need and removing all the points that we know we will not use in any way shape or form
    for i in range(len(points[0])):
        x = points[0][i]
        if ((x >= xi - margin) and (x <= xi + margin)) or ((x >= xa - margin) and (x <= xa + margin)):
            y = points[1][i]
            if ((y >= yi - margin) and (y <= yi + margin)) or ((y >= ya - margin) and (y <= ya + margin)):
                #print('+',end=' ')
                pnts[0].append(x)
                pnts[1].append(y)
                pnts[2].append(points[2][i])

                xy_point.append([ points[0][i] , points[1][i] ])

        #creation of a list with all the points that will be kept after resizing
        if points[0][i] >= xi:
            if points[0][i] <= xa:
                if points[1][i] >= yi:
                    if points[1][i] <= ya:

                        final_pnts[0].append(points[0][i]) #x
                        
                        final_pnts[1].append(points[1][i]) #y
                        final_pnts[2].append(points[2][i]) #z

                        xy_final_pnt.append([ points[0][i] , points[1][i] ])


    corner_points = [ [xi,yi] , [xi,ya] , [xa,yi] , [xa,ya] ] #creating the points for the corners of the resized file

    num_pnt = len(pnts[0])

    x = np.asarray(pnts[0])
    y = np.asarray(pnts[1])
    z = np.asarray(pnts[2])

    #print('\nx:',x,'\ny:',y)
    segments , tri = alpha_shape( np.array(xy_point) , α , only_outer=False , Pbl=[xi,yi] , Ptr=[xa,ya] )
    #triang = mtri.Triangulation(x, y)
    #tri = triang.triangles

    for t in tri:
        p1 = [ x[t[0]] , y[t[0]] , z[t[0]] ]
        p2 = [ x[t[1]] , y[t[1]] , z[t[1]] ]
        p3 = [ x[t[2]] , y[t[2]] , z[t[2]] ]

        l1 = [p1 , p2]
        l2 = [p2 , p3]
        l3 = [p3 , p1]

        l_tri = [l1 , l2 , l3] # l_tri = list triangle

        for cor in corner_points:
            in_tri = P_in_triangle(p1,p2,p3,cor)
            if in_tri != False:
                final_pnts[0].append(in_tri[0])
                final_pnts[1].append(in_tri[1])
                final_pnts[2].append(in_tri[2])
                #print(in_tri[2])

                xy_final_pnt.append([ in_tri[0] , in_tri[1] ])


        for lb in border:
            for lt in l_tri:
                inte = intersect(lt,lb)
                if inte != False:
                    final_pnts[0].append(inte[0])
                    final_pnts[1].append(inte[1])
                    final_pnts[2].append(inte[2])

                    xy_final_pnt.append([ inte[0] , inte[1] ])

    return final_pnts , xy_final_pnt


def P_in_triangle(p1,p2,p3,p): #https://www.w3resource.com/python-exercises/basic/python-basic-1-exercise-40.php
    '''
    x1 = p1[0]
    x2 = p2[0]
    x3 = p3[0]

    y1 = p1[1]
    y2 = p2[1]
    y3 = p3[1]

    #z1 = p1[2]
    #z2 = p2[2]
    #z3 = p3[2]

    xp = p[0]
    yp = p[1]

    c1 = (x2-x1)*(yp-y1)-(y2-y1)*(xp-x1)
    c2 = (x3-x2)*(yp-y2)-(y3-y2)*(xp-x2)
    c3 = (x1-x3)*(yp-y3)-(y1-y3)*(xp-x3)
    if (c1<0 and c2<0 and c3<0) or (c1>0 and c2>0 and c3>0): #The point is in the triangle
    '''
    
    xp = p[0]
    yp = p[1]
    
    if p_in_poly( p[:2] , [p1[:2] , p2[:2] , p3[:2] ] ):
        #now we need to calculate the z value
        a,b,c,d = plane_equation(p1,p2,p3)
        #print(a,b,c,d,xp,yp)
        zp = - (a*xp + b*yp + d) / c
        #print(zp)
        return [xp,yp,zp]
    else: # we try to see if it is on a line
        list_line = [ [ p1 , p2 ] , [ p1 , p3 ] ]
        for l in list_line:
            point = point_on_3D_line_x(l,xp,yp)
            if point[0] == xp and point[1] == yp: # the point is on the line
                return point
        return False

def p_in_poly(p,poly): #poly is a list of points where 2 adjacent points form a line (I think)
    #https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python
    path = mpltPath.Path(np.array(poly))
    inside = path.contains_points([p])
    return inside[0]


def add_puzzle(file_name,puzzle,xi,yi,xa,ya,z_mini,play,tab_size, base_height=5): #puzzle: 0 for full puzzle
    if puzzle == 0:

        tri,points = stl_puzzle_full([xi,yi],[xa,ya],z_mini,play,tab_size, height=base_height)
        
        edit_stl(file_name,tri,points)
def mm_to_m(d):
    return d/0.2

def m_to_mm(d):
    return d*0.2 #because in the slicer we will inport it at 20% scale

def puzzle_full(Pbl,Ptr,tolerance,tab_size): #Ptl = Point bottom left  ;  Pbr = Point top right ; it is in 2D
    size = tab_size #10#mm   #size = size of the dove tails
    size = mm_to_m(size)#m    #because in the slicer we will inport it at 20% scale   #doesn't activly take into consideration the scale of the model   -    -   -    -   -   -   -  /!\

    
    print('size: ',size)
    points = []
    triangles = []
    t  = tolerance/2
    t2 = tolerance/10

    print('t:',t)

    xi = Pbl[0]
    yi = Pbl[1]
    xa = Ptr[0]
    ya = Ptr[1]
    
    print('xi,yi,xa,ya: ',xi,yi,xa,ya,'    Ptr:',Ptr)

    p_middle = [ (xi+xa)/2 , (yi+ya)/2 ]
    pm = p_middle

    print('p_middle: ',p_middle)

    height = ya - yi
    width = xa - xi

    #n1 = (np.tan(rad(30))*(size)) 
    #n2 = t*(2*np.sin(rad(60))+np.tan(rad(60)))**(-1)

    diagonal_play = t/np.sin(rad(30))
    #diagonal_play = 5
    
    size1 = size-diagonal_play
    size2 = size+diagonal_play

    size11 = size-t
    size22 = size+t
    #n11 = (np.tan(rad(30))*(size-t))
    #n22 = (np.tan(rad(30))*(size+t))
    
    #diagonal_play = t/np.sin(rad(30))
    
    n11 = np.tan(rad(30))*(size11)#-diagonal_play) 
    n22 = np.tan(rad(30))*(size22)#+diagonal_play) 
    print('diagonal_play:\n',diagonal_play,'n11: ',n11,m_to_mm(n11),'\nn22: ',n22,m_to_mm(n22),'\n','   =====================================================================')

    d1 = np.tan(rad(30))*size
    d2 = t/np.cos(rad(30))
    d3 = t * np.tan(rad(30)) + d2
    
    #diagram page 13
    
    #south side:
    points.append([ xi , yi ])                       #0
    points.append([ pm[0] - (size/2 - d2) , yi ])           #1
    points.append([ pm[0] - (size/2+d1-d3) , yi-(size-t) ]) #2
    points.append([ pm[0] + (size/2+d1-d3) , yi-(size-t) ]) #3
    points.append([ pm[0] + (size/2 - d2), yi ])           #4
    points.append([ xa , yi ])                       #5

    #east side
    points.append([ xa , pm[1] - (size/2-d2) ])           #6
    points.append([ xa+(size-t) , pm[1] - (size/2+d1-d3) ]) #7
    points.append([ xa+(size-t) , pm[1] + (size/2+d1-d3) ]) #8
    points.append([ xa , pm[1] + (size/2-d2) ])           #9
    points.append([ xa , ya ])                     #10

    #north side
    points.append([ pm[0] + (size/2+d2) , ya ])          #11
    points.append([ pm[0] + (size/2+d3+d1) , ya-(size+t) ])     #12
    points.append([ pm[0] - (size/2+d3+d1) , ya-(size+t) ]) #    13
    points.append([ pm[0] - (size/2+d2) , ya ]) #         14
    points.append([ xi , ya ]) #                        15

    

    #west side
    points.append([ xi , pm[1] + (size/2+d2) ]) #         16
    points.append([ xi+(size+t) , pm[1] + (size/2+d3+d1) ]) #    17
    points.append([ xi+(size+t) , pm[1] - (size/2+d3+d1) ]) #    18
    points.append([ xi , pm[1] - (size/2+d2) ]) #         19


    

    points.append( p_middle ) #in the middle of the puzzle, not on a side

    l_temp = []
    for i in range(len(points)):
        if i>=0:
            l_temp.append( ''.join( [str(i),': ',str(points[i])] ) )
    print('\npoints:\n', '\n'.join(l_temp),'\n')
    print('deg1:',deg(angle([points[0],points[1]] , [points[1],points[2]])))
    print('deg2:',deg(angle([points[10],points[11]] , [points[11],points[12]])))

    #print('points => ',len(points),points)   
                
    return points #, triangles

def stl_puzzle_full(Pbl,Ptr,z_mini,play,tab_size, height=5):
    #diagram page 13
    tolerance_xy = play #mm_to_m(0.7)
    tolerance_z = 0.8
    points = puzzle_full(Pbl,Ptr,tolerance_xy,tab_size)
    
    points_bottom =[]
    for p in points:
        points_bottom.append([ p[0] , p[1] , z_mini-height ])

    points_top =[]
    for p in points:
        points_top.append([ p[0] , p[1] , z_mini ])
    points_top[2][2] = z_mini-tolerance_z                                   #2
    points_top[3][2] = z_mini-tolerance_z                                   #3
    points_top[7][2] = z_mini-tolerance_z                                   #7
    points_top[8][2] = z_mini-tolerance_z                                   #8
    points_top.append([ points[9][0] , points[9][1] , z_mini-tolerance_z ]) #21
    points_top.append([ points[6][0] , points[6][1] , z_mini-tolerance_z ]) #22
    points_top.append([ points[1][0] , points[1][1] , z_mini-tolerance_z ]) #23
    points_top.append([ points[4][0] , points[4][1] , z_mini-tolerance_z ]) #24

    all_points = points_bottom + points_top

    '''
    triangles_bottom=[ [15,16,17],
                       [13,15,17],
                       [13,14,15],
                       [10,11,12],
                       [13,17,18],
                       [13,18,20],
                       [12,13,20],
                       [6,12,20],
                       [6,9,12],
                       [9,10,12],
                       [6,8,9],
                       [4,20,18],
                       [4,6,20],
                       [6,7,8],
                       [0,18,19],
                       [0,1,18],
                       [1,4,18],
                       [4,5,6],
                       [1,2,3],
                       [1,3,4] ]
    '''
    triangles_bottom=[ [17,16,15],
                       [17,15,13],
                       [15,14,13],
                       [12,11,10],
                       [18,17,13],
                       [20,18,13],
                       [20,13,12],
                       [20,12,6],
                       [12,9,6],
                       [12,10,9],
                       [9,8,6],
                       [18,20,4],
                       [20,6,4],
                       [8,7,6],
                       [19,18,0],
                       [18,1,0],
                       [18,4,1],
                       [6,5,4],
                       [3,2,1],
                       [4,3,1] ]


    triangles_top=[ [15,16,17],
                    [13,15,17],
                    [13,14,15],
                    [10,11,12],
                    [13,17,18],
                    [13,18,20],
                    [12,13,20],
                    [6,12,20],
                    [6,9,12],
                    [9,10,12],
                    [22,8,21], 
                    [4,20,18],
                    [4,6,20],
                    [22,7,8],
                    [0,18,19],
                    [0,1,18],
                    [1,4,18],
                    [4,5,6],
                    [23,2,3],
                    [23,3,24] ]

    #shifting the indexes in triangles_top to be able to use all_points list
    shift = len(points_bottom)
    for t in range(len(triangles_top)):
        for i in range(3):
            triangles_top[t][i] += shift
            
    triangles_south_side = [ [0 , 1 , 0+shift],
                             [0+shift , 1 , 1+shift],
                             [1+shift , 24+shift , 4+shift],
                             [1+shift , 23+shift , 24+shift],
                             [4+shift , 4 , 5],
                             [4+shift , 5 , 5+shift],
                             [1 , 2 , 2+shift],
                             [1 , 2+shift , 23+shift],
                             [2 , 3 , 2+shift],
                             [3 , 3+shift , 2+shift],
                             [4 , 3 , 24+shift],
                             [3 , 3+shift , 24+shift] ]

    triangles_east_side = [ [5 , 6 , 5+shift],
                            [5+shift , 6 , 6+shift],
                            [6+shift , 21+shift , 9+shift],
                            [6+shift , 22+shift , 21+shift],
                            [9+shift , 9 , 10],
                            [9+shift , 10 , 10+shift],
                            [6 , 7 , 7+shift],
                            [6 , 7+shift , 22+shift],
                            [7 , 8 , 7+shift],
                            [8 , 8+shift , 7+shift],
                            [9 , 8 , 21+shift],
                            [8 , 8+shift , 21+shift] ]
    
    triangles_north_side = [ [11 , 10 , 11+shift],
                             [11+shift , 10 , 10+shift],
                             [12 , 11 , 11+shift],
                             [12 , 11+shift , 12+shift],
                             [13 , 12 , 13+shift],
                             [12 , 12+shift , 13+shift],
                             [14 , 13 , 14+shift],
                             [14+shift , 13 , 13+shift],
                             [15 , 14 , 14+shift],
                             [15 , 14+shift , 15+shift] ]

    triangles_west_side = [ [16 , 15 , 16+shift],
                            [16+shift , 15 , 15+shift],
                            [17 , 16 , 16+shift],
                            [17 , 16+shift , 17+shift],
                            [18 , 17 , 18+shift],
                            [17 , 17+shift , 18+shift],
                            [19 , 18 , 19+shift],
                            [19+shift , 18 , 18+shift],
                            [0 , 19 , 19+shift],
                            [0 , 19+shift , 0+shift] ]

    all_triangles = triangles_bottom + triangles_top + triangles_south_side + triangles_east_side + triangles_north_side + triangles_west_side

    '''
    all_triangles_xyz = []
    for t in all_triangles:
        all_triangles_xyz.append([])
        for i in t:
            all_triangles_xyz[-1].append(
    '''
    return all_triangles , all_points
    
    #return triangles_bottom , all_points              
    
def puzzle_narow(Pbl,Ptr,tolerance,side): #Ptl = Point bottom left  ;  Pbr = Point top right ; side = [south,east,north,west] a list of true/false or 1/0 for each sides  ;  it is in 2D
    #diagram page 14
    if side[0] != 0 or side[1] != 0 or side[2] != 0 or side[3] != 0 :
        size = 10#mm
        size *= 5#m

        points = []
        t = tolerance/2

        xi = Pbl[0]
        xa = Ptr[0]
        yi = Pbl[1]
        ya = Ptr[1]

        height = ya - yi
        width = xa - xi

        n1 = - (np.tan(rad(30))*size)
        n2 = t*(2*np.sin(rad(60))+tan(rad(60)))**(-1)

        points.append([ (width-size)/2 , (height-size)/2 ]) # 0
        if side[0] == true:
            points.append([ (width-size)/2 , yi+t ])           #1
            points.append([ (width-size)/2 - n1 , yi+t-size ]) #2
            points.append([ (width+size)/2 + n1 , yi+t-size ]) #3
            points.append([ (width+size)/2 , yi+t ])           #4

        points.append([ (width+size)/2 , (height-size)/2 ]) # 5
        if side[1] == true:
            points.append([ xa-t , (height-size)/2 ])           #6
            points.append([ xa-t+size , (height-size)/2 - n1 ]) #7
            points.append([ xa-t+size , (height+size)/2 + n1 ]) #8
            points.append([ xa-t , (height+size)/2 ])           #9

        points.append([ (width+size)/2 , (height+size)/2 ]) # 10
        if side[2] == true:
            points.append([ (width+size)/2 , ya - (2*size+t) ]) # 11
            points.append([ (width+size)/2 +n1+n2+size/2 , ya - (1.5*size+t) ]) # 12
            points.append([ (width+size)/2 + n2+0.5*size , ya-t ])          #13
            points.append([ (width+size)/2 + n2 , ya-t ])          #14
            points.append([ (width+size)/2 + n1 + n2 , ya-t-size ])     #15
            points.append([ (width-size)/2 - n1 - n2 , ya-t-size ]) #    16
            points.append([ (width-size)/2 - n2 , ya-t ]) #         17
            points.append([ (width-size)/2 - n2-0.5*size , ya-t ])          #18
            points.append([ (width-size)/2 -n1-n2-size/2 , ya - (1.5*size+t) ]) # 19
            points.append([ (width-size)/2 , ya - (2*size+t) ]) # 20

        points.append([ (width-size)/2 , (height+size)/2 ]) # 21
        if side[3] == true:
            points.append([ xa - (1.5*size+t) , (height+size)/2 ]) # 22
            points.append([ xa - (1.5*size+t) , (height+size)/2 +n1+n2+size/2]) # 23
            points.append([ xa - t , (height+size)/2 + n2+size/2 ]) # 24
            points.append([ xa - t , (height+size)/2 + n2 ]) # 25
            points.append([ xa-t-size , (height+size)/2 + n1 + n2 ]) # 26
            points.append([ xa-t-size , (height-size)/2 - n1 - n2 ]) # 27
            points.append([ xa-t , (height-size)/2 - n2 ]) # 28
            points.append([ xa - t , (height-size)/2 - n2-size/2 ]) # 29
            points.append([ xa - (1.5*size+t) , (height-size)/2 -n1-n2-size/2]) # 30
            points.append([ xa - (1.5*size+t) , (height-size)/2 ]) # 31

        return points


def rad(deg):
    return deg*math.pi/180

def deg(rad):
    return rad*180/math.pi

def path_intersection(path1 , path2):  #https://stackoverflow.com/questions/22417842/how-do-i-find-the-intersection-of-two-line-segments
    line1 = LineString(path1)
    line2 = LineString(path2)
    inter = line1.intersection(line2)
    print(inter)

    if inter.geom_type == 'Point':
        return [inter.x , inter.y]
    elif inter.geom_type == 'MultiPoint':
        retur = []
        for p in inter:
            retur.append([inter.x , inter.y])

def normalize_line(line):
    p1 = line[0]
    p2 = line[1]
    if p1[0] < p2[0]:
        return [p1,p2] 
    elif p1[0] > p2[0]:
        return [p2,p1] 
    elif p1[1] < p2[1]:
        return [p1,p2] 
    else:
        return [p2,p1] 


def find_edges_home_made1(tri,x,y,z): #looking at every lines and seeing if it is used more than once, if it is, it cannot be an edge piece
    x_min = min(x)
    x_max = max(x)
    y_min = min(y)
    y_max = max(y)
    lines = []
    edges = []
    counter = 0
    triangles = len(tri) #840059

    #making a list of all the lines
    print('find_edges_home_made1\n  making a list of all the lines:')
    print('(',' '*100,')\n ',end='')
    for t in tri:
        #print(t)
        p1 = [ x[t[0]] , y[t[0]] , z[t[0]] ]
        p2 = [ x[t[1]] , y[t[1]] , z[t[1]] ]
        p3 = [ x[t[2]] , y[t[2]] , z[t[2]] ]

        lines.append( normalize_line([p1,p2]) )
        lines.append( normalize_line([p1,p3]) )
        lines.append( normalize_line([p2,p3]) )
        

        counter += 1

        if counter % int(triangles/100) == 0:
            print('=',end='')
    print('\nnumber of lines:',len(lines))

    counter = 0
    print('\n  looking at every lines and seeing if it is used more than once:')
    print('\n(',' '*200,')\n ',end='')
    #looking at every lines and seeing if it is used more than once, if it is, it cannot be an edge piece
    len_lines = len(lines)
    while len(lines) > 0:
        l = lines[0][:]
        if lines.count(lines[0]) == 1:
            edges.append(l)
        while l in lines:
            lines.remove(l)
        counter += 1

        if counter % int(len_lines/200) == 0:
            print('=',end='')
    return lines

def find_edges_home_made3(tri,x,y,z, **kwargs): #looking at every lines and seeing if it is used more than once, if it is, it cannot be an edge piece
    progress_bar = bool(kwargs.get('pb', None)) #shows progress bar, but slows down the process
    l_max = (kwargs.get('l_max', None))         #force a maximum length, anytriangle with a greater length will be destroyed
    max_ratio = (kwargs.get('max_ratio', None)) # force a max ratio between the lengths of the sides of the triangle (ex: a side cannot be more than 3X the length of an other side)

    x_min = min(x)
    x_max = max(x)
    y_min = min(y)
    y_max = max(y)
    lines = []
    edges = []
    counter = 0
    triangles_removed = 0
    triangles = len(tri) #840059
    new_tri = tri[:]
    continu = True
    
    #making a list of all the lines
    if progress_bar:
        print('find_edges_home_made1\n  making a list of all the lines:')
        print('(',' '*198,')\n ',end='')
    for t in tri:
        #print(t)
        p1 = [ x[t[0]] , y[t[0]] , z[t[0]] ]
        p2 = [ x[t[1]] , y[t[1]] , z[t[1]] ]
        p3 = [ x[t[2]] , y[t[2]] , z[t[2]] ]

        l1 = normalize_line([p1,p2])
        l2 = normalize_line([p1,p3])
        l3 = normalize_line([p2,p3])

        if l_max != None:
            if (dist(p1,p2) > l_max) or (dist(p1,p3) > l_max) or (dist(p2,p3) > l_max):
                continu == False
                new_tri.remove(t)
                triangles_removed += 1
                
        elif max_ratio != None:
            length = sorted([ dist(p1,p2) , dist(p1,p3) , dist(p2,p3) ])
            if (length[1]/length[0] > max_ratio) or (length[2]/length[1] > max_ratio) or (length[2]/length[1] > max_ratio):
                continu == False
                new_tri.remove(t)
                triangles_removed += 1
                  
        #this is the part that takes for ever - - - - - - - -
        if continu:
            if l1 in edges:
                edges.remove(l1)
            else:
                edges.append( l1 )

            if l2 in edges:
                edges.remove(l2)
            else:
                edges.append( l2 )

            if l3 in edges:
                edges.remove(l3)
            else:
                edges.append( l3 )
        #up to here - - - - - - - - - - - - - - - - - - - - -
        
        if progress_bar:
            counter += 1
            if counter % int(triangles/200) == 0:
                print('=',end='')
    print('\nnumber of lines:',len(edges),'\nnumber of triangles removed:',triangles_removed)

    return edges , new_tri #edges is a list of lines with coordinates, and not just a list of indexes


def find_edge_with_stl(tri,x,y,z,temp_file):

    O = [0]*len(x)
    #creation of an stl file containing the surface described by the points in the .xyz file
    f= open(temp_file,"w")
    f.write("solid xyz_to_stl\n")
    write_stl(f,tri,x,y,O)
    f.write("endsolid xyz_to_stl")
    f.close()

    mesh = pyvista.PolyData(temp_file)
    edges = mesh.extract_feature_edges(boundary_edges=True,
                           feature_edges=False,
                           manifold_edges=False) #https://docs.pyvista.org/api/core/_autosummary/pyvista.PolyDataFilters.extract_feature_edges.html#pyvista.PolyDataFilters.extract_feature_edges
    list_line = get_lines(edges)

    '''
    p = pyvista.Plotter()
    p.add_mesh(mesh, color=True)
    p.add_mesh(edges, color="red", line_width=5)
    p.show()
    '''

    return list_line

'''
def find_edges_home_made2(x,y,z,l_max):
    y_max = max(y)
    indexes = np.where(np.array(y) == y_max)[0] #https://btechgeeks.com/python-how-to-find-all-indexes-of-an-item-in-a-list/

    i_max = indexes[0]
    x_max = x[i_max]
    for i in indexes:
        if x[i] > x[i_max]:
            i_max = i

    p1 = [x[i_max],y_max]

    n_pnt = len(x)
    edge_points = [p1]
    for i in range(n_pnt):
        p = [x[i],y[i]]
        if p not in edge_points:
            if dist(p,edge_points[-1]) <= l_max:

'''
def find_edges_Graham_scan(x,y,**kwargs): #https://www.youtube.com/watch?v=VP9ylElm1yY
    l_max = (kwargs.get('l_max', None))  #https://stackoverflow.com/questions/9539921/how-do-i-create-a-python-function-with-optional-arguments
    progress_bar = bool(kwargs.get('pb', None))
    length_restrictions = bool(l_max)
    
    x_min = min(x)
    #we get all the points who have the smallest x coordinate
    indexes = np.where(np.array(x) == x_min)[0] #https://btechgeeks.com/python-how-to-find-all-indexes-of-an-item-in-a-list/

    i_min = indexes[0]
    for i in indexes:
        if y[i] < y[i_min]:
            i_min = i
    p0 = [x[i_min],y[i_min]]

    p00 = [ p0[0]-1 , p0[1] ]
    l00 = [p0 , p00] #axis of reference for angles in the polar coordinate system that will be used

    #creating a list of polar coordinates for all the points and sorting it from lowest angle to the biggest
    liste = []
    for i in range(len(x)):
        if i != i_min:
            p1 = [x[i],y[i]]
            l1 = [p0 , p1]
            point = [ angle2(l00,l1) , i ]# , dist(p0,p1) ]
            liste.append(point)
            
    #ordering the list:
    ordered_list = sorted(liste, key=lambda x:x[0]) #https://stackoverflow.com/questions/10619905/quicksort-a-list-containing-lists-using-python

    #scanning the list and choosing all the edges so that we get a convex polygone (all inside angles < 180°)
    if progress_bar:
        print('\n  Finding edge points:\n(',' '*48,')\n ',end='') #progress bar
        counter = 0
    edge =[ i_min , ordered_list[0][1] ]
    edge_points =[ [0,i_min] , ordered_list[0] ]
##    for j in range(len(ordered_list)):
##        point = ordered_list[i]
    for point in ordered_list:
        
        if point != ordered_list[0]:
            '''
            if point[0] == edge_points[-1][0]:#si les angles sont égaux
                p1 = [ x[edge_points[-1][1]] , y[edge_points[-1][1]] ]
                p2 = [ x[point[1]] , y[point[1]] ]
                d1 = dist(p0,p1)
                d2 = dist(p0,p2)

                if d2 > d1:
                    del edge[-1]
                    del edge_points[-1]
            '''
            continu = False
            while continu == False:  #continue == false means that we do not continue to the rest of the code and instead stay stuck in the while loop
                i0 = edge[-2]
                i1 = edge[-1]
                i3 = point[1]
                
                l1 = [ [x[i0],y[i0]] , [x[i1],y[i1]] ]
                l2 = [ [x[i1],y[i1]] , [x[i3],y[i3]] ]

                ang = angle2(l1,l2)
                
##                if (length_restrictions == True) and (dist([x[i1],y[i1]] , [x[i3],y[i3]]) > l_max):
##                    continu = True
                
                if ang <180:
                    edge.append(i3)
                    edge_points.append(point)
                    continu = True
                elif len(edge) == 2:
                    del edge[-1]
                    edge.append(i3)
                    edge_points.append(point)
                    continu = True
                else:
                    del edge[-1]
                    del edge_points[-1]
                    
        if progress_bar:
            counter += 1            
            if counter % int(len(ordered_list)/50) == 0:
                print('=',end='')
    return edge #indexes of the points forming the edges 
        
        
                 

#def pol(p0,p1): #gives polar coordiates of p1 with p0 being the origine


def angle(l1,l2): #l1 = AO ; l2 = OB
    l1 = l1[::-1] #l1 = OA ; l2 = OB
    v1 = [ l1[1][0]-l1[0][0] , l1[1][1]-l1[0][1] ]
    v2 = [ l2[1][0]-l2[0][0] , l2[1][1]-l2[0][1] ]
    d1 = dist(l1[0],l1[1])
    d2 = dist(l2[0],l2[1])
    ang = np.arccos( scalar_product(v1,v2) / ( d1 * d2 ) )
    return ang

def angle2(l1,l2): #https://math.stackexchange.com/questions/878785/how-to-find-an-angle-in-range0-360-between-2-vectors
                  #l1 = AO ; l2 = OB
    #l1 = l1[::-1] #l1 = OA ; l2 = OB
    v1 = [ l1[1][0]-l1[0][0] , l1[1][1]-l1[0][1] ]
    v2 = [ l2[1][0]-l2[0][0] , l2[1][1]-l2[0][1] ]
    x1 = v1[0]
    x2 = v2[0]
    y1 = v1[1]
    y2 = v2[1]
    
    dot = x1*x2 + y1*y2      # dot product
    det = x1*y2 - y1*x2      # determinant
    ang = math.atan2(det, dot)  # atan2(y, x) or atan2(sin, cos)
    degang = deg(ang)
    if degang < 0:
        degang += 360
    return degang

    
def scalar_product(v1,v2):
    if len(v1) != len(v2):
        return 'no'
    scal = 0
    for i in range(len(v1)):
        scal += v2[i]*v1[i]
    return  scal


def point_above_line(l,p):
    x1 = l[0][0]
    y1 = l[0][1]
    x2 = l[1][0]
    y2 = l[1][1]

    xA = p[0]
    yA = p[1]

    v1 = (x2-x1, y2-y1)   # Vector 1
    v2 = (x2-xA, y2-yA)   # Vector 1
    xp = v1[0]*v2[1] - v1[1]*v2[0]  # Cross product
    if xp > 0: #below
        return -1
    elif xp < 0: #above
        return 1
    else:
        return 0

def dist(p1,p2): #works for points in 2D , 3D , 4D , ...
    num = 0
    for i in range(len(p1)):
        num += (p2[i]-p1[i])**2
    return num**(1/2)

def verticies(indexs,x,y,z):
    points = []
    for i in indexs:
        points.append([ x[i] , y[i] , z[i] ])
    print(points)
    return np.asarray(points)

def lines_np(indexs):
    print(indexs)
    line = [[2,indexs[0],indexs[1]]]
    count = 1
    for i in range(len(indexs)-2):
        i += 2
        line.append([ 2 , line[-1][-1] , indexs[i] ])

    print(line)
        
    return np.hstack([ line ])

def sec_time(sec):
    annee = int(sec // (60*60*24*365.25))
    rest_annee = (sec % (60*60*24*365.25))

    mois = int(rest_annee // (60*60*24*(365.25/12)))
    rest_mois = (rest_annee % (60*60*24*(365.25/12)))

    jour = int(rest_mois // (60*60*24))
    rest_jour = (rest_mois%(60*60*24))

    heur = int(rest_jour // (60*60))
    rest_heur = (rest_jour % (60*60))

    minute = int(rest_heur // 60)
    rest_minute = (rest_heur % 60)
    
    second = round((rest_minute ),3)
  

    

    liste = []
    if annee != 0:
        liste.append(' '.join([str(annee),'year']))
    if mois != 0:
        liste.append(' '.join([str(mois),'month']))
    if jour != 0:
        liste.append(' '.join([str(jour),'day']))
    if heur != 0:
        liste.append(' '.join([str(heure),'hour']))
    if minute != 0:
        liste.append(' '.join([str(minute),'min']))
    if second != 0:
        liste.append(' '.join([str(second),'sec']))
    string = ' , '.join(liste)
    return str(string)

def show_stl(stl_file):
    mesh = pyvista.PolyData(stl_file)
    p = pyvista.Plotter()
    p.add_mesh(mesh, color=True)
    p.show()

def show_stl_edge(stl_file,edge_points):
    verticie = verticies(edge_points,x,y,z)
    line = lines_np(edge_points)

    mesh_edge = pyvista.PolyData(verticie, lines=line)

    #print(mesh_edge.lines)

    
    mesh = pyvista.PolyData(stl_file)
    #print(mesh.vertices)
    
    p = pyvista.Plotter()
    p.add_mesh(mesh, color=True)
    p.add_mesh(mesh_edge, color="red", line_width=5)
    p.show()

def move_points(list_x,list_y ,x_shift=None, y_shift=None):
    if x_shift==None:
        x_shift = min(list_x)
    if y_shift==None:
        y_shift = min(list_y)
        
    new_list_x = []
    new_list_y = []
    xy_points = []
    
    for x in list_x:
        new_list_x.append(x - x_shift)
        xy_points.append([x - x_shift])

    for i in range(len(list_y)):
        y = list_y[i]
        new_list_y.append(y - y_shift)
        xy_points[i].append(y - y_shift)

    return new_list_x , new_list_y , xy_points

def move_points_array(points): #points = np.transpose( np.array( [np.array(x_list) , np.array(y_list) , np.array(z_list)] ) )
    x_min = np.min(points[:,0])
    y_min = np.min(points[:,1])

    points[:,0] -= x_min
    points[:,1] -= y_min
    

    return points


def same_line(l1,l2):
    rnd = 1
    l111 = [ [ round(l1[0][0],rnd) , round(l1[0][1],rnd) , 0 ] , [ round(l1[1][0],rnd) , round(l1[1][1],rnd) , 0 ] ]
    l222 = [ [ round(l2[0][0],rnd) , round(l2[0][1],rnd) , 0 ] , [ round(l2[1][0],rnd) , round(l2[1][1],rnd) , 0 ] ]

    l11 = [ [ round(l1[0][0],rnd) , round(l1[0][1],rnd) ] , [ round(l1[1][0],rnd) , round(l1[1][1],rnd) ] ]
    l22 = [ [ round(l2[0][0],rnd) , round(l2[0][1],rnd) ] , [ round(l2[1][0],rnd) , round(l2[1][1],rnd) ] ]
    
    vectorial_product = normal2( l111 , l222 ,rounding = 3)
    if vectorial_product == [0, 0, 0]: #the 2 line are //
        a , b = _2D_line_equation(l11)
        x22 = l22[0][0]
        y22 = round(l22[0][1],rnd)
        y = round(a*x22 + b,rnd)

        if y == y22:
            return True
    return False

def dist_point_line(p1,l):
    p2 = l[0]
    p3 = l[1]
    a = dist(p1,p2)
    b = dist(p1,p3)
    c = dist(p2,p3)
    #Heron's formula
    s = (a+b+c)/2
    h = 2/c * (( s*(s-a) * (s-b) * (s-c) )**2)**0.25
    return h
        


#https://portailsig.org/content/sur-la-creation-des-enveloppes-concaves-concave-hull-et-les-divers-moyens-d-y-parvenir-forme.html
#https://stackoverflow.com/questions/23073170/calculate-bounding-polygon-of-alpha-shape-from-the-delaunay-triangulation
def alpha_shape(points, alpha, only_outer=True, Pbl=None, Ptr=None, flat=True):
    """
    Compute the alpha shape (concave hull) of a set of points.
    :param points: np.array of shape (n,2) points.
    :param alpha: alpha value.
    :param only_outer: boolean value to specify if we keep only the outer border
    or also inner edges.
    :return: set of (i,j) pairs representing edges of the alpha-shape. (i,j) are
    the indices in the points array.
    """
    assert points.shape[0] > 3, "Need at least four points"

    def add_edge(edges, i, j):
        """
        Add a line between the i-th and j-th points,
        if not in the list already
        """
        if (i, j) in edges or (j, i) in edges:
            # already added
            assert (j, i) in edges, "Can't go twice over same directed edge right?"
            if only_outer:
                # if both neighboring triangles are in shape, it is not a boundary edge
                edges.remove((j, i))
            return
        edges.add((i, j))
    hard_border = []
    if Pbl!=None and Ptr!=None:
        l1 = [ Pbl , [ Pbl[0] , Ptr[1] ] ]
        l2 = [ Pbl , [ Ptr[0] , Pbl[1] ] ]
        l3 = [ Ptr , [ Pbl[0] , Ptr[1] ] ]
        l4 = [ Ptr , [ Ptr[0] , Pbl[1] ] ]
        hard_border = [l1,l2,l3,l4]
    
    tri = Delaunay(points)
    #print('len(tri.simplices):',len(tri.simplices))
    final_triangles = []
    edges = set()
    # Loop over triangles:
    # ia, ib, ic = indices of corner points of the triangle
    for ia, ib, ic in tri.simplices:
        pa = points[ia]
        pb = points[ib]
        pc = points[ic]

        skip = False
        
        if len(hard_border) == 4: #if we are resizinfg the file
            lab = [pa , pb]
            lac = [pa , pc]
            lbc = [pb , pc]

            if flat == True: #if we flatten edges, basicaly we ignore alpha on the edges
                dmax = 5
                near_border = False
                for l in hard_border:
                    if skip == False: #a triangle can be near 2 edges on a corner but we don't want to add it twice
                        d1 = dist_point_line(pa,l)
                        d2 = dist_point_line(pb,l)
                        d3 = dist_point_line(pc,l)
                        if (d1 <= dmax and d2 <= dmax) or (d1 <= dmax and d3 <= dmax) or (d3 <= dmax and d2 <= dmax):
                            near_border = True
                        if near_border == True:
                            add_edge(edges, ia, ib)
                            add_edge(edges, ib, ic)
                            add_edge(edges, ic, ia)
                            if only_outer == False:
                                final_triangles.append( [ia , ib , ic] )
                            skip = True
        '''
            on_border = False
            for l in hard_border:
                if (same_line(l ,lab) == True) or (same_line(l ,lac) == True) or (same_line(l ,lbc) == True):
                    on_border = True
            if on_border == True:
                print('on border',end= ' ')
                add_edge(edges, ia, ib)
                add_edge(edges, ib, ic)
                add_edge(edges, ic, ia)
                if only_outer == False:
                    final_triangles.append( [ia , ib , ic] )
                skip = True
        '''       
        if skip == False:
                    
            # Computing radius of triangle circumcircle
            # www.mathalino.com/reviewer/derivation-of-formulas/derivation-of-formula-for-radius-of-circumcircle
            a = np.sqrt((pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2)
            b = np.sqrt((pb[0] - pc[0]) ** 2 + (pb[1] - pc[1]) ** 2)
            c = np.sqrt((pc[0] - pa[0]) ** 2 + (pc[1] - pa[1]) ** 2)
            s = (a + b + c) / 2.0
            if s * (s - a) * (s - b) * (s - c) >= 0:  
                area = np.sqrt(s * (s - a) * (s - b) * (s - c))
            else:
                area = 0
                
            if area != 0:
                circum_r = a * b * c / (4.0 * area)
            else:
                circum_r = infinity
            if circum_r < alpha:
                add_edge(edges, ia, ib)
                add_edge(edges, ib, ic)
                add_edge(edges, ic, ia)
                
                if only_outer == False:
                    final_triangles.append( [ia , ib , ic] )
                
    if only_outer == True:
        return edges
    else:
        return edges , final_triangles

def grid_triangles(point , x_spacing , y_spacing, xi, yi, zi, xa, ya, za ):
    xp = point[0]
    yp = point[1]

    #making sure the point is within the file area and if not moving it
    while xp < xi and xp < xa:
        xp += x_spacing
    while xp > xi and xp > xa:
        xp -= x_spacing

    while yp < yi and yp < ya:
        yp += y_spacing
    while yp > yi and yp > ya:
        yp -= y_spacing


    triangle_list=[]
    x_temp = xp
    while x_temp <= xa :
        triangle_list.append([ [x_temp,yi,zi],
                               [x_temp,yi,za],
                               [x_temp,ya,zi]     ])

        triangle_list.append([ [x_temp,ya,za],
                               [x_temp,yi,za],
                               [x_temp,ya,zi]     ])

        x_temp += x_spacing

    x_temp = xp - x_spacing
    while x_temp >= xi :
        triangle_list.append([ [x_temp,yi,0],
                               [x_temp,yi,za],
                               [x_temp,ya,0]     ])

        triangle_list.append([ [x_temp,ya,za],
                               [x_temp,yi,za],
                               [x_temp,ya,0]     ])

        x_temp -= x_spacing



    y_temp = yp
    while y_temp <= ya :
        triangle_list.append([ [xi,y_temp,0],
                               [xi,y_temp,za],
                               [xa,y_temp,0]     ])

        triangle_list.append([ [xa,y_temp,za],
                               [xi,y_temp,za],
                               [xa,y_temp,0]     ])

        y_temp += y_spacing

    y_temp = yp - y_spacing
    while y_temp >= yi :
        triangle_list.append([ [xi,y_temp,0],
                               [xi,y_temp,za],
                               [xa,y_temp,0]     ])

        triangle_list.append([ [xa,y_temp,za],
                               [xi,y_temp,za],
                               [xa,y_temp,0]     ])

        y_temp -= y_spacing

    return triangle_list
        
        
def visualaze_point_cloud(X,Y,Z): # X,Y,Z are lists
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(projection='3d')
    ax.scatter(X, Y, Z)
    plt.show()

def visualaze_point_cloud2(X,Y,Z): # X,Y,Z are np arrays
    print("\nX:",X,"\nY:",Y,"\nZ:",Z,"\n")
    h = plt.contourf(X, Y, Z)
    plt.axis('scaled')
    plt.show()

def visualaze_point_cloud3(x_list,y_list,z_list):
    #https://stackoverflow.com/questions/39727040/matplotlib-2d-plot-from-x-y-z-values
    from scipy.interpolate import interp2d

    # f will be a function with two arguments (x and y coordinates),
    # but those can be array_like structures too, in which case the
    # result will be a matrix representing the values in the grid 
    # specified by those arguments
    f = interp2d(x_list,y_list,z_list,kind="linear")

    x_coords = np.arange(min(x_list),max(x_list)+1)
    y_coords = np.arange(min(y_list),max(y_list)+1)
    Z = f(x_coords,y_coords)

    fig = plt.imshow(Z,
               extent=[min(x_list),max(x_list),min(y_list),max(y_list)],
               origin="lower")

    # Show the positions of the sample points, just to have some reference
    fig.axes.set_autoscale_on(False)
    plt.scatter(x_list,y_list,400,facecolors='none')

def visualaze_point_cloud4(x_list,y_list,z_list): 
    from matplotlib.colors import LogNorm

    x_list = np.array(x_list)
    y_list = np.array(y_list)
    z_list = np.array(z_list)

    N = int(len(z_list)**.5)
    z = z_list.reshape(N, N)
    plt.imshow(z, extent=(np.amin(x_list), np.amax(x_list), np.amin(y_list), np.amax(y_list)), norm=LogNorm(), aspect = 'auto')
    plt.colorbar()
    plt.show()

def visualaze_point_cloud5(x_list,y_list,z_list, n_max=500000 ,  Tstart=time.time()):  #n_max = max number of points shown in the preview
    #https://scipy-cookbook.readthedocs.io/items/Matplotlib_Gridding_irregularly_spaced_data.html
    t1 = Tstart
    import numpy as np
    from scipy.interpolate import griddata
    import matplotlib.pyplot as plt
    import numpy.ma as ma
    from numpy.random import uniform, seed
    plt.figure()
    points = np.array( [np.array(x_list) , np.array(y_list) , np.array(z_list)] )
    points = np.transpose(points)
    #print(points)
    
    #reducing the number of points to n:
    cnt = 0
    n_points_to_remove = len(points) - n_max
    #print('n_points_to_remove:',n_points_to_remove)
    while n_points_to_remove > 0:
        
        rng = np.random.default_rng()
        rints = rng.integers(low=0, high=len(points), size=n_points_to_remove)
        #print(points)
        #print(rints)
        points = np.delete(points, list(rints), axis=0) #https://thispointer.com/delete-elements-rows-or-columns-from-a-numpy-array-by-index-positions-using-numpy-delete-in-python/
        
        n_points_to_remove =  len(points) - n_max
        cnt +=1
        #print(cnt)
        
    #print('len(points):',len(points))
    

    
    npts = len(points)
    size = int(npts**0.5)
    #print(points)
    points = np.transpose(points)
    #print(points)
    x = points[0]
    y = points[1]
    z = points[2]

    #print(x)
    #print(y)
    #print(z)

    xmi = min(x)
    xma = max(x)
    ymi = min(y)
    yma = max(y)
    zmi = min(z)
    zma = max(z)
    
    # define grid.
    xi = np.linspace(xmi,xma,size)
    yi = np.linspace(ymi,yma,size)
    # grid the data.
    zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')
    # contour the gridded data, plotting dots at the randomly spaced data points.
    CS = plt.contour(xi,yi,zi,15,linewidths=0.5,colors='k')
    CS = plt.contourf(xi,yi,zi,15,cmap=plt.cm.jet)
    plt.colorbar() # draw colorbar
    # plot data points.
    #plt.scatter(x,y,marker='o',c='b',s=5)
    plt.xlim(xmi,xma)
    plt.ylim(ymi,yma)
    plt.title('preview (%d points)' % npts)

    print("\nit took %4.2f sec to show the preview\n" %(time.time()-t1) )
    plt.show()

def visualaze_point_cloud6(points,  Tstart=time.time()):  
    #https://scipy-cookbook.readthedocs.io/items/Matplotlib_Gridding_irregularly_spaced_data.html
    t1 = Tstart
    import numpy as np
    from scipy.interpolate import griddata
    import matplotlib.pyplot as plt
    import numpy.ma as ma
    from numpy.random import uniform, seed
    fig, axs = plt.subplots()
    

    
    npts = len(points)
    size = int(npts**0.5)
    x = points[:,0]
    y = points[:,1]
    z = points[:,2]

    #print(x)
    #print(y)
    #print(z)

    xmi = min(x)
    xma = max(x)
    ymi = min(y)
    yma = max(y)
    zmi = min(z)
    zma = max(z)
    
    step = 1 #meters
    n_lines = int( (zma-zmi)/step )

    
    # define grid.
    xi = np.linspace(xmi,xma,size)
    yi = np.linspace(ymi,yma,size)
    # grid the data.
    #zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')
    zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='nearest') #not the prettyest but it shouldn't interpolate points that are at -40m in a -5m zone, completly changing the deph scale
    # contour the gridded data, plotting dots at the randomly spaced data points.
    CS = plt.contour(xi,yi,zi,n_lines,linewidths=0.5,colors='k')
    CS = plt.contour(xi,yi,zi,[-4,2],linewidths=1,colors='k')
    CS = plt.contourf(xi,yi,zi,n_lines,cmap=plt.cm.jet)
    plt.colorbar() # draw colorbar
    # plot data points.
    #plt.scatter(x,y,marker='o',c='b',s=5)
    plt.xlim(xmi,xma)
    plt.ylim(ymi,yma)
    axs.set_aspect('equal', 'box')
    plt.title('preview (%d points)' % npts)

    print("\nit took %4.2f sec to show the preview\n" %(time.time()-t1) )
    plt.show()

def visualaze_point_cloud7(points,  Tstart=time.time()):  
    #https://scipy-cookbook.readthedocs.io/items/Matplotlib_Gridding_irregularly_spaced_data.html
    t1 = Tstart
    import numpy as np
    import matplotlib.pyplot as plt


    x = points[:,0]
    y = points[:,1]
    z = points[:,2]

    #https://matplotlib.org/stable/plot_types/unstructured/tripcolor.html#sphx-glr-plot-types-unstructured-tripcolor-py
    fig, ax = plt.subplots()
    #ax.plot(x, y, 'o', markersize=0.25, color='grey')
    ax.tripcolor(x, y, z)


    #https://matplotlib.org/stable/plot_types/unstructured/tricontour.html
    levels = np.linspace(z.min(), z.max(), 1)
    print('levels:',levels)
    ax.tricontour(x, y, z, levels=levels)
    
    #plt.colorbar()
    plt.xlim(min(x),max(x))
    plt.ylim(min(y),max(y))
    plt.title('preview (%d points)' % len(x))

    print("\nit took %4.2f sec to show the preview\n" %(time.time()-t1) )
    plt.show()


def export_name(xyz_file,xi,xa,yi,ya, resize=False):
    xyz_file = xyz_file.split('/')[-1]
    xyz_file = xyz_file.split('.')[0]

    if resize == True:
        export = ''.join([ xyz_file , '_' , str(int(float(xi))) , '_' , str(int(float(xa))) , '__' , str(int(float(yi))) , '_' , str(int(float(ya))) , '.stl' ])
    else:
        export = ''.join([ xyz_file ,'.stl' ])
    return export

def get_settings():
    #https://stackoverflow.com/questions/14990907/how-to-have-python-check-if-a-file-exists-and-create-it-if-it-doesnt
    try: #checking to see if the settings.txt file exists, and if not creates one
        with open('settings.txt') as file:
            a = 1 # this has the only purpuse of not making an error
            print('settings files exist') 
    except IOError:

        settings = """centre_on_0 1 (1 or 0)
z_min -25
z_max 100
z_high_tide 4
land_exa 2
water_exa 5
scale 20
alpha 15
lower_resolution 0 (1 or 0)
resolution 1
flaten_edges True (True or False)
put_base 1 (1 or 0)
tab 10
play 0.2
n_preview 10000"""
        f= open('settings.txt',"w")
        f.write(settings)
        f.close()

        print('settings files had to be created')

    f= open('settings.txt',"r")
    string = f.read()
    f.close()
    string = string.split('\n')
    settings = {}

    for i in string:
        i = i.split(' ')[:2]
        settings[i[0]] = i[1]
    
    return settings

def save_settings(settings):
    string = str(settings)
    # string looks like this: {'a': 1, 'z': 2}
    string = string.replace("{", "") #https://stackoverflow.com/questions/22187233/how-to-delete-all-instances-of-a-character-in-a-string-in-python
    string = string.replace("}", "")
    string = string.replace("'", "")
    string = string.replace(":", "")
    string = string.replace(", ", "\n")

    f= open('settings.txt',"w")
    f.write(string)
    f.close()

    print('settings saved')
