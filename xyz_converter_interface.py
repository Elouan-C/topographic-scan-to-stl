from tkinter import *
from tkinter.tix import *
from Convertor_library import *
import time

def is_numeric(s):  #https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
    """ Returns True is string is a number. """
    try:
        int(s)
        return True
    except ValueError:
        try:
            float(s)
            return True
        except ValueError:
            return False
    
def extracte_info():
    t1 = time.time()
    print('extracting info')

    global lines
    
    nom_fichier = name_ent.get()
    text_file = open(nom_fichier, "r")
    lines = text_file.read().split('\n')
    text_file.close()
    

    x_list=[]
    y_list=[]
    z_list=[]

    if lower_resolution.get() == 1 and is_numeric(resolution_ent.get()):
        jump = int(resolution_ent.get())
    else:
        jump = 1
        
    for str_point in lines[::jump]:
        temp_point =  str_point.split(' ')
        if len(temp_point) >= 3:
            x_list.append(float(temp_point[0]))
            y_list.append(float(temp_point[1]))
            z_list.append(float(temp_point[2]))
            
    #visualaze_point_cloud(x_list,y_list,z_list)
    
    n_points = len(x_list)
    x_min = min(x_list)
    x_max = max(x_list)
    y_min = min(y_list)
    y_max = max(y_list)
    z_min = min(z_list)
    z_max = max(z_list)

    print(n_points,'points')
    print(x_min,'< x <',x_max,'    Δ=',x_max-x_min)
    print(y_min,'< y <',y_max,'    Δ=',y_max-y_min)
    print(z_min,'< z <',z_max,'    Δ=',z_max-z_min)

    X_min.set(x_min)
    X_max.set(x_max)
    Y_min.set(y_min)
    Y_max.set(y_max)
    Z_min.set(z_min)
    Z_max.set(z_max)
    N.set(n_points)

    xi_ent.delete(0, 'end')
    xa_ent.delete(0, 'end')
    yi_ent.delete(0, 'end')
    ya_ent.delete(0, 'end')
    zi_ent.delete(0, 'end')
    za_ent.delete(0, 'end')
    
    xi_ent.insert(0,str(x_min))
    xa_ent.insert(0,str(x_max))
    yi_ent.insert(0,str(y_min))
    ya_ent.insert(0,str(y_max))
    zi_ent.insert(0,str(settings['z_min']))  #-25
    za_ent.insert(0,str(settings['z_max']))  #100

    update_info()

    ChkBttn1_resize.config(state = NORMAL)
    ChkBttn3_rescale.config(state = NORMAL)
    Button_convert.config(state = NORMAL)
    centre.set(0)
    ChkBttn6_advanced.config(state = NORMAL)
    ChkBttn4_lower_res.config(state = NORMAL)
    Button_preview.config(state = NORMAL)
    
    
    
    print("oppened file in",sec_time(time.time() - t1),'\n')


def update_info(centre=False):
    x_min = X_min.get()
    x_max = X_max.get()
    y_min = Y_min.get()
    y_max = Y_max.get()
    z_min = Z_min.get()
    z_max = Z_max.get()
    n_points = N.get()

    

    #print(x_min,x_max,y_min,y_max,z_min,z_max,n_points)
    #print((type(x_min) != str) and (type(x_max) != str) and (type(y_min) != str) and (type(y_max) != str) and (type(z_min) != str) and (type(z_max) != str) and (type(n_points) != str))
    if is_numeric(x_min) and is_numeric(x_max) and is_numeric(y_min) and is_numeric(y_max) and is_numeric(z_min) and is_numeric(z_max) and is_numeric(n_points):
        x_min = float(x_min)
        x_max = float(x_max)
        y_min = float(y_min)
        y_max = float(y_max)
        z_min = float(z_min)
        z_max = float(z_max)
        n_points = float(n_points)
        
        if centre == True:
            x_max -= x_min
            x_min = 0

            y_max -= y_min
            y_min = 0

        #https://stackoverflow.com/questions/5180365/python-add-comma-into-number-string
        info.set(''.join(['infos:\n',
                      str(str("{:,}".format(int(n_points)))),' points\n',
                      str(round(x_min,3)),' < X < ',str(round(x_max,3)),'    Δ=',str(round(x_max - x_min,3)),'\n',
                      str(round(y_min,3)),' < Y < ',str(round(y_max,3)),'    Δ=',str(round(y_max - y_min,3)),'\n',
                      str(round(z_min,3)),' < Z < ',str(round(z_max,3)),'    Δ=',str(round(z_max - z_min,3))]))

