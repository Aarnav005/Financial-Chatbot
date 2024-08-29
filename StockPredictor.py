import pandas as pd
from sklearn.linear_model import LinearRegression
import yfinance as yf
import plotly.graph_objects as go
import streamlit as st


def predict(ticker):
    start_date = "2011-01-01"
    end_date = "2024-01-01"
    tbl=yf.download(ticker,start=start_date,end=end_date)
    tbl['Average']=tbl['High']/2 +tbl['Low']/2
    X = tbl['Close'].values.reshape(-1,1)
    y = tbl[['Open','Average']].values
    model = LinearRegression()
    model.fit(X, y)
    y_pred=model.predict(X)
    tbl['Pred_Open']=y_pred[:,0]
    tbl['Pred_Average']=y_pred[:,1]
    tbl['Old_close']=tbl['Close'].shift(1)
    tbl['Old_open']=tbl['Pred_Open'].shift(1)
    tbl['Old_Average']=tbl['Pred_Average'].shift(1)
    tbl = tbl.iloc[1:]
    X = tbl[['Old_open','Old_close','Old_Average']].values
    y = tbl['Close'].values
    model1 = LinearRegression()
    model1.fit(X, y)
    stock_info = yf.Ticker(ticker).info
    cls_price=stock_info.get('currentPrice')
    y_prd=model.predict([[float(cls_price)]])
    a=y_prd[0][0]
    b=y_prd[0][1]
    y_fnl=model1.predict([[a,float(cls_price),b]])
    return y_fnl[0]

def stock_graph(sym):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sym.index, y=sym['Close'].values.flatten()))
    st.plotly_chart(fig)