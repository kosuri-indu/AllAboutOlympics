## Olympics Data Analysis Dashboard 🏆📅

This project showcases an interactive data analysis dashboard for Olympic Games data using Streamlit, Plotly, Pandas, Seaborn, Matplotlib, and PIL (Pillow). 
This application analyzes and visualizes Olympic Games data including medal tallies, country-wise performance, athlete statistics, and more.
Use the sidebar to select different analysis options such as Medal Tally, Overall Analysis, Country-wise Analysis, or Athlete-wise Analysis. Explore the interactive charts and tables to gain insights into Olympic Games data.

### Features
- **Medal Tally Analysis**: View medal tally based on selected year and country.
- **Overall Analysis**: Explore overall statistics like editions, host cities, participating nations, and more.
- **Country-wise Analysis**: Analyze medal tallies and sports performance of specific countries over the years.
- **Athlete-wise Analysis**: Investigate top athletes, age distributions, and participation trends.

### Tech Stack
| Language | Libraries Used |
|-----------|---------------|
| Python | Numpy, Pandas, Matplotlib, Seaborn, Plotly (express, figure_factory), Pillow, Streamlit|

### Setup and Installation
To run this application locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AllAboutOlympics.git
   ```

2. Install dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

### Folder Structure

``` 
olympics-analysis/
│
├── app.py                
├── data/                 
│   ├── Athletes_summer_games.csv
│   ├── Athletes_winter_games.csv
│   └── regions.csv
├── images/              
│   └── logo.jpeg
├── helper.py             
├── preprocessor.py       
├── requirements.txt     
└── README.md             

```
