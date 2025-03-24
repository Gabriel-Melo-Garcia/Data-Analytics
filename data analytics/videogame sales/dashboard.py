import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout='wide')

@st.cache_data
def load_data():
    return pd.read_csv('vgsales_clean.csv')

df = load_data()

st.title("Video Game Sales Dashboard")

df = pd.read_csv('vgsales_clean.csv')
year = st.sidebar.selectbox("year", df['Year'].sort_values(ascending=False).unique())

col1 ,col2 = st.columns(2)
col3 ,col4 = st.columns([3, 2])

genre = st.sidebar.selectbox("Genre", ['All'] + sorted(df['Genre'].unique()))
publisher = st.sidebar.selectbox("Publisher", ['All'] + sorted(df['Publisher'].unique()))

df_filtered = df[df['Year'] == year]
if genre != 'All':
    df_filtered = df_filtered[df_filtered['Genre'] == genre]
if publisher != 'All':
    df_filtered = df_filtered[df_filtered['Publisher'] == publisher]

df_grouped_top_sales = df_filtered.groupby(['Name'], as_index=False).agg({'Global_Sales': 'sum'})
df_sorted_top_sales = df_grouped_top_sales.sort_values(by='Global_Sales', ascending=False).head(10)

fig1 = px.bar(
    df_sorted_top_sales,
    x='Name',
    y='Global_Sales',
    title=f'Top 10 of {year}',

)
fig1.update_layout(
    xaxis_title="Game Name",
    yaxis_title="Sales (in million units)",
)
fig1.update_xaxes(tickangle=45)
col1.plotly_chart(fig1)

df_grouped_top_genre = df_filtered.groupby(['Genre'], as_index=False).agg({'Global_Sales': 'sum'})
df_sorted_top_genre = df_grouped_top_genre.sort_values(by='Global_Sales', ascending=False).head(10)

fig2 = px.bar(
    df_sorted_top_genre,
    x = 'Genre',
    y = 'Global_Sales',
    title=f'Top 10 genres of {year}',
    color='Genre'
)
fig2.update_layout(
    xaxis_title="Genre",
    yaxis_title="Sales (in million units)",
)
fig2.update_xaxes(tickangle=45)
col2.plotly_chart(fig2)

df_top_publishers = df_filtered.groupby('Publisher', as_index=False).agg({'Global_Sales': 'sum'})

top_publishers = df_top_publishers.sort_values(by='Global_Sales', ascending=False).head(10)['Publisher']

df_filtered_top_publishers = df_filtered[df_filtered['Publisher'].isin(top_publishers)]

fig3 = px.sunburst(
    df_filtered_top_publishers,
    path=['Publisher', 'Name'],
    values='Global_Sales',
    title=f"Top 10 Publishers and their games of {year}"
)

col3.plotly_chart(fig3, use_container_width=True)

df_publisher_regions = df_filtered.groupby('Publisher', as_index=False).agg({
    'NA_Sales': 'sum',
    'EU_Sales': 'sum',
    'JP_Sales': 'sum',
    'Other_Sales': 'sum'
})

df_publisher_regions['Total_Sales'] = df_publisher_regions[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum(axis=1)
fig4 = px.bar(
    df_publisher_regions.sort_values(by='Total_Sales', ascending=False).head(10),
    x='Publisher',
    y=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'],
    title=f"Sales distribution per region for the Top 10 Publishers in {year}",
    barmode='stack'
)

fig4.update_layout(
    xaxis_title="Publisher",
    yaxis_title="Sales (in million units)",
)
fig4.update_xaxes(
    tickangle=45)
col4.plotly_chart(fig4)

st.download_button(
    label="Download filtered data as CSV",
    data=df_filtered.to_csv(index=False),
    file_name=f"vgsales_{year}.csv",
    mime="text/csv"
)