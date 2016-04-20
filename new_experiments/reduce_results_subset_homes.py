import pandas as pd
import numpy as np
import pickle

#train_region = "Austin"
#test_region = "SanDiego"
import sys

train_region, test_region = sys.argv[1:]
out_overall = pickle.load(open('../data/input/all_regions.pkl','r'))

train_df = out_overall[train_region]
test_df = out_overall[test_region]
#APPLIANCES=["dw",'hvac','fridge','wm','mw','ec','wh','oven']
APPLIANCES=['hvac','fridge','wm']

from regional_average_contribution import  contribution as contri

k=3
if train_region!=test_region:
    TRANSFORMATIONS = ["None","DD","DD-percentage","median-aggregate-percentage",
                      "median-aggregate",'regional','regional-percentage']
else:
    TRANSFORMATIONS = ["None"]#transformations = ['DD','None',"DD-fridge"]
count_absent = {}
#transformations = ["None"]

out = {}
for num_homes in range(5, 40, 5):
    out[num_homes] = {}
    for transform in TRANSFORMATIONS:
        count_absent[transform] = {}
        out[num_homes][transform] = {}
        #for appliance in ["hvac","fridge","dr","wm"]:
        for appliance in APPLIANCES:
            count_absent[transform][appliance] = 0
            out[num_homes][transform][appliance] = {}
            for month in range(1,13):
                print appliance, month, transform
                out[num_homes][transform][appliance][month] = []
                for test_home in test_df.index:
                    try:
                        pred =  pickle.load(open('../../../output/output/ineq_cross_subset/%s_%s_%s_%s_%d_%d_%d.pkl' %(
                                                                                                    num_homes,
                                                                                                    train_region,
                                                                                                   test_region,
                                                                                                   transform,
                                                                                                   appliance,
                                                                                                   month,
                                                                                                   test_home,
                                                                                                   k),'r'))
                        gt = test_df.ix[test_home]['%s_%d' %(appliance, month)]

                        error = np.abs(gt-pred)
                        percentage_error = error*100/gt
                        if percentage_error>100:
                            percentage_error=100
                        percentage_accuracy = 100-percentage_error
                        out[num_homes][transform][appliance][month].append(percentage_accuracy)
                    except Exception, e:
                        count_absent[transform][appliance]+= 1

#acc = {tr:{} for tr in transformations}
acc = {}
acc['Regional average']={}

for num_homes in range(5, 40, 5):
    acc[num_homes] = {}
    for transform in TRANSFORMATIONS:
        acc[num_homes][transform] = {}
        for appliance in APPLIANCES:
        #for appliance in ["hvac"]:
            acc[num_homes][transform][appliance] = {}
            for month in range(1,13):
                acc[num_homes][transform][appliance][month] = pd.Series(out[transform][appliance][month]).mean()



for appliance in APPLIANCES:
    acc['Regional average'][appliance] = {}
    for month in range(1,13):
        acc['Regional average'][appliance][month] = []
        for test_home in test_df.index:
            try:
                if month in range(3, 11):
                    pred = test_df.ix[test_home]['aggregate_%d' %month]*contri[test_region]['Cooling'][appliance]
                else:
                    pred = test_df.ix[test_home]['aggregate_%d' %month]*contri[test_region]['Heating'][appliance]
                gt = test_df.ix[test_home]['%s_%d' %(appliance, month)]
                error = np.abs(gt-pred)
                percentage_error = error*100/gt
                if percentage_error>100:
                    percentage_error=100
                percentage_accuracy = 100-percentage_error
                acc['Regional average'][appliance][month].append(percentage_accuracy)
            except Exception, e:
                print e

        acc['Regional average'][appliance][month] = pd.Series(acc['Regional average'][appliance][month]).mean()


