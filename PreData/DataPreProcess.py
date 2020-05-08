# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np


# %%
########Begin Pre Processing the Happiness Scores CSV#########
# Read in the Happiness CSV files
happy_16 = pd.read_csv('2016.csv')
happy_18 = pd.read_csv('2018.csv')


# %%
# Create new tables out of the relvant colums from the database
Happy16 =  happy_16[['Country', 'Region', 'Happiness Score']].copy()
Happy18 =  happy_18[['Country or region', 'Score']].copy()
Happy18.columns = ['Country', 'Happiness Score'] # Change column names to make them consistent
Happy18 = pd.merge(Happy18, Happy16[['Country', 'Region']], on=['Country'], how='left') # Merge the regional information from 16 to 18
Happy18 = Happy18[['Country', 'Region', 'Happiness Score']] # Reorder columns
print(Happy16.head())
print(Happy18.head())

# Check for nulls
print(Happy16.isnull().sum(axis = 0))
print(Happy18.isnull().sum(axis = 0))


# %%
# Find and clean missing values for Region
print(set(Happy18['Country']) - set(Happy16['Country'])) # Get Set of missing values
print(set(Happy16['Region'])) # Get set of possible regions

# Match different spellings of country name
Happy16['Country'].replace('North Cyprus', 'Cyprus', inplace=True)
Happy18['Country'].replace('Northern Cyprus', 'Cyprus', inplace=True)
Happy18['Country'].replace('Trinidad & Tobago', 'Trinidad and Tobago', inplace=True)

# Assign values based on most plausible region
Happy18.loc[Happy18['Country'] == 'Cyprus', ['Region']] = 'Middle East and Northern Africa'
Happy18.loc[Happy18['Country'] == 'Trinidad and Tobago', ['Region']] = 'Latin America and Caribbean'
Happy18.loc[Happy18['Country'] == 'Lesotho', ['Region']] = 'Sub-Saharan Africa'
Happy18.loc[Happy18['Country'] == 'Central African Republic', ['Region']] = 'Sub-Saharan Africa'
Happy18.loc[Happy18['Country'] == 'Mozambique', ['Region']] = 'Sub-Saharan Africa'

# Check table there is now no missing values
print(Happy18.isnull().sum(axis = 0))


# %%
# Check table out put matches and it is as expected
print(Happy16)
print(Happy18)

# Export tables to csv files for easy reuse
Happy16.to_csv('HappinessScores16.csv')
Happy18.to_csv('HappinessScores18.csv')


# %%
########Begin Pre Processing the GDP pre Capita Scores CSV#########

# Read and format csv file
gdpCap = pd.read_csv('gdpCap.csv')
newGDP =  gdpCap[['Country Name', '2016', '2018']].copy()
newGDP.columns = ['Country', 'gdpCap16', 'gdpCap18'] # Change column names to make them consistent

# Check country name discrepancies
print(set(Happy16['Country']) - set(newGDP['Country']))
print(set(Happy18['Country']) - set(newGDP['Country']))

# Map country names to Happiness Score Country names where possible
newGDP['Country'].replace('Congo, Rep.', 'Congo (Brazzaville)', inplace=True)
newGDP['Country'].replace('North Macedonia', 'Macedonia', inplace=True)
newGDP['Country'].replace('Yemen, Rep.', 'Yemen', inplace=True)
newGDP['Country'].replace('Slovak Republic', 'Slovakia', inplace=True)
newGDP['Country'].replace("Cote d'Ivoire", 'Ivory Coast', inplace=True)
newGDP['Country'].replace('Kyrgyz Republic', 'Kyrgyzstan', inplace=True)
newGDP['Country'].replace('Hong Kong SAR, China',  'Hong Kong', inplace=True)
newGDP['Country'].replace('Venezuela, RB', 'Russia', inplace=True)
newGDP['Country'].replace('Congo, Dem. Rep.', 'Congo (Kinshasa)', inplace=True)
newGDP['Country'].replace('Korea, Rep.', 'South Korea', inplace=True)
newGDP['Country'].replace('Syrian Arab Republic', 'Syria', inplace=True)
newGDP['Country'].replace('Lao PDR', 'Laos', inplace=True)
newGDP['Country'].replace('Egypt, Arab Rep.', 'Egypt', inplace=True)
newGDP['Country'].replace('Cyprus', 'North Cyprus', inplace=True)
newGDP['Country'].replace('Russian Federation', 'Russia', inplace=True)

