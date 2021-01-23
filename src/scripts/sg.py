#load common utilities
import os
path = os.path.abspath(os.curdir).replace('\\', '/')
from datetime import datetime
import glob

#load data analysis packages
import numpy as np
import pandas as pd

# data_path = '../../data'
data_path = '../../data'

cbg_pop = pd.read_csv(f"{data_path}/raw/census/data/cbg_b01.csv", usecols=['census_block_group','B01001e1'])
cbg_pop_dict = dict(zip(cbg_pop.iloc[:,0], cbg_pop.iloc[:,1]))

# pop_stats_dict = {
#     "B01001e1": "total_population",
#     "B01001e2": "total_population_male",
#     "B01001e26": "total_population_female",
#     "B01002Ae1": "pop_white",
#     "B01002Be1": "pop_black"
# }

# pop_stats = pd.read_csv(f"{data_path}/raw/census/data/cbg_b01.csv", dtype={"census_block_group": "object"}, usecols=['census_block_group'] + list(pop_stats_dict.keys()))\
# .rename(columns=pop_stats_dict).fillna(0)

def get_sg_data(poi_name, month):
    dtypes = {
    "naics_code" : "object",
    "postal_code": "object",
    "phone_number": "object",
    "poi_cbg": "object"
}
    #read in SafeGraph data, joined with additional datasets
    safegraph_df = pd.read_csv(f"{data_path}/raw/safegraph/{poi_name}/{month}/{month}.csv", dtype=dtypes).merge(
        pd.read_csv(f'{data_path}/raw/safegraph/{poi_name}/{month}/home_panel_summary.csv', usecols=['census_block_group', 'number_devices_residing'], dtype={"census_block_group": "object"}),
        left_on='poi_cbg', right_on='census_block_group', how='left'
    ).merge(
        pd.read_csv(f"{data_path}/raw/census/data/cbg_b01.csv", usecols=['census_block_group','B01001e1'], dtype={'census_block_group': 'object'}),
        on='census_block_group', how='left'
    ).rename(columns={"B01001e1":'cbg_pop'})
    
    return safegraph_df

def read_census_data(variable_dict):
    dfs = []
    
    data_sets = sorted(list(set([x[0:3].lower() for x in variable_dict])))
    
    for data_set in data_sets:
        dfs.append(pd.read_csv(f"{data_path}/raw/census/data/cbg_{data_set}.csv", usecols=["census_block_group"] + [x for x in list(variable_dict.keys()) if x[0:3].lower() == data_set]).set_index('census_block_group'))
    
    df = pd.concat(dfs, axis=1)
    df = df.rename(columns=variable_dict)
    
    return df

def read_census_data2(var_dict):
    flatten = lambda t: [item for sublist in t for item in sublist]
    var_list = flatten(list(var_dict.values()))
    data_sets = sorted(list(set([x[0:3].lower() for x in var_list])))
    
    dfs = []
    for data_set in data_sets:
        dfs.append(pd.read_csv(f"{data_path}/raw/census/data/cbg_{data_set}.csv", dtype={'census_block_group':"object"}, usecols=["census_block_group"] + [x for x in var_list if x[0:3].lower() == data_set])\
                  .set_index('census_block_group'))
    
    df = pd.concat(dfs, axis=1)
    for col in var_dict:
        df[col] = np.sum(df[var_dict[col]], axis=1)
    
    return df[list(var_dict.keys())]

def calc_median_age(brands):
    cbg_visits = pd.read_csv(f"{data_path}/processed/cbg_visits.csv", dtype={'census_block_group': "int64"})
    
    data = read_census_data({
        "B01002e2": "male_median_age",
        "B01002e3": "female_median_age"
    })
    
    dfs = []
    
    for brand in brands:
        df = cbg_visits.set_index("census_block_group")[f"visits_{brand}"].to_frame().merge(data, on='census_block_group', how='left').fillna(0)
        df = df[df[f"visits_{brand}"] > 0]
        
        df = df[['male_median_age','female_median_age']].median().to_frame().T
        df['brand'] = brand
        dfs.append(df)
        
    
    return pd.concat(dfs)[['brand', 'male_median_age', 'female_median_age']]

