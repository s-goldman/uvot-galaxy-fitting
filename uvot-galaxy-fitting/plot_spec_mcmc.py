import numpy as np
import matplotlib
matplotlib.interactive(False)
import matplotlib.pyplot as plt
import pickle

import model_parameters
import best_val_chi2

def spectrum(lambda_list, mag, mag_err, grid_func,
                 best_fit, file_label, verbose=False):
    """
    Make a spectrum of the data and the best-fit model, and save the model magnitudes

    The best-fit parameters are extracted using the file_label with best_val_chi2.py


    Parameters
    ----------
    lambda_list : array of floats
        wavelengths (in Angstroms) for each photometric point

    mag : array of floats
        AB magnitudes of the photometry

    mag_err : array of floats
        errors for each magnitude

    grid_func : list of functions
        a list of functions, where each function outputs the model f_nu for each filter

    best_fit : dict
        the dictionary with the best-fit values (and errors) output from best_val_mcmc.py

    file_label : string
        the label associated with the region/galaxy
        
    verbose : boolean
        set to True to print out model magnitudes

    Returns
    -------
    nothing

    """

    # plot photometry
    plt.figure(figsize=(7,5))
    plt.errorbar( np.log10(lambda_list), mag, \
                  yerr=mag_err, fmt='ko', fillstyle='none' )
    plt.xlim(3,5)
    #plt.ylim(15,11.5)
    ax = plt.gca()
    ax.set_ylim(ax.get_ylim()[::-1])
    plt.xlabel('Log Wavelength (A)')
    plt.ylabel('AB Mag')

    # file to save the model magnitudes
    model_file = open('./results/modelmag_'+str(file_label)+'.list','w')
    model_file.write('# wavelength (A)     model (AB mag) \n')
   
    
    # grab the model magnitudes for the best fit
    model_mag = np.empty(len(lambda_list))
    for m in range(len(lambda_list)):
        temp = np.array([ best_fit['tau'], best_fit['av'], 10**(best_fit['log_age']),
                              best_fit['bump'], best_fit['rv'] ])
        model_mag[m] = -2.5 * np.log10( grid_func[m](temp) * 10**best_fit['log_mass'] ) - 48.6

        model_file.write(' ' + str(lambda_list[m]) + '      ' + str(model_mag[m]) + '\n')

    # close file
    model_file.close()

    if verbose == True:
        print('best-fit model magnitudes:')
        print(model_mag)

    plt.plot(np.log10(lambda_list), model_mag, 'b^')

    #plt.tight_layout(h_pad=0.1)
    #plt.show()
    plt.savefig('./plots/spectrum_'+file_label+'.pdf')
    plt.close()
