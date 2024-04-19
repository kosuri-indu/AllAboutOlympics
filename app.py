import pandas as pd
import utils.preprocessor, utils.helper as helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
from PIL import Image
import streamlit as st

summer_data = pd.read_csv('data/Athletes_summer_games.csv')
winter_data = pd.read_csv('data/Athletes_winter_games.csv')
regions = pd.read_csv('data/regions.csv')

summer_data = preprocessor.preprocess_summer_olympics(summer_data, regions)
winter_data = preprocessor.preprocess_winter_olympics(winter_data, regions)

st.sidebar.title('Olympics Data Analysis')

selected_olympics = st.sidebar.selectbox("🌍 Choose the season", ['Overall','Summer','Winter'])

img = Image.open('images/logo.jpeg')
st.sidebar.image(img)

user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

if selected_olympics == 'Overall':
    data = pd.concat([summer_data, winter_data], sort=False)
elif selected_olympics == 'Summer':
    data = summer_data
else:
    data = winter_data

if user_menu == 'Medal Tally':
    st.sidebar.header('Olympics Medal Tally')
    years, country = helper.country_year_list(data)

    selected_year = st.sidebar.selectbox("📅 Select Year", years)
    selected_country = st.sidebar.selectbox("🌍 Select Country", country)

    medal_tally = helper.get_medal_tally(data, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("🏆 Overall Medal Tally 🏆")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("🏆 Medal Tally in " + str(selected_year) + " Olympics 🏆")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title("🏆 " + selected_country + "'s overall performance 🏆")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title("🏆 " + selected_country + "'s performance in " + str(selected_year) + " Olympics 🏆")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':

    editions = data['Year'].unique().shape[0] - 1
    cities = data['City'].unique().shape[0]
    sports = data['Sport'].unique().shape[0]
    events = data['Event'].unique().shape[0]
    athletes = data['Name'].unique().shape[0]
    nations = data['region'].unique().shape[0]


    st.title("Top Statistics 🥇")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.subheader("Editions")
        st.title(editions)
    with col2:
        st.subheader("Hosts")
        st.title(cities)
    with col3:
        st.subheader("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Events")
        st.title(events)
    with col2:
        st.subheader("Nations")
        st.title(nations)
    with col3:
        st.subheader("Athletes")
        st.title(athletes)

    
    st.markdown("---")

    nations_over_time = helper.data_over_time(data, 'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    st.markdown("---")

    events_over_time = helper.data_over_time(data, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    st.markdown("---")

    athlete_over_time = helper.data_over_time(data, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.markdown("---")
    
    city_data = helper.held_at_city(data, selected_olympics)
    if not city_data.empty:
        st.title("Cities that hosted the Olympics")
        st.table(city_data)
    else:   
        st.subheader("No data available")

    st.markdown("---")

    st.title("No. of Events over time(Every Sport)")
    fig,axis = plt.subplots(figsize=(20,20))
    discrete_data = data.drop_duplicates(['Year', 'Sport', 'Event'])
    axis = sns.heatmap(discrete_data.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.markdown("---")

    st.title("Most successful Athletes")
    sport_list = data['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(data,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = data['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('🌍 Select Country',country_list)

    country_data = helper.yearwise_medal_tally(data, selected_country)
    
    st.title(selected_country + " Medal Tally over the years")
    if not country_data.empty:
        fig = px.line(country_data, x="Year", y="Medal")
        st.plotly_chart(fig)
    else:
        st.subheader("The selected country didn't win any medals")

    st.markdown("---")

    pt = helper.country_event_heatmap(data,selected_country)
    st.title(selected_country + " excels in the following sports")
    if not pt.empty:
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(pt,annot=True)
        st.pyplot(fig)
    else:
        st.subheader("The selected country didn't win any medals")
    
    st.markdown("---")

    sports_data = helper.sports_wise_medals(data,selected_country)
    if not sports_data.empty:
        st.title(selected_country + " excels in the following sports")
        fig, ax = plt.subplots()
        ax.barh(sports_data['Sport'], sports_data['Medal'])
        st.pyplot(fig)

        fig, ax = plt.subplots()
        ax.pie(sports_data['Medal'], labels=sports_data['Sport'])
        st.pyplot(fig)
    else:
        st.subheader("The selected country didn't win any medals")

    st.markdown("---")

    st.title("🥇 Top 10 athletes of " + selected_country)
    top10_data = helper.most_successful_countrywise(data,selected_country)
    if not top10_data.empty:
        st.table(top10_data)
    else:
        st.subheader("The selected country didn't win any medals")

    st.markdown("---")

    st.title("Event-wise Medals won by "+ selected_country)
    event_data = helper.medals_per_event(summer_data,selected_country)
    if not event_data.empty:
        st.table(event_data)
    else:
        st.subheader("The selected country didn't win any medals")


if user_menu == 'Athlete-wise Analysis':

    st.title("Top Athlete of Each Event")
    event_list = data['Event'].unique().tolist()
    event_list.sort()
    event_list.insert(0,'Overall')

    selected_event = st.selectbox('Select a Event',event_list)
    x = helper.most_successful_event(data,selected_event)
    st.table(x)

    st.markdown("---")
    
    athlete_data = data.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_data['Age'].dropna()
    x2 = athlete_data[athlete_data['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_data[athlete_data['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_data[athlete_data['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=800,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    st.markdown("---")

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_data = athlete_data[athlete_data['Sport'] == sport]
        x.append(temp_data[temp_data['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    sport_list = data['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    if not any(series.empty for series in x):
        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=800, height=600)
        st.plotly_chart(fig)
        st.markdown("---")
    else:
        st.subheader("The selected country didn't win any medals")

    st.title("Men Vs Women Participation Over the Years")
    men_women_data = helper.men_vs_women(data)
    if not men_women_data.empty:
        fig = px.line(men_women_data, x="Year", y=["Male", "Female"])
        fig.update_layout(autosize=False, width=800, height=600)
        st.plotly_chart(fig)
        st.markdown("---")
    else:
        st.subheader("No data available")

    st.title("🥇 Top 20 athletes")
    top20_data = helper.most_successful_overall(data)
    if not top20_data.empty:
        st.table(top20_data)
    else:
        st.subheader("The selected country didn't win any medals")
