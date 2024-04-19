import pandas as pd

def preprocess_summer_olympics(data, regions):
    data.drop_duplicates(inplace=True)
    merged_data = data.merge(regions, how='left', on='NOC')
    summer_data = merged_data[merged_data['Season'] == 'Summer']
    summer_data = pd.concat([summer_data, pd.get_dummies(summer_data['Medal'])], axis=1)

    return summer_data

def preprocess_winter_olympics(data, regions):
    data.drop_duplicates(inplace=True)
    merged_data = data.merge(regions, how='left', on='NOC')
    winter_data = merged_data[merged_data['Season'] == 'Winter']
    winter_data = pd.concat([winter_data, pd.get_dummies(winter_data['Medal'])], axis=1)

    return winter_data