# Check Country names have updated correctly
print(set(Happy16['Country']) - set(newGDP['Country']))
print(set(Happy18['Country']) - set(newGDP['Country']))

# Copy newGDP table to CSV
newGDP.to_csv('GDP.csv')


# %%
# Perform inner join merge between newGDP and Happiness table to drop any remaining outstanding values
gdpHappy16 = pd.merge(Happy16, newGDP[['Country', 'gdpCap16']], on=['Country'], how='inner')
gdpHappy18 = pd.merge(Happy18, newGDP[['Country', 'gdpCap18']], on=['Country'], how='inner')

# Check table output as expected
#print(gdpHappy16)
#print(gdpHappy18)

# Print nulls
print(gdpHappy16[gdpHappy16.isna().any(axis=1)])
print(gdpHappy18[gdpHappy18.isna().any(axis=1)])

# Drop null rows
gdpHappy16 = gdpHappy16.dropna()
gdpHappy18 = gdpHappy18.dropna()

# Check for nulls
print(gdpHappy16.isnull().sum(axis = 0))
print(gdpHappy18.isnull().sum(axis = 0))


# %%
########Begin Pre Processing the EPI Scores CSV#########
epi16 = pd.read_csv('EPI 2016 Scores.csv')
epi18 = pd.read_csv('EPI 2018 Scores.csv')

# Identify null values in the Data to choose which columns to drop
#print(epi16.isnull().sum(axis=0))
#print(epi18.isnull().sum(axis=0))

# Average data between AIR.current and APE.current as EH - Air Quality encompasses both
epi18['AIRQ.current'] = epi18[['AIR.current', 'APE.current']].mean(axis=1)

# Extract useful Data to new table
Epi16 =  epi16[['Country', 'EH - Air Quality', 'EV - Biodiversity and Habitat', 'EH - Water and Sanitation', 'EV - Water Resources']].copy()
Epi18 =  epi18[['country', 'AIRQ.current', 'BDH.current', 'H2O.current', 'WRS.current']].copy()

# Rename table column headers for consistency
Epi16.columns = ['Country', 'Air Quality', 'Biodiversity', 'Water Sanitation', 'Water Resource']
Epi18.columns = ['Country', 'Air Quality', 'Biodiversity', 'Water Sanitation', 'Water Resource']

'''
# Check averages and standard deviation of column values to confirm the scoring is broadly similar year to year for columns data
# This has also been verified through the metadata for each report
#print(Epi16.std(axis = 0, skipna = True) - Epi18.std(axis = 0, skipna = True))
print(Epi16.std(axis = 0, skipna = True))
print(Epi18.std(axis = 0, skipna = True))

#print(Epi16.mean(axis = 0, skipna = True) - Epi18.mean(axis = 0, skipna = True))
print(Epi16.mean(axis = 0, skipna = True))
print(Epi18.mean(axis = 0, skipna = True))

# Check for nulls
print((Epi16 == 0).sum(axis = 0))
print((Epi18 == 0).sum(axis = 0))
'''
# Compare country sets to match up countries
print(set(gdpHappy16['Country']) - set(Epi16['Country']))
print(set(gdpHappy18['Country']) - set(Epi18['Country']))

# Map countries on the EPI16 reports
Epi16['Country'].replace('Congo', 'Congo (Brazzaville)', inplace=True)
Epi16['Country'].replace('Viet Nam', 'Vietnam', inplace=True)
Epi16['Country'].replace('United States of America', 'United States', inplace=True)
Epi16['Country'].replace("Cote d'Ivoire", 'Ivory Coast', inplace=True)
Epi16['Country'].replace('Dem. Rep. Congo', 'Congo (Kinshasa)', inplace=True)
Epi16['Country'].replace('Kyrgyz Republic', 'Kyrgyzstan', inplace=True)

