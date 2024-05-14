import pandas as pd
import io
import requests

site = r"https://covid19.who.int/WHO-COVID-19-global-data.csv"
s = requests.get(site).content
covid_data = pd.read_csv(io.StringIO(s.decode('utf-8'))) 
site = r"https://github.com/y-takefuji/score-covid-19-policy/raw/main/country-pop.csv"
s = requests.get(site).content
pop_data = pd.read_csv(io.StringIO(s.decode('utf-8'))) 

# Get the latest date
latest_date = covid_data['Date_reported'].max()
print(f'Latest date: {latest_date}')

# Select countries
import subprocess as sp
import os
if os.path.isfile('countries'):
 countries=open('countries').read().strip()
 countries=countries.split(',')
else:
 sp.call("wget -nc https://github.com/y-takefuji/score-covid-19-policy/raw/main/countries",shell=True)
 countries=open('countries').read().strip()
 countries=countries.split(',')

# Create a mapping from country names in the countries list to country names in the COVID-19 data
country_mapping = {'United States': 'United States of America', 'United Kingdom': 'The United Kingdom'}
covid_countries = [country_mapping.get(country, country) for country in countries]

# Filter data for selected countries and latest date
covid_data = covid_data[covid_data['Country'].isin(covid_countries) & (covid_data['Date_reported'] == latest_date)]

# Replace country names in population data
pop_data['country'] = pop_data['country'].replace(country_mapping)

# Merge with population data
covid_data = covid_data.merge(pop_data, left_on='Country', right_on='country')

# Calculate score
covid_data['score'] = (covid_data['Cumulative_deaths'] / covid_data['pop2022'] * 1000000).astype(int)

# Replace country names with names from the countries list
covid_data['Country'] = covid_data['Country'].replace({v: k for k, v in country_mapping.items()})

# Print results
covid_data = covid_data[['Country', 'pop2022', 'Cumulative_deaths', 'score']].sort_values(by='score')
covid_data.columns = ['country', 'population', 'deaths', 'score']
def main():
 print(covid_data.to_string(index=False))
if __name__ == "__main__":
    main()