def resize_check_button():
    
    if resize_chk.get() == 1:
        label2_info.place(x=-100,y=60)

        
        labelxyz_.pack()
        labelxyz_.place(x=250,y=88)

        xi_ent.pack(padx = 10, pady = 5)
        xi_ent.place(x=265,y=84)
        
        xa_ent.pack(padx = 10, pady = 5)
        xa_ent.place(x=340,y=84)

        yi_ent.pack(padx = 10, pady = 5)
        yi_ent.place(x=265,y=104)

        ya_ent.pack(padx = 10, pady = 5)
        ya_ent.place(x=340,y=104)

        zi_ent.pack(padx = 10, pady = 5)
        zi_ent.place(x=265,y=124)

        za_ent.pack(padx = 10, pady = 5)
        za_ent.place(x=340,y=124)

        ChkBttn2.pack()
        ChkBttn2.place(x=330,y=50)
        
    else:
        label2_info.place(x=0,y=60)

        
        labelxyz_.pack_forget()
        labelxyz_.place_forget()

        xi_ent.pack_forget()
        xi_ent.place_forget()

        xa_ent.pack_forget()
        xa_ent.place_forget()

        yi_ent.pack_forget()
        yi_ent.place_forget()

        ya_ent.pack_forget()
        ya_ent.place_forget()

        zi_ent.pack_forget()
        zi_ent.place_forget()

        za_ent.pack_forget()
        za_ent.place_forget()

        ChkBttn2.pack_forget()
        ChkBttn2.place_forget()

def centre_check_button():
    
    x_min = float(X_min.get())
    x_max = float(X_max.get())
    y_min = float(Y_min.get())
    y_max = float(Y_max.get())

    shift_x = x_min
    shift_y = y_min

    xi = xi_ent.get()
    xa = xa_ent.get()
    yi = yi_ent.get()
    ya = ya_ent.get()
    
    if is_numeric(xi) and is_numeric(xa) and is_numeric(yi) and is_numeric(ya):
        xi = float(xi)
        xa = float(xa)
        yi = float(yi)
        ya = float(ya)

        xi_ent.delete(0, 'end')
        xa_ent.delete(0, 'end')
        yi_ent.delete(0, 'end')
        ya_ent.delete(0, 'end')
        
        if centre.get() == 1:
            update_info(centre=True)
            xi_ent.insert(0,str(round(xi-shift_x,3)))
            xa_ent.insert(0,str(round(xa-shift_x,3)))
            yi_ent.insert(0,str(round(yi-shift_y,3)))
            ya_ent.insert(0,str(round(ya-shift_y,3)))
            
        if centre.get() == 0:
            update_info()
            xi_ent.insert(0,str(round(xi+shift_x,3)))
            xa_ent.insert(0,str(round(xa+shift_x,3)))
            yi_ent.insert(0,str(round(yi+shift_y,3)))
            ya_ent.insert(0,str(round(ya+shift_y,3)))

def rescale_z_check_button():
    if rescale_z.get() == 1:
        z_high_tide_ent.pack()
        z_high_tide_ent.place(x=70,y=210)

        land_exa_ent.pack()
        land_exa_ent.place(x=70,y=240)

        water_exa_ent.pack()
        water_exa_ent.place(x=70,y=270)

        label4_high_tide.pack()
        label4_high_tide.place(x=6,y=210)

        label5_land_exa.pack()
        label5_land_exa.place(x=15,y=240)

        label6_water_exa.pack()
        label6_water_exa.place(x=10,y=270)

        


    else:

        z_high_tide_ent.pack_forget()
        z_high_tide_ent.place_forget()

        land_exa_ent.pack_forget()
        land_exa_ent.place_forget()

        water_exa_ent.pack_forget()
        water_exa_ent.place_forget()

        label4_high_tide.pack_forget()
        label4_high_tide.place_forget()

        label5_land_exa.pack_forget()
        label5_land_exa.place_forget()

        label6_water_exa.pack_forget()
        label6_water_exa.place_forget()

        
    
def lower_resolution_check_button():
    #print('lower')
    if lower_resolution.get() == 1:
        resolution_ent.config(state = NORMAL)
    else:
        resolution_ent.config(state = DISABLED)
        

