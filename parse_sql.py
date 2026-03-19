import re
import pandas as pd
import db_helper

helper = db_helper.QueryHelper('LukasPostgres')

# Get all character columns in gisdb_JED with their max lengths
query = '''
SELECT table_name, column_name, character_maximum_length
FROM information_schema.columns
WHERE table_schema = 'gisdb_JED' AND data_type LIKE '%character%' AND character_maximum_length IS NOT NULL;
'''
df = helper.execute_query(query)

schema_limits = {}
for _, row in df.iterrows():
    if row['table_name'] not in schema_limits:
        schema_limits[row['table_name']] = {}
    schema_limits[row['table_name']][row['column_name']] = row['character_maximum_length']

with open('Generated Files/2026-03-09/JED GIS Insert Script/migrate_gisdb_data.sql', 'r', encoding='utf-8') as f:
    sql_content = f.read()

# Find all insert statements
insert_matches = list(re.finditer(r'INSERT INTO gisdb\.([a-zA-Z0-9_]+) \((.*?)\)\nVALUES\n(.*?)(\n;|\n\n--)', sql_content, re.DOTALL))

for match in insert_matches:
    table_name = match.group(1)
    if table_name not in schema_limits:
        continue
        
    columns = [c.strip() for c in match.group(2).split(',')]
    values_str = match.group(3)
    
    # Simple split by "),\n  ("
    rows_str = values_str.strip()[1:-1] # remove first ( and last )
    rows = rows_str.split('),\n  (')
    
    for i, row in enumerate(rows):
        # Very brittle split, assuming no commas inside strings for now since these are mostly simple gis files
        vals = [v.strip() for v in row.split(',')]
        
        # Check lengths
        for col_idx, col_name in enumerate(columns):
            if col_idx < len(vals) and col_name in schema_limits[table_name]:
                max_len = schema_limits[table_name][col_name]
                val = vals[col_idx].strip("'")
                if val != 'NULL' and len(val) > max_len:
                    print(f"Length violation in {table_name}.{col_name} (max {max_len}): length={len(val)}, value='{val}' at row {i}")
