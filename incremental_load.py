import census
import us
import civis
from datetime import datetime

# get date of most recent data from table
max_year = civis.io.read_civis_sql('select max(year) from scratch.census_commute', 'Civis Database')[1][0]

# see if newer data available via client
new_year = int(max_year) + 1
try:
    c.acs5.state('NAME', us.states.DC.fips, year=new_year)
except UnsupportedYearException:
    print("No newer data available")

# if new data available, get it!
print("Getting new data")
data_all = []
for state in us.STATES:
    data_all.extend(c.acs5.state_county_tract(fields, state.fips, Census.ALL, Census.ALL))
 
# load to dataframe
df = pd.DataFrame(data_all)  

# add year column
df['year'] = new_year

# append new data to existing Civis table
print("Loading new data to Redshift")
civis.io.dataframe_to_civis(df, 'Civis Database', 'scratch.census_commute', 
                            existing_table_rows='append').result()
