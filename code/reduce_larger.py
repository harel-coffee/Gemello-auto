# NEED TO RUN ON CLUSTER
import sys
CLUSTER=True
if CLUSTER:
    sys.path.insert(0, '/if6/nb2cz/anaconda/lib/python2.7/site-packages')

import  os

import numpy as np
import pandas as pd


from create_df_larger import read_df_larger
df, dfc, all_homes, appliance_min, national_average = read_df_larger()

df = df.rename(columns={'house_num_rooms':'num_rooms',
                        'num_occupants':'total_occupants',
                        'difference_ratio_min_max':'ratio_difference_min_max'})

from all_functions import *
from features_larger import *

import sys

from sklearn.neighbors import KNeighborsRegressor
from sklearn.cross_validation import ShuffleSplit
from sklearn.cross_validation import LeaveOneOut

NUM_NEIGHBOUR_MAX = 6
F_MAX = 6

import json
APPLIANCES=["hvac"]
out_path = os.path.expanduser("~/main-out-new-larger/")
for feature in ["Static"]:
    for appliance in APPLIANCES:
        if appliance =="hvac":
            month_start, month_end = 5, 11
        else:
            month_start, month_end = 1, 13
        for home in all_homes[appliance][:2]:
            pred_df = pd.read_csv(out_path+"%s_%s_%d.csv" %(appliance, feature, home))
            gt_df = df.ix[home][["%s_%d" %(appliance,month) for month in range(month_start, month_end)]]
"""

    #gt_df = pd.DataFrame(gt_test)
    #print pred_df, gt_df
    #error = (gt_df-pred_df).abs().div(gt_df).mul(100)
    #print error
    #accuracy_test = 100-error
    #accuracy_test[accuracy_test<0]=0

    #return accuracy_test.squeeze()
    return pred_df



import sys
appliance, feature, home = sys.argv[1], sys.argv[2], sys.argv[3]
home = int(home)

out_df = _find_accuracy(home, appliance, feature)
out_df.to_csv(os.path.expanduser("~/main-out-new-larger/%s_%s_%d.csv" %(appliance, feature, home)))
#_save_csv(out_df, "../main-out", appliance, feature)
"""