import pandas as pd
import numpy as np
import csv
# master = pd.read_csv("/home/gianthk/Data/BEATS/IH/scratch/master.csv", header=[0], index_col=[1])
master = pd.read_csv("/home/gianthk/Data/BEATS/IH/scratch/master.csv")

COR = 45
pad = True
alpha = 0.0002


# update master when button is pushed

# check if scan is already in master
if np.any(master['scan'].isin([filename])):

    # check if already reconstructed
    if master.loc[master["scan"] == filename, "reconstructed"][0]:

        # if already reconstructed create a new line
        newline = master.loc[master["scan"] == filename]

        # if multiple rows exist for 1 scan take the first one
        if len(newline) > 1:
            newline = newline.loc[[0]]

        # newline["reconstructed"] = False
        newline["cor"] = COR
        newline["pad"] = pad
        newline["alpha"] = alpha
        master = pd.concat([master, newline])
    else:
        master.loc[master["scan"] == filename, "cor"] = COR
        master.loc[master["scan"] == filename, "pad"] = pad
        master.loc[master["scan"] == filename, "alpha"] = alpha

        # master.loc[master["scan"] == filename, "reconstructed"] = True

else:
    master.loc[len(master), ["scan", "cor", "pad", "alpha"]] = [filename, COR, pad, alpha]



master.to_csv("/home/gianthk/Data/BEATS/IH/scratch/master.csv", index=False)


# launch recon script on Rum


# launch watchdog on reconstruction