def advanced_options_check_button():
    if advanced_chk.get() == 1:
        #ChkBttn3_rescale.pack()
        #ChkBttn3_rescale.place(x=20,y=180)
        '''
        label7_name_stl.place(x=10,y=280)

        export_file_ent.place(x=10,y=305)

        Button_convert.place(bordermode=OUTSIDE,x=200,y=330)
        '''

        label7_name_stl.place(x=10,y=350)

        export_file_ent.place(x=10,y=375)

        Button_convert.place(bordermode=OUTSIDE,x=200,y=400)
        
        z_high_tide_ent.pack()
        z_high_tide_ent.place(x=70,y=180)

        land_exa_ent.pack()
        land_exa_ent.place(x=70,y=210)

        water_exa_ent.pack()
        water_exa_ent.place(x=70,y=240)

        label4_high_tide.pack()
        label4_high_tide.place(x=6,y=180)

        label5_land_exa.pack()
        label5_land_exa.place(x=15,y=210)

        label6_water_exa.pack()
        label6_water_exa.place(x=10,y=240)

        label8_alpha.pack()
        label8_alpha.place(x=180,y=180)

        alpha_ent.pack()
        alpha_ent.place(x=200,y=182)

        ChkBttn5_show.pack()
        ChkBttn5_show.place(x=300,y=350)

        ChkBttn4_lower_res.pack()
        ChkBttn4_lower_res.place(x=300,y=180)

        resolution_ent.pack(padx = 10, pady = 5)
        resolution_ent.place(x=330,y=205)

        ChkBttn7_grid.pack()
        ChkBttn7_grid.place(x=180,y=205)
        '''
        origine_x_ent.pack()
        origine_x_ent.place(x=145,y=230)
        
        origine_y_ent.pack()
        origine_y_ent.place(x=215,y=230)

        x_spacing_ent.pack()
        x_spacing_ent.place(x=180,y=255)

        y_spacing_ent.pack()
        y_spacing_ent.place(x=180,y=280)
        '''
        ChkBttn8flat_edge.pack()
        ChkBttn8flat_edge.place(x=300,y=220)

        ChkBttn9_base.pack()
        ChkBttn9_base.place(x=300,y=247)

        label9_play.pack()
        label9_play.place(x=300,y=290)

        play_ent.pack()
        play_ent.place(x=330,y=293)

        label10_tab.pack()
        label10_tab.place(x=300,y=270)

        tab_ent.pack()
        tab_ent.place(x=330,y=273)

        scale_ent.pack()
        scale_ent.place(x=50,y=285)
        
        label11_scale.pack()
        label11_scale.place(x=10,y=285)

        Button_auto_name.place(bordermode=OUTSIDE,x=120,y=345)
        grid_check_button()

        Button_preview.place(bordermode=OUTSIDE,x=300,y=400)

        Button_save_settings.place(bordermode=OUTSIDE,x=185,y=345)

        label12_preview.pack()
        label12_preview.place(bordermode=OUTSIDE,x=150,y=250)

        n_preview_ent.pack()
        n_preview_ent.place(bordermode=OUTSIDE,x=150,y=270)
        
    else:
        #ChkBttn3_rescale.pack_forget()
        #ChkBttn3_rescale.place_forget()

        label7_name_stl.place(x=10,y=190)

        export_file_ent.place(x=10,y=215)

        Button_convert.place(bordermode=OUTSIDE,x=200,y=250)

        z_high_tide_ent.pack_forget()
        z_high_tide_ent.place_forget()

        land_exa_ent.pack_forget()
        land_exa_ent.place_forget()

        water_exa_ent.pack_forget()
        water_exa_ent.place_forget()

        label4_high_tide.pack_forget()
        label4_high_tide.place_forget()

        label5_land_exa.pack_forget()
        label5_land_exa.place_forget()

        label6_water_exa.pack_forget()
        label6_water_exa.place_forget()

        label8_alpha.pack_forget()
        label8_alpha.place_forget()

        alpha_ent.pack_forget()
        alpha_ent.place_forget()

        ChkBttn5_show.pack_forget()
        ChkBttn5_show.place_forget()

        ChkBttn4_lower_res.pack_forget()
        ChkBttn4_lower_res.place_forget()

        resolution_ent.pack_forget()
        resolution_ent.place_forget()

        ChkBttn7_grid.pack_forget()
        ChkBttn7_grid.place_forget()

        origine_x_ent.pack_forget()
        origine_x_ent.place_forget()

        origine_y_ent.pack_forget()
        origine_y_ent.place_forget()

        x_spacing_ent.pack_forget()
        x_spacing_ent.place_forget()

        y_spacing_ent.pack_forget()
        y_spacing_ent.place_forget()

        ChkBttn8flat_edge.pack_forget()
        ChkBttn8flat_edge.place_forget()

        ChkBttn9_base.pack_forget()
        ChkBttn9_base.place_forget()

        label9_play.pack_forget()
        label9_play.place_forget()

        play_ent.pack_forget()
        play_ent.place_forget()

        label10_tab.pack_forget()
        label10_tab.place_forget()

        tab_ent.pack_forget()
        tab_ent.place_forget()

        scale_ent.pack_forget()
        scale_ent.place_forget()
        
        label11_scale.pack_forget()
        label11_scale.place_forget()

        Button_auto_name.place(bordermode=OUTSIDE,x=120,y=185)

        Button_preview.place(bordermode=OUTSIDE,x=300,y=250)

        Button_save_settings.pack_forget()
        Button_save_settings.place_forget()

        label12_preview.pack_forget()
        label12_preview.place_forget()

        n_preview_ent.pack_forget()
        n_preview_ent.place_forget()
        
def grid_check_button():
    if grid.get() == 1:
        origine_x_ent.config(state = NORMAL)
        origine_y_ent.config(state = NORMAL)
        x_spacing_ent.config(state = NORMAL)
        y_spacing_ent.config(state = NORMAL)

        origine_x_ent.pack()
        origine_x_ent.place(x=145,y=230)

        origine_y_ent.pack()
        origine_y_ent.place(x=215,y=230)

        x_spacing_ent.pack()
        x_spacing_ent.place(x=180,y=255)

        y_spacing_ent.pack()
        y_spacing_ent.place(x=180,y=280)
    else:
        origine_x_ent.config(state = DISABLED)
        origine_y_ent.config(state = DISABLED)
        x_spacing_ent.config(state = DISABLED)
        y_spacing_ent.config(state = DISABLED)

        origine_x_ent.pack_forget()
        origine_x_ent.place_forget()

        origine_y_ent.pack_forget()
        origine_y_ent.place_forget()

        x_spacing_ent.pack_forget()
        x_spacing_ent.place_forget()

        y_spacing_ent.pack_forget()
        y_spacing_ent.place_forget()

def put_base_check_button():
    if base.get() == 1:
        play_ent.config(state = NORMAL)
        tab_ent.config(state = NORMAL)
    else:
        play_ent.config(state = DISABLED)
        tab_ent.config(state = DISABLED)

