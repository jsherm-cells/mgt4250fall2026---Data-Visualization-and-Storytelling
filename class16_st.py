import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_excel('sample_-_superstore.xls')
df = df[df['Country/Region']=='United States']
all_states = sorted(df["State/Province"].unique())
target_states = st.multiselect("States", 
                               options=all_states, 
                               default=all_states
)
df = df[df['State/Province'].isin(target_states)]

SOP = df.groupby('State/Province')['Profit'].sum()
SOS = df.groupby('State/Province')['Sales'].sum()
PMBS = SOP/SOS
PMBS = PMBS.reset_index(name='Profit Margin')

fig1 = px.choropleth(
    locations=PMBS['State/Province'],
    locationmode='USA-states',
    color=PMBS['Profit Margin'],
    scope='usa',
    color_continuous_scale='Viridis',
    title = 'Profit Margin by State',
    template='plotly_dark'
)


SOPBC = df.groupby('Category')['Profit'].sum()
SOSBC = df.groupby('Category')['Sales'].sum()
PMBC = SOPBC/SOSBC
PMBC = PMBC.reset_index(name='Profit Margin')

fig2 = px.bar(
    PMBC,
    x='Category',
    y='Profit Margin',
    color='Category',
    title='Profit Margin by Category',
    template='plotly_dark'
)

df["YearMonth"] = pd.to_datetime(df['Order Date']).dt.strftime('%Y-%m')
a = df.groupby(['Category', 'YearMonth'])['Profit'].sum()
b = df.groupby(['Category', 'YearMonth'])['Sales'].sum()
PRCYM = a/b
PRCYM = PRCYM.reset_index(name='Profit Margin')

fig3 = px.line(
    PRCYM,
    x='YearMonth',
    y='Profit Margin',
    color='Category',
    title='Profit Margin of Categories over Time',
    template='plotly_dark'
)

PSB = df.groupby('Sub-Category')['Sales'].sum()
PSB = PSB.reset_index(name='Sub-Cat Sales Totals')
PSB['Category'] = df['Category']
PSB['Sales'] = df['Sales']

fig4 = px.treemap(
    PSB,
    path=[px.Constant('Category'), 'Sub-Category'],
    values='Sub-Cat Sales Totals', color='Category',
    title='Total Sales on Sub-Cat Level',
    template='plotly_dark'
)

st.title('Profit Margin and Sales Analysis')
st.header('For Class 16/17')
st.write('An analysis of the profit margins in each state, category, sub-cat, and overtime')
st.set_page_config(layout='wide')
col1, col2 = st.columns([7,3])
with col1:
    st.plotly_chart(fig1, width='stretch')
with col2:
    st.plotly_chart(fig2, width='stretch')
col3, col4 = st.columns([5,5])
with col3:
    st.plotly_chart(fig3, width='stretch')
with col4:
    st.plotly_chart(fig4, width='stretch')