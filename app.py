import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('startup_invest (1).csv')
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['month']=df['date'].dt.month
df['year'] = df['date'].dt.year
def load_investor_detailed(investor):
    st.title(investor)
    last_5df = df[df['investors'].str.contains(investor)][['date', 'startup', 'vertical', 'city', 'round', 'amount']].head()
    st.subheader('Most Recent Investments')
    st.dataframe(last_5df)
    col1,col2 = st.columns(2)
    with col1:
        big_df = df[df['investors'].str.contains('IDG Ventures')].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_df.index,big_df.values)
        st.pyplot(fig)
    with col2:
        sector_investment = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sector Investments in')
        fig1, ax1 = plt.subplots()
        ax1.pie(sector_investment,labels=sector_investment.index,autopct='%0.01f%%')
        st.pyplot(fig1)
    col3,col4 = st.columns(2)
    with col3:
        stage_invest = df[df['investors'].str.contains(investor)].groupby('subvertical')['amount'].sum()
        st.subheader('Stage Investments in')
        fig2, ax2 = plt.subplots()
        ax2.pie(stage_invest,labels=stage_invest.index,autopct='%0.01f%%')
        st.pyplot(fig2)
    with col4:
        city_invest = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('city Investments in')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_invest,labels=city_invest.index,autopct='%0.01f%%')
        st.pyplot(fig3)
    df['year'] = df['date'].dt.year
    yearwise = df[df['investors'].str.contains('IDG Ventures')].groupby('year')['amount'].sum()
    st.subheader('Yearwise Investments in ')
    fig4, ax4 = plt.subplots()
    ax4.plot(yearwise.index,yearwise.values)
    st.pyplot(fig4)
    startup = df[df['investors'].str.contains(investor)]['startup'].unique().tolist()
    list1 = []
    for i in df['investors'].unique():
        startups_i = df[df['investors'].str.contains(i)]['startup'].unique().tolist()
        if set(startup) & set(startups_i):  # common startup check
            list1.append(i)
    st.subheader('Similar Investors names ')
    st.json(list(set(list1)))

def load_overall_analysis():
    st.title('Overall Analysis')


    col1,col2,col3,col4 = st.columns(4)
    with col1:
        total_invested_amount = round(df['amount'].sum())
        st.metric('Total Invested Amount', str(total_invested_amount) + 'CR')
    with col2:
        max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
        st.metric('Maximum Invested Amount',str(max_funding)+'CR')
    with col3:
        avg_funding = df.groupby('startup')['amount'].sum().mean()
        st.metric('Average Invested Amount',str(avg_funding)+'CR')
    with col4:
        num_startup = df['startup'].nunique()
        st.metric('Funded Startup',num_startup)
    st.header('Month on Month Graph')
    selected_option = st.selectbox('Select Type',['Total','Count'])


    if selected_option=='Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else :
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
    temp_df['x-Axis'] = temp_df['month'].astype('str') + '-' + temp_df['month'].astype('str')
    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x-Axis'], temp_df['amount'])
    st.pyplot(fig3)
def load_startup_details(startup):
    st.title('Startup Detailes')
    last5_investor = df[df['startup'].str.contains(startup)][['date','vertical','subvertical','city','investors','round','amount']]
    st.subheader('Recently Invested in This Startup')
    st.dataframe(last5_investor)
    investors_detailed = df[df['startup'].str.contains('Ola Cabs')].groupby('investors')['amount'].sum().sort_values(ascending=False)
    total_investments = str(df[df['startup'].str.contains('Ola Cabs')]['amount'].sum())+'CR'
    col1,col2 = st.columns(2)
    with col1:
        st.subheader('Investors Details')
        st.dataframe(investors_detailed)
    with col2:
        st.subheader('Total Investments')
        st.metric('Total Investments',total_investments)
    datee = df[df['startup'].str.contains(startup)].groupby(['year', 'month'])['amount'].sum().reset_index()
    datee['temp_date'] = datee['month'].astype('str') + '-' + datee['year'].astype('str')
    citywiseinvestments = df[df['startup'].str.contains('Ola Cabs')].groupby('city')['amount'].sum()
    col3,col4 = st.columns(2)
    with col3:
        st.subheader('Month By Month Startup money details')
        fig1,ax1 = plt.subplots()
        ax1.plot(datee['temp_date'], datee['amount'])
        st.pyplot(fig1)
    with col4:
        st.subheader('City Wise Investments')
        fig2, ax2 = plt.subplots()
        ax2.pie(citywiseinvestments,labels=citywiseinvestments.index,autopct='%0.01f%%')
        st.pyplot(fig2)
st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])
if option=='Overall Analysis':
    load_overall_analysis()

elif option=='Startup':
    selected_startup = st.sidebar.selectbox('Select One',list(df['startup'].unique()))
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:
        load_startup_details(selected_startup)
elif option=='Investor':
    selected_investor = st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    print(selected_investor)
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_detailed(selected_investor)