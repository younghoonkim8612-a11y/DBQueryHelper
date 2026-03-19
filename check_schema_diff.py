import db_helper
helper = db_helper.QueryHelper('LukasPostgres')

query_jed = "SELECT table_name, column_name, character_maximum_length FROM information_schema.columns WHERE table_schema = 'gisdb_JED' AND data_type LIKE '%character%';"
df_jed = helper.execute_query(query_jed)

query_target = "SELECT table_name, column_name, character_maximum_length FROM information_schema.columns WHERE table_schema = 'gisdb' AND data_type LIKE '%character%';"
df_target = helper.execute_query(query_target)

mismatches = []
for _, row in df_jed.iterrows():
    target_row = df_target[(df_target['table_name'] == row['table_name']) & (df_target['column_name'] == row['column_name'])]
    if not target_row.empty:
        target_len = target_row.iloc[0]['character_maximum_length']
        if row['character_maximum_length'] != target_len:
            mismatches.append(f"{row['table_name']}.{row['column_name']}: JED={row['character_maximum_length']}, gisdb={target_len}")

if mismatches:
    print('Length Mismatches found:')
    for m in mismatches:
        print(m)
else:
    print('No length mismatches between gisdb_JED and gisdb schemas for character columns.')
