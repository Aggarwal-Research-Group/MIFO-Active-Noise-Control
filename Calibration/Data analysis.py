
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit 
from scipy.signal import find_peaks

def plotter(input):
    # Import der Messdaten
    CH_1,CH_2,outfile,distance,title = input
    CH_1_data = np.genfromtxt(CH_1,
                        delimiter=',',
                        skip_header=0)
    CH_2_data = np.genfromtxt(CH_2,
                        delimiter=',',
                        skip_header=0)
   
    plt.close()
    
    t_start = 102
    t_stop = 1352

    x = CH_2_data[t_start:t_stop,4]
    t = CH_1_data[t_start:t_stop,3]
    y = CH_1_data[t_start:t_stop,4]



    def triangular(x, a, b, c):
        return a + b*abs(x-c)
    
    popt, pcov = curve_fit(triangular, t, x, p0=[ 10, -300,0.002 ])
    
    err = np.sqrt(np.diag(pcov))

    print(popt)   
    print(err)

    plt.plot(t, x, label= "measurement")
    plt.plot(t, triangular(t, *popt), label='Fitted function')
    plt.xlabel("Time [s]")
    plt.ylabel("Voltage [V]")
    plt.title("Output function generator")
    
    
    information_string_entladen = r""" $ U(t)= a + b \times |t-c| $
    $ a = (%.3g \pm %.3g) V $
    $ b = (%.3g \pm %.3g) V/s $
    $ c = (%.3g \pm %.3g) s $"""%(popt[0],err[0],popt[1],err[1],popt[2],err[2])

    plt.text(0,3,information_string_entladen)

    plt.legend("best")
    plt.savefig("01.png")
    plt.close()


    plt.plot(t, y, label='measurment')
    plt.xlabel("Time [s]")
    plt.ylabel("Voltage [V]")
    plt.title("measured signal")
    
    """
    information_string_entladen =  $ U(t)= d + a \times |t-b| $
    $ a = (%.3g \pm %.3g) V $
    $ b = (%.3g \pm %.3g) V/t $
    $ c = (%.3g \pm %.3g) t $%(popt[0],err[0],popt[1],err[1],popt[2],err[2])

    plt.text(0,3,information_string_entladen)
    """

    plt.legend("best")
    plt.savefig("02.png")
    plt.close()


    f = plt.figure(figsize=(10, 4))
    ax1, ax2 = f.subplots(1, 2, sharey=True)
    f.supxlabel(r'Displacement_Voltage [V]') 
    f.supylabel("PD_voltage  [V]")
    f.suptitle(title)


    length = len(t)
    ax1.plot(triangular(t[:int(length/2)], *popt),y[:int(length/2)], label='Fitted function', color='green',zorder = 3)
    ax2.plot(triangular(t[int(length/2):], *popt),y[int(length/2):], label='Fitted function', color='green',zorder = 3)
    ax2.xaxis.set_inverted(True)

    # Grenzrequenz 

    # plt.text(10,0,information_string_entladen)

    # Speichern der Abbildung als PDF
    f.savefig(outfile)

    plt.close()

    f = plt.figure(figsize=(10, 4))
    ax1 = f.subplots(1, 1)

    x = CH_2_data[:,4]*15*15.7/980
    t = CH_1_data[:,3]
    y = CH_1_data[:,4]


    ax1.set_xlabel('Time [s]') 
    ax1.set_ylabel('Voltage [V]', color = 'black') 
    plot_1 = ax1.plot(t, y, color = 'black') 
    ax1.tick_params(axis ='y', labelcolor = 'black') 

    # Adding Twin Axes

    ax2 = ax1.twinx() 
    
    ax2.set_ylabel('Displacement in [lambda]', color = 'green') 
    plot_2 = ax2.plot(t, x, color = 'green') 
    ax2.tick_params(axis ='y', labelcolor = 'green') 
    ax2.axhline(1.25)
    ax2.axhline(1.75)

    f.savefig("04.png")



if __name__ == "__main__":
    l = [
        ["F0018CH1.CSV","F0018CH2.CSV", "00.png",0,"driven_piezo"],
    ]
    plotter(l[0])

#Test