def auto_export_name():
    xi = xi_ent.get()#user defined limits
    xa = xa_ent.get()
    yi = yi_ent.get()
    ya = ya_ent.get()
    file_name_xyz = name_ent.get()
    re = bool(resize_chk.get())

    
    export_stl_name = export_name(file_name_xyz,xi,xa,yi,ya, resize = re)

    export_file_ent.delete(0, 'end')
    export_file_ent.insert(0,export_stl_name)

def show_preview():
    print("preview")
    convert(preview=True , n_points_preview = 10000)

def save_settings_button():
    global settings

    z_min = float(zi_ent.get())
    z_max = float(za_ent.get())
    α = float(alpha_ent.get())
    high_tide = float(z_high_tide_ent.get())
    low_tide = float(z_low_tide_ent.get())
    sea_exa = float(water_exa_ent.get())
    land_exa = float(land_exa_ent.get())
    play = float(play_ent.get())
    tab_size = float(tab_ent.get())
    scale = float(scale_ent.get())
    
    settings['z_min'] = str(z_min)
    settings['z_max'] = str(z_max)
    settings['alpha'] = str(α)
    settings['z_high_tide'] = str(high_tide)
    settings['z_low_tide'] = str(low_tide)
    settings['water_exa'] = str(sea_exa)
    settings['land_exa'] = str(land_exa)
    settings['play'] = str(play)
    settings['tab'] = str(tab_size)
    settings['scale'] = str(scale)
    settings['centre_on_0'] = str(centre.get())
    settings['lower_resolution'] = str(lower_resolution.get())
    settings['resolution'] = str(resolution_ent.get())
    settings['flaten_edges'] = str(flat_edge.get())
    settings['put_base'] = str(base.get())
    settings['n_preview'] = str(int(n_preview_ent.get()))
    
    save_settings(settings)

    
