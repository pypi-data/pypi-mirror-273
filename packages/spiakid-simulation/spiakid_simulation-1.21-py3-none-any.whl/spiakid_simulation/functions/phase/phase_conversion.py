import numpy as np
import multiprocessing as mp
import spiakid_simulation.functions.utils as Ut

def phase_conv(Photon,pix,conv_wv,conv_phase,resolution, process_nb):
    r"""Convert the wavelength in phase on each pixel

    Parameters:
    -----------

    Photon: array
        Photon's wavelength on each pixel

    pix: array
        Pixel id

    conv_wv: array
        Calibration's wavelength

    conv_phase: array
        Calibration's phase

    resolution: float
        Spectrale resolution of the detector

    Output:
    -------

    signal: array
        Phase on each pixel 
    
    
    """
    dim = np.shape(Photon)
    signal = np.zeros(dim,dtype = object)
    dict = {}
    for i in range(len(pix)):
        dict[pix[i]] = [conv_wv[i],conv_phase[i]]
    pool = mp.Pool(process_nb)
    res = []
    for i in range(dim[0]):
        for j in range(dim[1]):

            results = pool.apply_async(photon2phase,args=(Photon[i,j],dict[str(i)+'_'+str(j)][0],dict[str(i)+'_'+str(j)][1], resolution,i,j))
            res.append((i,j,results))
    for i,j,result in res:
        _,_,value = result.get()
        signal[i,j] = value
    pool.close()
    pool.join()
    return(signal)


def phase_conv_calib(data,pix,conv_wv,conv_phase,resolution, process_nb):
    signal_calib = []
    dim_x,dim_y = np.shape(data[0][1])
    dict = {}
    for i in range(len(pix)):
        dict[pix[i]] = [conv_wv[i],conv_phase[i]]
    for wv in range(len(data)):
        signal = np.zeros(shape=(dim_x,dim_y),dtype = object)
        pool = mp.Pool(process_nb)
        res = []
        for i in range(dim_x):
            for j in range(dim_y):
                results = pool.apply_async(photon2phase,args=(data[wv][1][i,j],dict[str(i)+'_'+str(j)][0],dict[str(i)+'_'+str(j)][1], resolution,i,j))
                res.append((i,j,results))
        for i,j,result in res:
            _,_,value = result.get()
            signal[i,j] = value
        pool.close()
        pool.join()
        signal_calib.append([wv,signal])

    return(signal_calib)

def photon2phase(Photon,conv_wv,conv_phase, resolution,i,j):
    r"""Convert the wavelength in phase

    Parameters:
    -----------

    Photon: array
        Photon's wavelength on each pixel

    conv_wv: array
        Calibration's wavelength

    conv_phase: array
        Calibration's phase

    Output:
    -------

    signal: array
        Signal converted in phase 
    
    
    """
    signal = np.copy(Photon)
    curv = Ut.fit_parabola(conv_wv,conv_phase)
    ph = curv[0] * Photon[1] ** 2 +  curv[1] * Photon[1] + curv[2] #µ
    sigma = ph / (2*resolution*np.sqrt(2*np.log10(2)))
    signal[1] = np.where(Photon[1]==0,Photon[1],np.random.normal(ph, sigma))
    return(i,j,signal)

def exp_adding(phase,decay, process_nb):
    r""" Add the exponential decay after the photon arrival on each pixel

    Parameters:
    -----------

    phase: array
        Signal on each pixel

    decay: float
        The decay of the decreasing exponential
    
    Output:
    -------
    
    signal: array
        The signal with the exponential decrease on each pixel 
    
    """
    dim = np.shape(phase)
    signal = np.zeros(dim,dtype = object)
    pool = mp.Pool(process_nb)
    res = []
    for i in range(dim[0]):
          for j in range(dim[1]):
            #    print(i,j)
            results = pool.apply_async(exp, args=(phase[i,j],decay,i,j))
            res.append((i,j,results))
            #    signal[i,j] = exp(phase[i,j],decay,signal,i,j)
    for i,j,result in res:
        _,_,value = result.get()
        signal[i,j] = value
    pool.close()
    pool.join()
    return(signal)

def exp_adding_calib(data,decay,process_nb):
    signal_calib = []
    dim = np.shape(data[0][1])
    for wv in range(len(data)):
        pool = mp.Pool(process_nb)
        res = []
        signal = np.zeros(dim,dtype = object)
        for i in range(dim[0]):
            for j in range(dim[1]):
                results = pool.apply_async(exp, args=(data[wv][1][i,j],decay,i,j))
                res.append((i,j,results))
        for i,j,result in res:
            _,_,value = result.get()
            signal[i,j] = value
          
        pool.close()
        pool.join()
        signal_calib.append([data[wv][0],signal])
    return(signal_calib)

def exp(sig,decay,i,j):
    r""" Add the exponential decay after the photon arrival

    Parameters:
    -----------

    sig: array
        Signal with the photon arrival

    decay: float
        The decay of the decreasing exponential
    
    Output:
    -------
    
    signal: array
        The signal with the exponential decrease
    
    """
    sig_time = np.copy(sig[0])
    sig_amp = np.zeros((len(sig_time)))
    
    phase_point = np.copy(sig[1])
    for i in range(len(sig[1])):
        if phase_point[i] !=0:
                if i+500 < len(sig[0]):
                    for j in range(0,500):
                        exp_time = sig[0][i:i+500]
                        sig_amp[i+j] += sig[1][i] * np.exp(decay * (exp_time[j]-exp_time[0])) 
                else:
                     for j in range(0,len(sig[1])-i):
                        exp_time = sig[0][i:len(sig[1])]
                        sig_amp[i+j] += sig[1][i] * np.exp(decay * (exp_time[j]-exp_time[0]))
    return(i,j,[sig_time,sig_amp])