def calc_gender(brands):
    cbg_visits = pd.read_csv(f"{data_path}/processed/cbg_visits.csv", dtype={'census_block_group': "int64"})

    pop_stats = read_census_data({
        "B01001e1": "total_population",
        "B01001e2": "total_population_male",
        "B01001e26": "total_population_female"
    })
    
    dfs = []
    for brand in brands:
        
        df = cbg_visits.set_index("census_block_group")[f"visits_{brand}"].to_frame().merge(pop_stats, on='census_block_group', how='left').fillna(0)
        df = df[df['total_population'] > 0]

        df['percent_male'] = df.apply(lambda x: x.total_population_male / x.total_population, axis=1)
        df['percent_female'] = df.apply(lambda x: x.total_population_female / x.total_population, axis=1)
        df['est_male'] = df[f"visits_{brand}"] * df['percent_male']
        df['est_female'] = df[f"visits_{brand}"] * df['percent_female']

        df = df[['est_male', 'est_female']].sum().to_frame().T
        df['brand'] = brand
        dfs.append(df)
    
    
    return pd.concat(dfs)[['brand', 'est_male', 'est_female']]

def calc_race(brands):
    cbg_visits = pd.read_csv(f"{data_path}/processed/cbg_visits.csv", dtype={'census_block_group': "int64"})
    
    data = read_census_data({
        "B01001e1": "total_population",
        "B02001e2": "pop_white",
        "B02001e3": "pop_black",
        "B02001e5": "pop_asian"
    })
    
    dfs = []
    
    for brand in brands:
        
        df = cbg_visits.set_index("census_block_group")[f"visits_{brand}"].to_frame().merge(data, on='census_block_group', how='left').fillna(0)
        df = df[df['total_population'] > 0]
    
   
        df['percent_black'] = df.apply(lambda x: x.pop_black / x.total_population, axis=1)
        df['percent_white'] = df.apply(lambda x: x.pop_white / x.total_population, axis=1)
        df['percent_asian'] = df.apply(lambda x: x.pop_asian / x.total_population, axis=1)
        df['percent_other'] = df.apply(lambda x: 1 - (x.percent_black + x.percent_white + x.percent_asian), axis=1)

        df['est_black'] = df[f'visits_{brand}'] * df['percent_black']
        df['est_white'] = df[f'visits_{brand}'] * df['percent_white']
        df['est_asian'] = df[f'visits_{brand}'] * df['percent_asian']
        df['est_other'] = df[f'visits_{brand}'] * df['percent_other']
    
        df = df[['est_white', 'est_black', 'est_asian', 'est_other']].sum().to_frame().T
        df['brand'] = brand
        dfs.append(df)
    
    return pd.concat(dfs)[['brand', 'est_white', 'est_black', 'est_asian', 'est_other']]