def convert(preview=False , n_points_preview = 0):
    print("\n\n===================================================================================================================================================================================================================")
    Tstart = time.time()
    
    x_min = float(X_min.get())#file limits
    x_max = float(X_max.get())
    y_min = float(Y_min.get())
    y_max = float(Y_max.get())
    z_min = float(Z_min.get())
    z_max = float(Z_max.get())
    xi = float(xi_ent.get())#user defined limits
    xa = float(xa_ent.get())
    yi = float(yi_ent.get())
    ya = float(ya_ent.get())
    zi = float(zi_ent.get())
    za = float(za_ent.get())
    α = float(alpha_ent.get())
    file_name_xyz = name_ent.get()
    stl_file = export_file_ent.get()
    high_tide = float(z_high_tide_ent.get())
    low_tide = float(z_low_tide_ent.get())
    sea_exa = float(water_exa_ent.get())
    land_exa = float(land_exa_ent.get())
    play = float(play_ent.get())
    tab_size = float(tab_ent.get())
    scale = float(scale_ent.get())

    print('x_min: ',x_min)
    print('x_max: ',x_max)
    print('y_min: ',y_min)
    print('y_max: ',y_max)
    print('z_min: ',z_min)
    print('z_max: ',z_max)
    print('xi: ',xi)
    print('xa: ',xa)
    print('yi: ',yi)
    print('ya: ',ya)
    print('zi: ',zi)
    print('za: ',za)
    print('α: ',α)
    print('file_name_xyz: ',file_name_xyz)
    print('stl_file: ',stl_file)
    print('high_tide: ',high_tide)
    print('sea_exa: ',sea_exa)
    print('land_exa: ',land_exa)
    print('play: ',play)
    print('tab_size',tab_size)
    print('scale',scale)


    if resize_chk.get() == 0:
        xi = x_min
        xa = x_max
        yi = y_min
        ya = y_max
        zi = z_min
        za = z_max
    
    
    
    zi -= high_tide
    if zi >= 0:
        zi *= land_exa
    else:
        zi *= sea_exa

    za -= high_tide
    if za >= 0:
        za *= land_exa
    else:
        za *= sea_exa

    print(file_name_xyz,'\n')
    '''
    text_file = open(file_name_xyz, "r")
    lines = text_file.read().split('\n')
    text_file.close()
    #'''

    print('lines[:10] ',lines[:10])

    num_pnt = len(lines)

    #creating a list and numpy array of x , y & z coordinates
    x_list=[]
    y_list=[]
    z_list=[]

    xy_points = []

    print('\ncreating list of x,y,z\n')
    margin = 51
    if centre.get() == 1:
        shift_x = x_min
        shift_y = y_min
    else:
        shift_x = 0
        shift_y = 0
        
    t0 = time.time()
    
    if lower_resolution.get() == 1 and is_numeric(resolution_ent.get()):
        jump = int(resolution_ent.get())
        α *= jump
    else:
        jump = 1

    if preview==False:
        #print('α:',α)
            
        for str_point in lines[::jump]:
            temp_point =  str_point.split(' ')
            if len(temp_point) >= 3:
                #print(temp_point)
                
                z = float(temp_point[2])-high_tide 
                
                if z >= 0:
                    z *= land_exa
                    #z += high_tide * sea_exa # we have to add the high tide z offset back so that the models are compatible with the older versions
                else:
                    z *= sea_exa
                    #z += high_tide * sea_exa
                
                if z >= zi and z <= za:
                    if float(temp_point[0]) >= (xi-margin+shift_x) and float(temp_point[0]) <= (xa+margin+shift_x):
                        if float(temp_point[1]) >= (yi-margin+shift_y) and float(temp_point[1]) <= (ya+margin+shift_y):

                            if z < zi:
                                z = zi + 1
                            elif z > za:
                                z = za
                    
                            x_list.append(float(temp_point[0]) *scale/100)
                            y_list.append(float(temp_point[1]) *scale/100)
                            #z_list.append(z+high_tide-0.923)  #the "-0.923" comes frommeasurements made between an old gen map and a new one, this is so that they line up
                            z_list.append(z *scale/100)
                            
                            xy_points.append([ float(temp_point[0])*scale/100 , float(temp_point[1])*scale/100 ])

        
        x_min *= scale/100
        x_max *= scale/100
        y_min *= scale/100
        y_max *= scale/100
        z_min *= scale/100
        z_max *= scale/100
        xi *= scale/100
        xa *= scale/100
        yi *= scale/100
        ya *= scale/100
        zi *= scale/100
        za *= scale/100
        α *= scale/100
        high_tide *= scale/100
        play *= scale/100
        tab_size *= scale/100

    elif preview==True:
        #print("preview==True")
        for str_point in lines[::jump*2]:
            temp_point =  str_point.split(' ')
            if len(temp_point) >= 3:
                if float(temp_point[0]) >= (xi+shift_x) and float(temp_point[0]) <= (xa+shift_x):
                    if float(temp_point[1]) >= (yi+shift_y) and float(temp_point[1]) <= (ya+shift_y):

                #if float(temp_point[0]) >= (xi-margin+shift_x) and float(temp_point[0]) <= (xa+margin+shift_x):
                    #if float(temp_point[1]) >= (yi-margin+shift_y) and float(temp_point[1]) <= (ya+margin+shift_y):
                    
                        x_list.append(float(temp_point[0]))
                        y_list.append(float(temp_point[1]))
                        z_list.append(float(temp_point[2]))

        points = np.array( [np.array(x_list) , np.array(y_list) , np.array(z_list)] )
        points = np.transpose(points)                        
        n_max = int(n_preview_ent.get())
        n_points_to_remove = len(points) - n_max
        cnt = 0
        print("\nlen(points):        ",len(points))
        print("n_points_to_remove: ",n_points_to_remove,'\n')
        while n_points_to_remove > 0:
            
            rng = np.random.default_rng()
            rints = rng.integers(low=0, high=len(points), size=n_points_to_remove)
            #print(points)
            #print(rints)
            points = np.delete(points, list(rints), axis=0) #https://thispointer.com/delete-elements-rows-or-columns-from-a-numpy-array-by-index-positions-using-numpy-delete-in-python/
            
            n_points_to_remove =  len(points) - n_max
            cnt +=1

        points2 = np.transpose(points)  
        x_list = list(points2[0])
        y_list = list(points2[1])
        z_list = list(points2[2])

                            

    print('xi: ',xi)
    print('xa: ',xa)
    print('yi: ',yi)
    print('ya: ',ya)
    print('-')
    print( 'points:\n',np.transpose( np.array( [np.array(x_list) , np.array(y_list) , np.array(z_list)] ) ) , '\n' )
    if centre.get() == 1:
        if preview==False:
            x_list , y_list , xy_points = move_points(x_list,y_list) # move all the points near [0,0]
            shift_x = xi
            shift_y = yi

            xi -= shift_x
            xa -= shift_x
            yi -= shift_y
            ya -= shift_y
            print('xi: ',xi)
            print('xa: ',xa)
            print('yi: ',yi)
            print('ya: ',ya)

        elif preview==True:
            x_list , y_list , xy_points = move_points(x_list,y_list,x_shift=x_min, y_shift=y_min)
            shift_x = x_min
            shift_y = y_min
            
            print( 'points:\n',np.transpose( np.array( [np.array(x_list) , np.array(y_list) , np.array(z_list)] ) ) , '\n' )
        '''
        xi -= shift_x
        xa -= shift_x
        yi -= shift_y
        ya -= shift_y
        print('xi: ',xi)
        print('xa: ',xa)
        print('yi: ',yi)
        print('ya: ',ya)
        '''

    print("it took %4.2f sec to move around the points\n" %(time.time()-t0) ) 
    x_min = min(x_list)
    x_max = max(x_list)
    y_min = min(y_list)
    y_max = max(y_list)
    z_min = min(z_list)
    z_max = max(z_list)

    print('before resizing:')
    print(len(x_list),'points')
    print(x_min,'< x <',x_max,'    Δ=',x_max-x_min)
    print(y_min,'< y <',y_max,'    Δ=',y_max-y_min)
    print(z_min,'< z <',z_max,'    Δ=',z_max-z_min)
    
    if resize_chk.get() == 1:
        if flat_edge.get() == False:
            resiz , xy_points = resize( xi, xa, yi, ya, [x_list,y_list,z_list] , α)
            print('resize')
        else:
            resiz , xy_points = simple_resize( xi, xa, yi, ya, [x_list,y_list,z_list] )
            print('simple_resize')
        #print('\nresiz:',resiz)
        x_list = resiz[0]
        y_list = resiz[1]
        z_list = resiz[2]

        print( 'points:\n',np.transpose( np.array( [np.array(x_list) , np.array(y_list) , np.array(z_list)] ) ) , '\n' )

        x_min = min(x_list)
        x_max = max(x_list)
        y_min = min(y_list)
        y_max = max(y_list)
        z_min = min(z_list)
        z_max = max(z_list)

        print('\nafter resizing:')
        print(len(x_list),'points')
        print(x_min,'< x <',x_max,'    Δ=',x_max-x_min)
        print(y_min,'< y <',y_max,'    Δ=',y_max-y_min)
        print(z_min,'< z <',z_max,'    Δ=',z_max-z_min)
        
    if centre.get() == 1 and preview==False:
        x_list , y_list , xy_points = move_points(x_list,y_list) # move all the points near [0,0] to make sure the stl file will be near the origine
        xa -= xi
        ya -= yi
        xi = 0
        yi = 0

    x = np.asarray(x_list)
    y = np.asarray(y_list)
    z = np.asarray(z_list)

    if preview==True:
        points = np.transpose( np.array( [np.array(x_list) , np.array(y_list) , np.array(z_list)] ) )
        print( "\nxmin:", np.min( points[:,0] ))
        tide_points = visualaze_point_cloud6(points , low_tide , high_tide , Tstart=Tstart) #visualize the file
        return None
    

    p_centre = [ (x_max+x_min)/2 , (y_max+y_min)/2 , zi ]

    print('\ncreating α shape triangle mesh from points with α =',α)
    t0 = time.time()

    segments , tri = alpha_shape( np.array(xy_points) , α , only_outer=False , Pbl=[xi,yi] , Ptr=[xa,ya], flat=flat_edge.get() )
    edge_lines = alpha_shape( np.array(xy_points) , α , only_outer=True , Pbl=[xi,yi] , Ptr=[xa,ya], flat=flat_edge.get() )

    if type(tri) == set:
        tri = list(tri)
    if type(edge_lines) == set:
        edge_lines = list(edge_lines)

    t1 = time.time()
    total = t1-t0
    print('it took',sec_time(round(total,3)),'sec\n')
    print('\nnumber of points:    ',len(x_list))
    print('\nnumber of edges:    ',len(edge_lines))
    print('number of triangles: ',len(tri))
    print('triangles/points:    ',len(tri)/len(x_list))

    use_grid = False
    if grid.get() == 1:
        use_grid = True

        origine = [float(origine_x_ent.get())*scale/100 , float(origine_y_ent.get()*scale/100)]
        x_spacing = float(x_spacing_ent.get())*scale/100
        y_spacing = float(y_spacing_ent.get())*scale/100
        
        extra_triangles_list = grid_triangles(origine , x_spacing , y_spacing, x_min, y_min, z_min, x_max, y_max, z_max*1.1 )

    f= open(stl_file,"w")
    f.write("solid xyz_to_stl\n")

    print('writing the stl file')
    t0 = time.time()

    if use_grid == False:
        write_stl(f,tri,x_list,y_list,z_list,edge_lines,zi,p_centre)# , pb=True)
    else:
        print('len(extra_triangles_list): ',len(extra_triangles_list),'\n',extra_triangles_list,'\n')
        write_stl(f,tri,x_list,y_list,z_list,edge_lines,zi,p_centre, extra_triangles = extra_triangles_list)
        
    t1 = time.time()
    f.write("endsolid xyz_to_stl")
    f.close()

    print('it took',round(t1-t0,3),'sec\n')

    if base.get() == 1:
        print("adding puzzle:\n")

        add_puzzle(stl_file,0,xi,yi,xa,ya,zi,play,tab_size)

    Tend = time.time()
    print('\nTotal run time:',sec_time(round(Tend - Tstart,3)))

    if show_stl_chk.get() == 1:
        show_stl(stl_file)

    print("\n===================================================================================================================================================================================================================\n")


        
