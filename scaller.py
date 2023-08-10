import streamlit as st
import pandas as pd
import yfinance as yf
from streamlit_option_menu import option_menu
import yahoo_fin.stock_info as si
from datetime import datetime
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards
from datetime import date
import plotly.graph_objects as go
import plotly_express as px
from stocknews import StockNews
import numpy as np
from plotly.subplots import make_subplots
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(page_title="Stock Analysis",page_icon="📈",layout="wide",initial_sidebar_state="expanded",)

def style_metric_cards(
    background_color: str = "#090c0c",
    border_size_px: int = 2,
    border_color: str = "#CCC",
    border_radius_px: int =10,
    border_left_color: str = "#beebe5",
    box_shadow: bool = True,
):

    box_shadow_str = (
        "box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;"
        if box_shadow
        else "box-shadow: none !important;"
    )
    st.markdown(
        f"""
        <style>
            div[data-testid="metric-container"] {{
                background-color: {background_color};
                border: {border_size_px}px solid {border_color};
                padding: 5% 5% 5% 10%;
                border-radius: {border_radius_px}px;
                border-left: 0.5rem solid {border_left_color} !important;
                {box_shadow_str}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    
st.image('sto.png')
df1 = pd.read_csv('symbols.csv', encoding='ISO-8859-1')
choice = st.sidebar.selectbox("Select Ticker", df1)
symbol = yf.Ticker(choice)

st.sidebar.header('Stock Analysis Options')

with st.sidebar:
    selected = option_menu("Menu", ["Details","Stock info","Analysis","News"], 
                icons=["buildings","info-circle","graph-up-arrow","newspaper"],
                menu_icon= "list",
                default_index=0,
                styles={"nav-link": {"font-size": "15px", "text-align": "left", "margin": "2px", "--hover-color": "#3e3e77"},
                        "nav-link-selected": {"background-color": "#6e67cf"}})
    
   

if selected == "Details":
    def get_company_info(symbol):
    # Create a Ticker object
     ticker = yf.Ticker(symbol)

    # Get company info from Yahoo Finance
     info = ticker.info
    
   
     market_cap = info.get('marketCap', 'Not available.')
     if isinstance(market_cap, (int, float)):
            market_cap = "{:,.2f}".format(market_cap)
    # Get the long business summary
     long_summary = info.get('longBusinessSummary', 'Not available.')
     
     return {
        'Symbol': symbol,
        'Name': info.get('longName', 'Not available.'),
        'Sector': info.get('sector', 'Not available.'),
        'Industry': info.get('industry', 'Not available.'),
        'Website': info.get('website', 'Not available.'),
        'Market Cap': market_cap,
        'Long Business Summary': long_summary,
    }
   
    add_vertical_space(1)
    st.subheader('Company Information Dashboard')
   
    
#symbol = yf.Ticker(choice)

    if st.button('Get Company Info'):
        # Fetch company information
        
        choice = choice.upper()
        
        company_info = get_company_info(choice)

        # Convert to a DataFrame
        df = pd.DataFrame.from_dict(company_info, orient='index', columns=['Value'])

        # Display the company information using DataFrame
        st.dataframe(df,use_container_width=True)
        c11,c12,c13,c14,c15=st.columns(5) # In Row 1
        
        c11.metric("Current Price",symbol.info["currentPrice"])
        c12.metric("Currency",symbol.info["currency"])
        c13.metric("Exchange",symbol.info["exchange"])
        c14.metric("Financial Currency",symbol.info["financialCurrency"])
        c15.metric("Regular Market Open",symbol.info['regularMarketOpen'])
        style_metric_cards()
        st.subheader('Long Business Summary')
        st.info(df.loc['Long Business Summary']['Value'])
        
if selected == "Stock info":     
    add_vertical_space(1) 
    tab1,tab2,tab3,tab4,tab5= st.tabs(["Quote table","Balance sheet and Cashflow","Income statement","Mutalfund holders","Earning day"])
   
    with tab1:
# Button to fetch the quote table
     if st.button('Get Quote Table'):
      try:
          
        choice = choice.upper()
        # Create a Ticker object
        ticker = yf.Ticker(choice)

        # Get the quote table
        quote_table = ticker.info

        # Display the quote table using DataFrame
        st.markdown('__<p style="text-align:center; font-size: 18px; color: #FDFEFE "> Quote table </P>__',
                unsafe_allow_html=True)
        st.caption("Quote table in the context of a company typically refers to a data table or database that stores information related to stock quotes or financial market quotes. This table contains the details of various financial instruments traded on stock exchanges, such as stocks, bonds, commodities, currencies, and other securities.")
        st.write('Company :',symbol.info["longName"])
        st.dataframe(quote_table,use_container_width=True)
        
      except:
        st.error("Error fetching the quote table. Please check the stock symbol and try again.")
        
    
    with tab2:
     if st.button('Get Balance Sheet and Cashflow'):
       try:
        choice = choice.upper()
        # Create a Ticker object
        ticker = yf.Ticker(choice)

        # Get the balance sheet data
        balance_sheet = ticker.balance_sheet

        # Get the cashflow data
        cashflow = ticker.cashflow

        # Display the balance sheet using DataFrame
        st.markdown('__<p style="text-align:center; font-size: 18px; color: #FDFEFE "> Balance Sheet </P>__',
                unsafe_allow_html=True)
        st.caption("Balance sheet,is a statement of financial position, provides a summary of a company's assets, liabilities, and shareholders' equity at a specific point in time.")
        st.write('Company :',symbol.info["longName"])
        st.dataframe(balance_sheet,use_container_width=True)

        # Display the cashflow using DataFrame
        st.markdown('__<p style="text-align:center; font-size: 18px; color: #FDFEFE "> Cash flow </P>__',
                unsafe_allow_html=True)
        st.caption("The cash flow statement is a financial statement that provides a detailed account of the cash inflows and outflows during a specific period, typically a quarter or a year.")
        st.write('Company :',symbol.info["longName"])
        st.dataframe(cashflow,use_container_width=True)

       except:
        st.error("Error fetching the data. Please check the stock symbol and try again.")
        
     def get_income_statement(ticker):
      try:
        ticker = ticker.upper()
        # Create a Ticker object
        ticker_obj = yf.Ticker(ticker)
        
        # Get the income statement
        income_statement = ticker_obj.financials
        return income_statement
        
      except:
        return None
    with tab3:
    # Button to fetch the income statement
     if st.button('Get Income Statement'):
        # Fetch the income statement data
         income_statement_data = get_income_statement(choice)
         
         if income_statement_data is not None:
            # Display the income statement using DataFrame
            st.markdown('__<p style="text-align:center; font-size: 18px; color: #FDFEFE "> Income Statement </P>__',
                unsafe_allow_html=True)
            st.caption("The income statement summarizes a company's revenues, expenses, and profits or losses during that period and helps stakeholders understand how the company's operations have contributed to its financial results.")
            st.write('Company :',symbol.info["longName"])
            st.dataframe(income_statement_data,use_container_width=True)
         else:
            st.error("Error fetching the income statement. Please check the stock symbol and try again.")
        
     def get_mutual_fund_holders(ticker):
      try:
        ticker = ticker.upper()
        # Create a Ticker object
        ticker_obj = yf.Ticker(ticker)
        
        mutual_fund_holders = ticker_obj.mutualfund_holders
        return mutual_fund_holders
        
      except:
        return None
    with tab4:

     if st.button('Get Mutual Fund Holders'):
        # Fetch the mutual fund holders' data
        mutual_fund_holders_data = get_mutual_fund_holders(choice)

        if mutual_fund_holders_data is not None:
            # Display the mutual fund holders' data using DataFrame
            st.markdown('__<p style="text-align:center; font-size: 18px; color: #FDFEFE "> Mutualfund Holders </P>__',
                unsafe_allow_html=True)
            st.caption("A mutual fund holder's statement is a document provided by the mutual fund company to individual investors who have invested in their mutual funds.")
            st.write('Company :',symbol.info["longName"])
            st.dataframe(mutual_fund_holders_data,use_container_width=True)
        else:
            st.error("Error fetching the mutual fund holders' data. Please check the stock symbol and try again.")
            
            
     def get_earning_dates(ticker):
      try:
        ticker = ticker.upper()
        # Create a Ticker object
        ticker_obj = yf.Ticker(ticker)
        
        # Get the earning dates
        earning_dates = ticker_obj.earnings_dates
        return earning_dates
        
      except Exception as e:
        st.error(f"Error fetching the earning dates: {str(e)}")
        return None
    
    

    with tab5:
     if st.button('Get Earning Dates'):
        # Fetch the earning dates data
        earning_dates_data = get_earning_dates(choice)
   
        if earning_dates_data is not None:
            # Display the earning dates using DataFrame
            st.markdown('__<p style="text-align:center; font-size: 18px; color: #FDFEFE "> Earning Days </P>__',
                unsafe_allow_html=True)
            st.caption("Earnings dates refer to the specific dates on which publicly-traded companies announce their quarterly or annual financial results to the public.")
            st.write('Company :',symbol.info["longName"])
            st.dataframe(earning_dates_data,use_container_width=True)
          
        else:
            st.warning("No earning dates data available for the selected stock symbol.")
            
if selected == "Analysis":
    if "key" not in st.session_state:
        st.session_state.key=0
        st.session_state.key=choice
    
    
    START = date(2023,1,1)
    TODAY = date.today()

    if "st" not in st.session_state:
     st.session_state.st=0

    if "et" not in st.session_state:
     st.session_state.et=0
    
    start_date = st.sidebar.date_input("Start date",START)
    end_date = st.sidebar.date_input("End date",TODAY,)

    st.session_state.st=start_date
    st.session_state.et=end_date

    tickerDf=symbol.history(period="1d",start=st.session_state.st,end=st.session_state.et)
    tickerDf.reset_index(inplace=True)
    add_vertical_space(3)
    st.write('Company :',symbol.info["longName"])
    st.markdown('__<p style="text-align:center; font-size: 18px; color: #FDFEFE "> Stock price history </P>__',
                unsafe_allow_html=True)

    st.dataframe(tickerDf,use_container_width=True)
    add_vertical_space(3)
    
    fig = go.Figure(data=[go.Candlestick(
    x=tickerDf['Date'],
    open=tickerDf['Open'], high=tickerDf['High'],
    low=tickerDf['Low'], close=tickerDf['Close'],
    increasing_line_color= 'cyan', decreasing_line_color= 'red'
    )])
    
    fig.update_layout(
    title='History of Stock price',
    yaxis_title='Values',
    xaxis_title='Date',title_x=0.5
    )
    st.write('Company :',symbol.info["longName"])
    st.plotly_chart(fig,use_container_width=True)
    add_vertical_space(5)
    
    
       # Create subplots with 3 rows and 1 column
    fig5 = make_subplots(rows=5, cols=1, shared_xaxes=True, vertical_spacing=0.05)

    # Subplot 1: Date vs. Close
    fig5.add_trace(go.Scatter(x=tickerDf['Date'], y=tickerDf['Close'], mode='lines', name='Close'), row=1, col=1)
    fig5.update_yaxes(title_text='Close Price', row=1, col=1)

    # Subplot 2: Date vs. Open
    fig5.add_trace(go.Scatter(x=tickerDf['Date'], y=tickerDf['Open'], mode='lines', name='Open'), row=2, col=1)
    fig5.update_yaxes(title_text='Open Price', row=2, col=1)

    # Subplot 3: Date vs. Volume
    fig5.add_trace(go.Bar(x=tickerDf['Date'], y=tickerDf['Volume'], name='Volume'), row=3, col=1)
    fig5.update_yaxes(title_text='Volume', row=3, col=1)
    
    fig5.add_trace(go.Scatter(x=tickerDf['Date'], y=tickerDf['High'], name='High'), row=4, col=1)
    fig5.update_yaxes(title_text='High', row=4, col=1)
    
    fig5.add_trace(go.Scatter(x=tickerDf['Date'], y=tickerDf['Low'], name='Low'), row=5, col=1)
    fig5.update_yaxes(title_text='Low', row=5, col=1)
    
    # Update layout for the subplots
    fig5.update_layout(
        title=f'{choice} Stock Subplots',
        xaxis=dict(title='Date'),
        showlegend=False,
        height=1000,
        width=1000,
        template='plotly_white',
    )
    st.plotly_chart(fig5,use_container_width=True)
   
    
    add_vertical_space(5)
    st.write('Company :',symbol.info["longName"])
    mdf=yf.download(choice,start=start_date,end=end_date)
    
    mdf.drop(['Open','High','Low','Close','Volume'],axis=1,inplace=True)
    mdf['% change ' + str(choice)]=mdf['Adj Close']/mdf['Adj Close'].shift(1)-1
    
    mdf1=yf.download(choice,start=start_date,end=end_date)
    
    mdf1.reset_index(inplace=True)
    mdf1.drop(['Open','Close','Volume','High','Low'],axis=1,inplace=True)
    mdf1['% change '+str(choice)]=mdf1['Adj Close']/mdf1['Adj Close'].shift(1)-1
    
    kk=mdf1.drop(['Adj Close'],axis=1)
    md2=pd.merge(left=kk,right=mdf['% change ' +str(choice)],how='right', on='Date')
    
    
    fig1=px.bar( md2,x='Date',y= md2.columns,width=1000, height=400)
    fig1.update_layout(
    title='Comparison',title_x=0.5)
    st.plotly_chart(fig1,use_container_width=True)
   
    
if selected == "News":
    st.markdown('__<p style="text-align:left; font-size: 22px; color: #FDFEFE ">:red[Latest News ] </P>__',
                unsafe_allow_html=True)
    
    sn= StockNews(choice,save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f' News {i+1}')
        st.caption(df_news['published'][i])
        title=df_news['title'][i]
        st.write(f'***{title}***')
        st.info(df_news['summary'][i])
    
       








     