def calc_age(brands):
    cbg_visits = pd.read_csv(f"{data_path}/processed/cbg_visits.csv", dtype={'census_block_group': "object"})
    
    age_dict = {
        "total_population": ["B01001e1"],
        "total_population_male": ["B01001e2"],
        "total_population_female": ["B01001e26"],
        "male_20_29": ["B01001e8", "B01001e9", "B01001e10","B01001e11"],
        "male_30_39": ["B01001e12","B01001e13"],
        "male_40_49": ["B01001e14", "B01001e15"],
        "male_50_59": ["B01001e16","B01001e17"],
        "male_60_69": ["B01001e18", "B01001e19", "B01001e20", "B01001e21"],
        "male_70+": ["B01001e22", "B01001e23", "B01001e24", "B01001e25"],
        'female_20_29': ["B01001e32", "B01001e33", "B01001e34","B01001e35"],
        'female_30_39': ["B01001e36", "B01001e37"],
        'female_40_49': ["B01001e38", "B01001e39"],
        'female_50_59': ["B01001e40", "B01001e41"],
        'female_60_69': ["B01001e42", "B01001e43","B01001e44", "B01001e45"],
        'female_70+': ["B01001e46", "B01001e47", "B01001e48", "B01001e49"]
    }
    
    data = read_census_data2(age_dict)
    
    dfs=[]
    
    for brand in brands:
        
        df = cbg_visits.set_index("census_block_group")[f"visits_{brand}"].to_frame().merge(data, on='census_block_group', how='left').fillna(0)
        df = df[df['total_population'] > 0]
        
        
        df['sum_20_29'] = df[['male_20_29', 'female_20_29']].sum(axis=1)
        df['sum_30_39'] = df[['male_30_39', 'female_30_39']].sum(axis=1)
        df['sum_40_49'] = df[['male_40_49', 'female_40_49']].sum(axis=1)
        df['sum_50_59'] = df[['male_50_59', 'female_50_59']].sum(axis=1)
        df['sum_60_69'] = df[['male_60_69', 'female_60_69']].sum(axis=1)
        df['sum_70+'] = df[['male_70+', 'female_70+']].sum(axis=1)
        
        df['percent_20_29'] = df.apply(lambda x: x.sum_20_29 / x.total_population, axis=1)
        df['percent_30_39'] = df.apply(lambda x: x.sum_30_39 / x.total_population, axis=1)
        df['percent_40_49'] = df.apply(lambda x: x.sum_40_49 / x.total_population, axis=1)
        df['percent_50_59'] = df.apply(lambda x: x.sum_50_59 / x.total_population, axis=1)
        df['percent_60_69'] = df.apply(lambda x: x.sum_60_69 / x.total_population, axis=1)
        df['percent_70+'] = df.apply(lambda x: x['sum_70+'] / x.total_population, axis=1)
        
        df['est_20_29'] = df[f'visits_{brand}'] * df['percent_20_29']
        df['est_30_39'] = df[f'visits_{brand}'] * df['percent_30_39']
        df['est_40_49'] = df[f'visits_{brand}'] * df['percent_40_49']
        df['est_50_59'] = df[f'visits_{brand}'] * df['percent_50_59']
        df['est_60_69'] = df[f'visits_{brand}'] * df['percent_60_69']
        df['est_70+'] = df[f'visits_{brand}'] * df['percent_70+']
        
        df = df[['est_20_29', 'est_30_39', 'est_40_49', 'est_50_59', 'est_60_69', 'est_70+']].sum().to_frame().T
        df['brand'] = brand
        dfs.append(df)
    
    return pd.concat(dfs)[['brand', 'est_20_29', 'est_30_39', 'est_40_49', 'est_50_59', 'est_60_69', 'est_70+']]



def calc_visits_by_day(record):
    strptime = datetime.strptime
    dateformat = '%Y-%m-%d'
    
    r = record
    
    startdate = strptime(r.date_range_start[0:10], dateformat)
    enddate = strptime(r.date_range_end[0:10], dateformat)
    date_range = pd.date_range(startdate, enddate)[:-1]
    
    visits = eval(r.visits_by_day)
    day_counts = dict(zip([*range(1, len(visits) + 1)], visits))
    
    df = pd.DataFrame(index=date_range, data={"id": r.safegraph_place_id, "visits": visits})
    return df


def calc_true_visits_by_day(record):
    r = record
    visits_by_day = calc_visits_by_day(r)
    
    visits_by_cbg = eval(r.visitor_home_cbgs)
    
    df = pd.DataFrame(data={
        "id": r.safegraph_place_id,
        "raw_visit_counts": r.raw_visit_counts,
            "raw_visitor_counts": r.raw_visitor_counts,
        "origin_cbg": visits_by_cbg.keys(),
        "visits_from_cbg": visits_by_cbg.values(),
        "sample_size": r.number_devices_residing
    })
    
    df['origin_cbg'] = df['origin_cbg'].astype('int64')
    df['est_visits_per_visitor'] = df['raw_visit_counts'] / df['raw_visitor_counts']
    df['cbg_pop'] = df['origin_cbg'].map(cbg_pop_dict)
    df['scaling_factor'] = df['cbg_pop'] / df['sample_size']
    df['extr_visitors'] = df['scaling_factor'] * df['visits_from_cbg']
    df['extr_visits'] = df['extr_visitors'] * df['est_visits_per_visitor']
    
    true_visits_estimate_total = df['extr_visits'].sum()
    true_visits_estimate_total
    
    df2 = pd.DataFrame(data={"visits_by_day": list(calc_visits_by_day(r).visits)})
    df2['raw_visit_counts'] = r.raw_visit_counts
    df2['fraction_raw_visits_by_day'] = df2['visits_by_day'] / df2['raw_visit_counts']
    df2['true_visits_estimate_total'] = true_visits_estimate_total
    df2['true_visits_by_day'] = df2['fraction_raw_visits_by_day'] * df2['true_visits_estimate_total']
    
    true_visit_dict = dict(zip(df2['visits_by_day'].values, df2['true_visits_by_day'].values))
    
    visits_by_day['true_visits'] = visits_by_day['visits'].map(true_visit_dict)

    
    return visits_by_day





