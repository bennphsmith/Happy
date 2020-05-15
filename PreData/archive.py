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

'''
normal16 = final16.copy()
normal18 = final18.copy()

# Normalise data uing boxcox function
def Normalise(df):
    for col in df.columns:
            if df[f'{col}'].dtype != 'object': # Ignore string value columns
                df[f'{col}'] = stats.boxcox(df[f'{col}'])[0]

Normalise(normal16)
Normalise(normal18)
'''