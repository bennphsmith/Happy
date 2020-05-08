# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np


# %%
# Read in the Happiness CSV files
happy16 = pd.read_csv('2016.csv')
happy18 = pd.read_csv('2018.csv')


# %%
# Create new tables out of the relvant colums from the database
newHappy16 =  happy16[['Country', 'Region', 'Happiness Score']].copy()
newHappy18 =  happy18[['Country or region', 'Score']].copy()
newHappy18.columns = ['Country', 'Happiness Score'] # Change column names to make them consistent
newHappy18 = pd.merge(newHappy18, newHappy16[['Country', 'Region']], on=['Country'], how='left') # Merge the regional information from 16 to 18
newHappy18 = newHappy18[['Country', 'Region', 'Happiness Score']] # Reorder columns
print(newHappy16.head())
print(newHappy18.head())

# Check for nulls
print(newHappy16.isnull().sum(axis = 0))
print(newHappy18.isnull().sum(axis = 0))


# %%
# Find and clean missing values for Region
print(set(newHappy18['Country']) - set(newHappy16['Country'])) # Get Set of missing values
print(set(newHappy16['Region'])) # Get set of possible regions

# Assign values based on most plausible region
newHappy18.loc[newHappy18['Country'] == 'Northern Cyprus', ['Region']] = 'Middle East and Northern Africa'
newHappy18.loc[newHappy18['Country'] == 'Lesotho', ['Region']] = 'Sub-Saharan Africa'
newHappy18.loc[newHappy18['Country'] == 'Trinidad & Tobago', ['Region']] = 'Latin America and Caribbean'
newHappy18.loc[newHappy18['Country'] == 'Central African Republic', ['Region']] = 'Sub-Saharan Africa'
newHappy18.loc[newHappy18['Country'] == 'Mozambique', ['Region']] = 'Sub-Saharan Africa'

# Check table there is now no missing values
print(newHappy18.isnull().sum(axis = 0))


# %%
# Check table out put matches and it is as expected
print(newHappy16)
print(newHappy18)

# Export tables to csv files for easy reuse
newHappy16.to_csv('Happiness Scores 16.csv')
newHappy18.to_csv('Happiness Scores 18.csv')