###################################################################################################################################################################
###################################################################################################################################################################


settings = get_settings()        

lines = [] #global variable containig the data 

height = 700
width = 490
size = 'x'.join([str(width),str(height)])

root = Tk()
root.geometry(size)
#root.geometry(width,height)
#root.geometry("500x700")
 
frame = Frame(root)
frame.pack()

leftframe = Frame(root)
leftframe.pack(side=LEFT)
 
rightframe = Frame(root)
rightframe.pack(side=RIGHT)

#=========================================================================================================================#
#       VARIABLES       VARIABLES       VARIABLES       VARIABLES       VARIABLES       VARIABLES       VARIABLES         #
#=========================================================================================================================#

X_min = StringVar()
X_min.set('X min')

X_max = StringVar()
X_max.set('X max')

Y_min = StringVar()
Y_min.set('Y min')

Y_max = StringVar()
Y_max.set('Y max')

Z_min = StringVar()
Z_min.set(str(settings['z_min']))

Z_max = StringVar()
Z_max.set(str(settings['z_max']))

N = StringVar() # N = number of points
N.set('n')
#=========================================================================================================================#
#       SPACER LABEL       SPACER LABEL       SPACER LABEL       SPACER LABEL       SPACER LABEL       SPACER LABEL       #
#=========================================================================================================================#


spacer1 = StringVar()
spacer1.set(''.join([ '.' , ''.join( ['   ']*50 ) , '.' ]))
label0_0 = Label(leftframe, textvariable = spacer1, width = 70 )
label0_0.pack()

