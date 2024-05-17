import numpy as np
import multiprocessing as mp


def pixel_sorting(time,data,point_nb,time_data, signal,i ,j):
        r""" Sort value according to the time

        Parameters:
        -----------

        time: float
            Time of observation

        data: array
            Photon's wavelength
        
        point_nb: int
            Number of point we want
        
        Output:
        -------

        signal: array
            Arrival time and wavelength of photons randomly spread
        
        """
        point_nb = int(point_nb)
       
        if type(data) == list:
            t = np.linspace(0,time,point_nb)
            wv = np.zeros_like(t)
            sig  = [t,wv]
            sig[1][time_data] = data
        
            # sig[0] = np.linspace(0,time,point_nb-len(data))
            # sig[0] = list(sig[0]) + list(photon_time)
            # sig[1] = list(sig[1]) + list(data)
            # signal_int = []
            # for p in range(len(sig[0])):
            #     signal_int.append((sig[0][p],sig[1][p]))
            # Sorted_signal = sorted(signal_int,key=lambda x:x[0])
            # for p in range(len(sig[0])):
            #     sig[0][p] = Sorted_signal[p][0]
            #     sig[1][p] = Sorted_signal[p][1]
        
        
        else:
             sig = list(np.zeros([2,point_nb]))
             sig[0] = np.linspace(0,time,point_nb)
        # signal[i,j] = np.array(sig)
        return(i,j,sig)
        


def sorting(time,data,point_nb, time_data, process_nb):
    r""" Sort value according to the time on each pixel

        Parameters:
        -----------

        time: float
            Time of observation

        data: array
            Photon's wavelength
        
        point_nb: int
            Number of point we want
        
        Output:
        -------

        signal: array
            Arrival time and wavelength of photons randomly spread on each pixel
        
        """
    dim = np.shape(data)
    # print('timeline')
    signal = np.zeros(dim,dtype = object)
    Point_number = point_nb * time
    pool = mp.Pool(process_nb)
    res = []
    for i in range(dim[0]):
          for j in range(dim[1]):
            # print(i,j,len(data[i,j]))
            
            results = pool.apply_async(pixel_sorting, args=(time,data[i,j],Point_number,time_data[i,j],signal,i,j))
            res.append((i,j,results))

    
    # print(res)
    for i,j,result in res:
         _,_,value = result.get()
        #  print(value)
         signal[i,j] = value
    pool.close()
    pool.join()

    

    return(signal)



def sorting_calib(dim, point_number,wv_inter):
    wv_step = np.linspace(start = wv_inter[0]+0.05,stop = wv_inter[1]-0.05, num = 3)
    x_det,y_det = dim
    element = 300
    signal_calib = []
    
    for wv in wv_step:
        signal = np.zeros(shape=dim,dtype = object)
        for i in range(x_det):
             for j in range(y_det):
                time = np.linspace(0,1,point_number)
                wv_list = np.zeros(shape = point_number)
                indx = np.round(np.linspace(element-1,len(wv_list)-1,int(len(wv_list-element)/element))).astype(int)
                wv_list[indx] = wv
                signal[i,j] = [time,wv_list]
        
        signal_calib.append([wv,signal])
    return(signal_calib)