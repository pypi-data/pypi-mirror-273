import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from Functions import *

def constructRanges(wavelength_range, resolution, precision):
    sep = (wavelength_range[1] - wavelength_range[0]) / (2*resolution)
    arr = []
    wall = wavelength_range[0]
    for i in range(resolution):
        new_wall = wall+2*sep
        arr.append(tuple([round(wall,precision), round(wall+2*sep, precision)]))
        wall = new_wall
    return arr

def addTelescope(df:pd.DataFrame, name, telescope_diameter, wavelength_range, resolution, throughput, precision=7):
    newdf = df.copy()
    
    newdf["Dayside Emitting Temperature [K]"] = newdf.apply(lambda x: Tday(x["Star Temperature [K]"], 
                                                                           x["Star Radius [Rs]"],
                                                                           x["Planet Semi-major Axis [au]"],
                                                                           x["Planet Albedo"],
                                                                           x["Heat Redistribution Factor"]),
                                                            axis=1)
    
    while round((wavelength_range[1] - wavelength_range[0]), precision) == 0:
        precision += 1
    arr = constructRanges(wavelength_range, resolution, precision=precision)
    
    # phase_curve = newdf.copy() ## To add when phase curve durations are determined
    # transit = newdf.copy() 
    # eclipse = newdf.copy()
    newdf["Transit Duration [hrs]"] = newdf["Transit Duration [hrs]"].fillna(newdf["Transit Duration [hrs]"].mean()) # replace each nan value with the mean value
    for w_range in arr:
        # newdf[f"Flux Ratio {w_range[0]}-{w_range[1]}um"] = newdf.apply(lambda x: fluxRatio(x["Planet Radius [Rjup]"],
        #                                                                                                 x["Star Radius [Rs]"],
        #                                                                                                 w_range,
        #                                                                                                 x["Dayside Emitting Temperature [K]"],
        #                                                                                                 x["Star Temperature [K]"]),
        #                                                                             axis=1)
        
        newdf[f"Noise Estimate {w_range[0]}-{w_range[1]}um"] = newdf.apply(lambda x: noiseEstimate(x["Star Temperature [K]"],
                                                                                                    *w_range,
                                                                                                    throughput, 
                                                                                                    x["Transit Duration [hrs]"]*3600,
                                                                                                    x["Star Radius [Rs]"],
                                                                                                    telescope_diameter,
                                                                                                    x["Star Distance [pc]"]),
                                                                            axis=1)
        
      
        

        # newdf[f"ESM Estimate {w_range[0]}-{w_range[1]}um"] = newdf.apply(lambda x: x[f"Flux Ratio {w_range[0]}-{w_range[1]}um"] / x[f"Noise Estimate {w_range[0]}-{w_range[1]}um"],
        #                                     axis=1)
    
    newdf.to_csv(f"Telescopes/{name}.csv")
    
def getDF(df):
    if type(df) == str:
        try:
            return pd.read_csv(df)
        except:
            raise Exception("Provided input is not valid. Ensure the dataframe or filename is spelled correctly.")
    return df
    
def getNoiseColumns(df):
    df = getDF(df)
    return [x for x in df if "Noise Estimate" in x]
    
def getNoiseEstimates(df):
    df = getDF(df)
    noise_columns = getNoiseColumns(df)
    return df.copy()[["Planet Name", *noise_columns]]

def getSubRange(column_name):
    arr = column_name.split()[-1].replace('um', '').split('-')
    return [float(x) for x in arr]

def getRange(df):
    df = getDF(df)
    columns = getNoiseColumns(df)
    return [getSubRange(columns[0])[0], getSubRange(columns[-1])[-1]]

def getNoise(df:pd.DataFrame, wavelength:float):
    df = getDF(df)
    for column in getNoiseColumns(df):
        w_range = getSubRange(column)
        if w_range[0] <= wavelength <= w_range[1]:
            return df.copy()[["Planet Name", column]]
    
    raise ValueError(f"Provided wavelength not in range for this telescope system. Range is {getRange(df)[0]} to {getRange(df)[1]} microns.")

def plotNoise(df, system_name=None, fill_between=False, ax=None, savepath=None):
    if system_name is None:
        raise ValueError("Please include a system_name for title.")
    
    df = getDF(df)
    
    if ax is None:
        fig, ax = plt.subplots()
        
    wavelengths = np.array([])
    stds = np.array([])
    means = np.array([])
    noise_columns = getNoiseColumns(df)
    for column in noise_columns:
        w_range = column.split()[-1].replace('um', '').split('-')
        
        wavelengths = np.append(wavelengths, round((float(w_range[1]) + float(w_range[0])) / 2, 3))
        stds = np.append(stds, df[column].std())
        means = np.append(means, df[column].mean())
        
    if fill_between:
        ax.fill_between(wavelengths, means-stds, means+stds, alpha=.3, zorder=3)
        ax.scatter(wavelengths, means, marker='.', color='blue', zorder=3)
    else:
        ax.errorbar(wavelengths, means, yerr=stds, fmt='o', c='black', capsize=3, zorder=3)
        
    ax.set_ylabel("Noise Estimate")
    ax.set_xlabel("Wavelength [microns]")
    
    ax.grid(which="major", alpha=.4, zorder=0)
    ax.grid(which="minor", alpha=.1, linestyle="-.", zorder=0)
    ax.minorticks_on()
    
    senstivity_range = getRange(df)
    title=f"Noise Estimates at Various Wavelengths\n{system_name}, {senstivity_range[0]}-{senstivity_range[1]} $\mu m$, R={len(noise_columns)})"
    ax.set_title(title)
    
    if savepath is not None:
        plt.savefig(savepath + "/" + title.replace("\n", " ").replace("$\mu m$", "microns") + ".png", bbox_inches='tight', dpi=300)