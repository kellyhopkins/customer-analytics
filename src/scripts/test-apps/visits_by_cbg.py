visits_by_cbg = eval(store.visitor_home_cbgs)
df = pd.DataFrame(data={
    "id": store.safegraph_place_id,
    "raw_visit_counts": store.raw_visit_counts,
    "raw_visitor_counts": store.raw_visitor_counts,
    "origin_cbg": visits_by_cbg.keys(),
    "visits_from_cbg": visits_by_cbg.values(),
    "sample_size": store.number_devices_residing
})
df['origin_cbg'] = df['origin_cbg'].astype('int64')
df['est_visits_per_visitor'] = df['raw_visit_counts'] / df['raw_visitor_counts']
df['cbg_pop'] = df['origin_cbg'].map(cbg_pop_dict)
df['scaling_factor'] = df['cbg_pop'] / df['sample_size']
df['extr_visitors'] = df['scaling_factor'] * df['visits_from_cbg']
df['extr_visits'] = df['extr_visitors'] * df['est_visits_per_visitor']

true_visits_estimate_total = df['extr_visits'].sum()
true_visits_estimate_total


df2 = pd.DataFrame(data={"visits_by_day": list(visits_by_day(store).visits)})
df2['raw_visit_counts'] = store.raw_visit_counts
df2['fraction_raw_visits_by_day'] = df2['visits_by_day'] / df2['raw_visit_counts']
df2['true_visits_estimate_total'] = true_visits_estimate_total
df2['true_visits_by_day'] = df2['fraction_raw_visits_by_day'] * df2['true_visits_estimate_total']

# df2 = df['raw_visit_counts'].to_frame()
# df2['visits_by_day'] = list(visits_by_day(store).visits)
# df2['fraction_raw_visits'] = df2['raw_visit_counts'] / df['extr_visits']
# df2['true_visits_estimate_total'] = true_visits_estimate_total
# df2['true_visits_by_day'] = df2['fraction_raw_visits'] * df2['true_visits_estimate_total']
df2

true_visit_dict = dict(zip(df2['visits_by_day'].values, df2['true_visits_by_day'].values))

dfs = []
for i,store in safegraph.iterrows():
    try:
        dfs.append(sg.calc_visits_by_day(store))
    except:
        pass

pd.concat(dfs)