# Map countries on the EPI18 reports
Epi18['Country'].replace('Republic of Congo', 'Congo (Brazzaville)', inplace=True)
Epi18['Country'].replace('Viet Nam', 'Vietnam', inplace=True)
Epi18['Country'].replace('United States of America', 'United States', inplace=True)
Epi18['Country'].replace('Dem. Rep. Congo', 'Congo (Kinshasa)', inplace=True)
Epi18['Country'].replace('Kyrgyz Republic', 'Kyrgyzstan', inplace=True)

# Compare country sets to match up countries
print(set(gdpHappy16['Country']) - set(Epi16['Country']))
print(set(gdpHappy18['Country']) - set(Epi18['Country']))




# %%
# Perform inner merge to add EPI data to Happiness scores
gdpEpiHappy16 = pd.merge(gdpHappy16, Epi16, on=['Country'], how='inner')
gdpEpiHappy18 = pd.merge(gdpHappy18, Epi18, on=['Country'], how='inner')
'''
# Check for null values
print(gdpEpiHappy16.isnull().sum(axis = 0))
print(gdpEpiHappy18.isnull().sum(axis = 0))
'''
# Print to check tables
print(gdpEpiHappy16)
print(gdpEpiHappy18)

# Convert to csv
gdpEpiHappy16.to_csv('test16.csv')
gdpEpiHappy18.to_csv('test18.csv')


# %%
#########Add CO2 data##########
# Measured in tons of CO2 per capita
# Data got from https://knoema.com/atlas/ranks/CO2-emissions-per-capita?action=export&gadget=tranking-container
# Extra values input manually from https://knoema.com/EDGARED2019/global-ghg-and-co2-emissions?location=1000500&indicator=1000070&type=1000140&utm_source=datafinder&utm_medium=excel&utm_campaign=sourcelink&frequency=A&lastUpdated=1585308536760#
co2 = pd.read_csv('CO2data.csv')
co2Data =  co2[['Location', '2016', '2018']].copy()

# Map countries
co2Data['Location'].replace('Congo', 'Congo (Brazzaville)', inplace=True)
co2Data['Location'].replace('Democratic Republic of the Congo', 'Congo (Kinshasa)', inplace=True)
co2Data['Location'].replace('Myanmar/Burma', 'Myanmar', inplace=True)
co2Data['Location'].replace('North Macedonia', 'Macedonia', inplace=True)

# Check unmapped countries
print(set(gdpEpiHappy16['Country']) - set(co2Data['Location']))
print(set(gdpEpiHappy18['Country']) - set(co2Data['Location']))

# Change column names
co2Data.columns = ['Country', '2016', '2018']

# Covert final table to csv format
print(co2Data)
co2Data.to_csv('test16.csv')


# %%
########Complete final merge to make total data set##########
final16= pd.merge(gdpEpiHappy16, co2Data[['Country', '2016']], on=['Country'], how='inner')
final18= pd.merge(gdpEpiHappy18, co2Data[['Country', '2018']], on=['Country'], how='inner')

# Final table format
final16 = final16.reindex(columns=['Country', 'Region', 'gdpCap16', 'Air Quality', 'Biodiversity', '2016', 'Water Sanitation', 'Water Resource', 'Happiness Score'])
final18 = final18.reindex(columns=['Country', 'Region', 'gdpCap18', 'Air Quality', 'Biodiversity', '2018', 'Water Sanitation', 'Water Resource', 'Happiness Score'])
final16.columns = ['Country', 'Region', 'GDP per Capita', 'Air Quality', 'Biodiversity', 'CO2 per Capita', 'Water Sanitation', 'Water Resource', 'Happiness Score']
final18.columns = ['Country', 'Region', 'GDP per Capita', 'Air Quality', 'Biodiversity', 'CO2 per Capita', 'Water Sanitation', 'Water Resource', 'Happiness Score']

# Too many 0 values in the Water Resource column so needs to be deleted
final16 = final16.drop(['Water Resource'], axis=1)
final18 = final18.drop(['Water Resource'], axis=1)

# Check for nulls
print(final16.isnull().sum(axis = 0))
print(final18.isnull().sum(axis = 0))

# Export to csv
final16.to_csv('final16.csv')
final18.to_csv('final18.csv')