spacer2 = StringVar()
spacer2.set(''.join([ '*' , ''.join( ['\n']*26 ) , '*' ]))
label0_1 = Label(leftframe, textvariable = spacer2, width = 70 )
label0_1.pack()



#=========================================================================================================================#
#       LABEL       LABEL       LABEL       LABEL       LABEL       LABEL       LABEL       LABEL       LABEL       LABEL #
#=========================================================================================================================#

f_name = StringVar()
f_name.set("name of the .xyz file to convert:")
label1 = Label(leftframe, textvariable = f_name, width = 50 )
label1.pack()
label1.place(x=30,y=0)


info = StringVar()
info.set(''.join(['infos:\n',
                  '?',' points\n',
                  X_min.get(),' < X < ',X_max.get(),'    Δ=','?','\n',
                  Y_min.get(),' < Y < ',Y_max.get(),'    Δ=','?','\n',
                  Z_min.get(),' < Z < ',Z_max.get(),'    Δ=','?']))
label2_info = Label(leftframe, textvariable = info, width = 60 )
label2_info.pack()
label2_info.place(x=0,y=60)

xyz_ = StringVar()
xyz_.set("x:\ny:\nz:")
labelxyz_ = Label(leftframe, textvariable = xyz_)#, width = 60 )

z_high_tide_ = StringVar()
z_high_tide_.set("z high tide           m")
label4_high_tide = Label(leftframe, textvariable = z_high_tide_)

land_exa_ = StringVar()
land_exa_.set("land exa")
label5_land_exa = Label(leftframe, textvariable = land_exa_)

water_exa_ = StringVar()
water_exa_.set("water exa")
label6_water_exa = Label(leftframe, textvariable = water_exa_)

stl_name = StringVar()
stl_name.set("name of the .stl file:")
label7_name_stl = Label(leftframe, textvariable = stl_name )
label7_name_stl.pack()
label7_name_stl.place(x=10,y=190)

alpha_input = StringVar()
alpha_input.set("α:           m")
label8_alpha = Label(leftframe, textvariable = alpha_input )

play_input = StringVar()
play_input.set("play:             mm")
label9_play = Label(leftframe, textvariable = play_input )

tab_input = StringVar()
tab_input.set("tab:               mm")
label10_tab = Label(leftframe, textvariable = tab_input )

scale_input = StringVar()
scale_input.set("scale:               %")
label11_scale = Label(leftframe, textvariable = scale_input )

preview_n_input = StringVar()
preview_n_input.set("points in preview:")
label12_preview = Label(leftframe, textvariable = preview_n_input )

#=========================================================================================================================#
#       TEXT BOX       TEXT BOX       TEXT BOX       TEXT BOX       TEXT BOX       TEXT BOX       TEXT BOX       TEXT BOX #
#=========================================================================================================================#

name_ent = Entry(leftframe, width =70)
#name_ent.insert(0,'nom_fichier.xyz')
name_ent.insert(0,'C:/Users/eloua/OneDrive/Documents/projet/xyz to stl/Github/bertheaum.xyz')
name_ent.pack(padx = 10, pady = 5)
name_ent.place(x=10,y=25)

xi_ent = Entry(leftframe, width =10)
xi_ent.insert(0,'x min')

xa_ent = Entry(leftframe, width =10)
xa_ent.insert(0,'x max')

yi_ent = Entry(leftframe, width =10)
yi_ent.insert(0,'y min')

ya_ent = Entry(leftframe, width =10)
ya_ent.insert(0,'y max')

zi_ent = Entry(leftframe, width =10)
zi_ent.insert(0,settings['z_min'])

za_ent = Entry(leftframe, width =10)
za_ent.insert(0,settings['z_max'])

z_high_tide_ent = Entry(leftframe, width =3)
z_high_tide_ent.insert(0 , settings['z_high_tide'])

z_low_tide_ent = Entry(leftframe, width =3)
z_low_tide_ent.insert(0 , settings['z_high_tide'])

land_exa_ent = Entry(leftframe, width =3)
land_exa_ent.insert(0 , settings['land_exa'])

water_exa_ent = Entry(leftframe, width =3)
water_exa_ent.insert(0 , settings['water_exa'])

export_file_ent = Entry(leftframe, width =70)
export_file_ent.insert(0 ,'file_name.stl')
export_file_ent.pack(padx = 10, pady = 5)
export_file_ent.place(x=10,y=215)

alpha_ent = Entry(leftframe, width =3)
alpha_ent.insert(0 , settings['alpha'] )

resolution_ent = Entry(leftframe, width =5)
resolution_ent.insert(0 , settings['resolution'] )
resolution_ent.config(state = DISABLED)

origine_x_ent = Entry(leftframe, width =10)
origine_x_ent.insert(0,'origine x')
origine_x_ent.config(state = DISABLED)

origine_y_ent = Entry(leftframe, width =10)
origine_y_ent.insert(0,'origine y')
origine_y_ent.config(state = DISABLED)

x_spacing_ent = Entry(leftframe, width =10)
x_spacing_ent.insert(0,'x spacing')
x_spacing_ent.config(state = DISABLED)

y_spacing_ent = Entry(leftframe, width =10)
y_spacing_ent.insert(0,'y spacing')
y_spacing_ent.config(state = DISABLED)

