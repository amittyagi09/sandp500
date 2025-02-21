import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf

st.set_page_config(layout="wide")
st.title("S&P 500 Application")
st.write("This web app retieves list of S&P 500 list (from wikipedia) and its corresponding **stock closing price** (year-to-date)")
st.write("**Python libraries:** pandas, numpy, matplotlib, yfinance")
st.write("**Data source:** [wikiepedia](https://www.wikipedia.org)")
st.write("***")

@st.cache_data
def load_data():
    url="https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    html=pd.read_html(url, header=0)
    html=html[0]
    return html

#s&p500data
data=load_data()

sector_unique=list(data["GICS Sector"].unique())

#sidebar
st.sidebar.header("User Input Features")
selected_sector=st.sidebar.multiselect("Sector", sector_unique, sector_unique)
com_no=st.sidebar.number_input("Companies", 1,5)

show_data=data[data["GICS Sector"].isin(selected_sector)]
st.header("Display companies in the selected selctor")
st.write(" **Dimensions:** " + str(show_data.shape[0]) + " rows " + str(show_data.shape[1]) + " columns")
st.dataframe(show_data)

com_list=list(show_data["Symbol"])[ :com_no]

stock_data=yf.download(
        tickers=com_list,
        period="ytd",
        interval="1d",
        group_by="ticker",
        auto_adjust=True,
        prepost=True,
        threads=True,
        proxy=None
        )

def plot_data(Symbol):
    df=pd.DataFrame(stock_data[Symbol]["Close"])
    df["Date"]=df.index
    fig, ax=plt.subplots()
    plt.plot(df["Date"],  df["Close"], alpha=0.8)
    plt.fill_between(df["Date"], df["Close"], alpha=0.5)
    plt.xticks(rotation=90)
    plt.xlabel("Date", fontweight="bold")
    plt.ylabel("Closing price", fontweight="bold")
    plt.title(Symbol, fontweight="bold", fontsize=15)

    return st.pyplot(fig)

if st.button("Charts"):
    st.header("Showing closing price charts")
    for i in com_list:
        plot_data(i)
