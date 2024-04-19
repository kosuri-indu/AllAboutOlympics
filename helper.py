import pandas as pd

def get_medal_tally(data, year, country):
    medal_data = data.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_data = medal_data
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_data = medal_data[medal_data['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_data = medal_data[medal_data['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_data = medal_data[(medal_data['Year'] == year) & (medal_data['region'] == country)]

    if flag == 1:
        result = temp_data.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        result = temp_data.groupby('NOC').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()
        region = temp_data.groupby('NOC').first()['region'].reset_index()   
        result = pd.merge(result, region, on='NOC') 
        result = result[['NOC', 'region', 'Gold', 'Silver', 'Bronze']]  
    
    result['total'] = result['Gold'] + result['Silver'] + result['Bronze']

    return result

def country_year_list(data):
    years = data['Year'].unique().tolist()
    years.sort()
    years.insert(0,"Overall")

    country = data['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0,"Overall")

    return years, country

def held_at_city(data, season):
    if season == 'Overall':
        region = data.groupby('Year').first()['City'].reset_index()
        season = data.groupby('Year').first()['Season'].reset_index()
        final_data = region.merge(season, on="Year")
    else:
        final_data = data.groupby('Year').first()['City'].reset_index()
    return final_data

def data_over_time(data, column):

    nations_over_time = data.drop_duplicates(['Year', column])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year': 'Edition', 'count': column}, inplace=True)
    return nations_over_time

def most_successful(data, sport):
    temp_data = data.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_data = temp_data[temp_data['Sport'] == sport]

    x = temp_data['Name'].value_counts().reset_index().head(15).merge(data, left_on='Name', right_on='Name', how='left')[
        ['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'}, inplace=True)
    return x

def sports_wise_medals(data,country):
    temp_data = data.dropna(subset=['Medal'])
    temp_data.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_data = temp_data[temp_data['region'] == country]
    final_data = new_data.groupby('Sport').count()['Medal'].reset_index()

    return final_data

def yearwise_medal_tally(data,country):
    temp_data = data.dropna(subset=['Medal'])
    temp_data.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_data = temp_data[temp_data['region'] == country]
    final_data = new_data.groupby('Year').count()['Medal'].reset_index()

    return final_data

def country_event_heatmap(data,country):
    temp_data = data.dropna(subset=['Medal'])
    temp_data.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_data[temp_data['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(data, country):
    temp_data = data.dropna(subset=['Medal'])

    temp_data = temp_data[temp_data['region'] == country]

    x = temp_data['Name'].value_counts().reset_index().head(10).merge(data, left_on='Name', right_on='Name', how='left')[
        ['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'}, inplace=True)
    return x

def most_successful_event(data, event):
    temp_data = data.dropna(subset=['Medal'])

    if event != 'Overall':
        temp_data = temp_data[temp_data['Event'] == event]
    
    x = temp_data['Name'].value_counts().reset_index().head(15).merge(data, left_on='Name', right_on='Name', how='left')[
        ['Name', 'count', 'region', 'Season']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'}, inplace=True)
    return x

def medals_per_event(data,country):
    temp_data = data.dropna(subset=['Medal'])
    temp_data.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_data = temp_data[temp_data['region'] == country]
    final_data = new_data.groupby('Event').count()['Medal'].sort_values(ascending=False).reset_index()

    return final_data

def men_vs_women(data):
    athlete_data = data.drop_duplicates(subset=['Name', 'region'])

    men = athlete_data[athlete_data['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_data[athlete_data['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final

def most_successful_overall(data):
    temp_data = data.dropna(subset=['Medal'])

    x = temp_data['Name'].value_counts().reset_index().head(20).merge(data, left_on='Name', right_on='Name', how='left')[
        ['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'}, inplace=True)
    return x