play_ent = Entry(leftframe, width =5)
play_ent.insert(0 , settings['play'] )
#play_ent.config(state = DISABLED)

tab_ent = Entry(leftframe, width =5)
tab_ent.insert(0 , settings['tab'] )

scale_ent = Entry(leftframe, width =4)
scale_ent.insert(0 , settings['scale'] )

n_preview_ent = Entry(leftframe, width =16)
n_preview_ent.insert(0 , int(settings['n_preview']) )

#=========================================================================================================================#
#       BUTTON       BUTTON       BUTTON       BUTTON       BUTTON       BUTTON       BUTTON       BUTTON       BUTTON    #
#=========================================================================================================================#
Button_deb = Button(leftframe, text = "Open", command = extracte_info)
Button_deb.pack(padx = 5, pady = 5)
Button_deb.place(bordermode=OUTSIDE,x=443,y=22)

Button_convert = Button(leftframe, text = "Convert", command = convert)
Button_convert.pack(padx = 5, pady = 5)
Button_convert.place(bordermode=OUTSIDE,x=200,y=250)
Button_convert.config(state = DISABLED)

Button_auto_name = Button(leftframe, text = ".", command = auto_export_name)
Button_auto_name.pack(padx = 5, pady = 5)
Button_auto_name.place(bordermode=OUTSIDE,x=120,y=185)#(x=10,y=190)

Button_preview = Button(leftframe, text = "preview", command = show_preview)
Button_preview.pack(padx = 5, pady = 5)
Button_preview.place(bordermode=OUTSIDE,x=300,y=250)
Button_preview.config(state = DISABLED)

Button_save_settings = Button(leftframe, text = "save settings", command = save_settings_button)
#Button_save_settings.pack(padx = 5, pady = 5)
#Button_save_settings.place(bordermode=OUTSIDE,x=185,y=185)
#=========================================================================================================================#
#       CHECKBUTTON       CHECKBUTTON       CHECKBUTTON       CHECKBUTTON       CHECKBUTTON       CHECKBUTTON             #
#=========================================================================================================================#

resize_chk = IntVar()
ChkBttn1_resize = Checkbutton(leftframe, width = 0, variable = resize_chk,text="resize",command = resize_check_button)
ChkBttn1_resize.pack(padx = 5, pady = 5)
ChkBttn1_resize.place(x=260,y=50)
ChkBttn1_resize.config(state = DISABLED)

centre = IntVar(value = int(settings['centre_on_0']))
ChkBttn2 = Checkbutton(leftframe, width = 0, variable = centre,text="centre on 0",command = centre_check_button)


rescale_z = IntVar()
ChkBttn3_rescale = Checkbutton(leftframe, width = 0, variable = rescale_z,text="rescale Z",command = rescale_z_check_button)
ChkBttn3_rescale.pack(padx = 5, pady = 5)
ChkBttn3_rescale.place(x=20,y=150)
ChkBttn3_rescale.config(state = DISABLED)

lower_resolution = IntVar()
ChkBttn4_lower_res = Checkbutton(leftframe, width = 0, variable = lower_resolution,text="lower resolution",command = lower_resolution_check_button)
#ChkBttn4_lower_res.config(state = DISABLED)

show_stl_chk = IntVar()
ChkBttn5_show = Checkbutton(leftframe, width = 0, variable = show_stl_chk,text="show stl when done")


advanced_chk = IntVar()
ChkBttn6_advanced = Checkbutton(leftframe, width = 0, variable = advanced_chk,text="Advanced options",command = advanced_options_check_button)
ChkBttn6_advanced.pack(padx = 5, pady = 5)
ChkBttn6_advanced.place(x=20,y=150)
#ChkBttn6_advanced.config(state = DISABLED)

grid = IntVar()
ChkBttn7_grid = Checkbutton(leftframe, width = 0, variable = grid,text="grid",command = grid_check_button)


flat_edge = BooleanVar(value = bool(settings['flaten_edges']))
ChkBttn8flat_edge = Checkbutton(leftframe, width = 0, variable = flat_edge,text="flaten edges")#,command = flaten_edges)


base = IntVar(value = int(settings['put_base']))
ChkBttn9_base = Checkbutton(leftframe, width = 0, variable = base,text="put base",command = put_base_check_button)


#=========================================================================================================================#
#       TOOLTIP       TOOLTIP       TOOLTIP       TOOLTIP       TOOLTIP       TOOLTIP       TOOLTIP       TOOLTIP         #
#=========================================================================================================================#

tip = Balloon(root)

tip.bind_widget(alpha_ent,balloonmsg="Maximum size of the triangles' circumscribed circle")

tip.bind_widget(resolution_ent,balloonmsg="divide the number of points in the file by this number")
tip.bind_widget(ChkBttn4_lower_res,balloonmsg="divide the number of points in the file by this number")


tip.bind_widget(tab_ent,balloonmsg="Size of the Dove tail\n      _______  \n       \\       /  \n    ___\\   /___")


tip.bind_widget(ChkBttn8flat_edge,balloonmsg="ignore α on the edges to ensure a smoother surface")

tip.bind_widget(ChkBttn7_grid,balloonmsg="put a grid over the model")











root.title("Convertor .xyz -> .stl")
root.mainloop()
