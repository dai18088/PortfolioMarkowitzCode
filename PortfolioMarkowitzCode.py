#Portfolio Markowitz

#For to use Ln

import numpy as np
import pandas as pd
#Data Source
import yfinance as yf
#For Average,Variance and Standard deviation
from statistics import mean
from statistics import variance
from statistics import stdev
import math

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import plotting
import tkinter as tk
#from tkinter import ttk
#from tkinter import *
import tkinter.messagebox


my_w = tk.Tk()

my_w.geometry("900x700") # Size of the window

my_w.title("Portfolio Markowitz") # title

assets_All = []

  

#The user enter the number of Stocks for Dow Jones
#number_stocks_DowJones = int(input('Please enter the number of stocks in Dow Jones: '))

labelNumberStocksDowJones = tk.Label(my_w,text='Please enter the number of stocks in Dow Jones:', font=20, fg='blue')
labelNumberStocksDowJones.grid(row=0, column=0, padx=10)

entryNumberStocksDowJones = tk.Entry(my_w, font=20, bg='lightyellow')
entryNumberStocksDowJones.grid(row=0,column=1, padx=10, pady=10)


#The user enter the number of Stocks for Nasdaq
#number_stocks_Nasdaq = int(input('Please enter the number of stocks in Nasdaq: '))

labelNumberStocksNasdaq = tk.Label(my_w,text='Please enter the number of stocks in Nasdaq:', font=20, fg='blue')
labelNumberStocksNasdaq.grid(row=1, column=0, padx=10)

entryNumberStocksNasdaq = tk.Entry(my_w, font=20, bg='lightyellow')
entryNumberStocksNasdaq.grid(row=1,column=1, padx=10, pady=10)


refDowJones = []
refNasdaq = []

def funEnterNumberOfStocks():
    number_stocks_DowJones = int(entryNumberStocksDowJones.get())
    number_stocks_Nasdaq = int(entryNumberStocksNasdaq.get())

    if (number_stocks_DowJones==1 and number_stocks_Nasdaq==1):
        tkinter.messagebox.showinfo("Error Message", "Please not enter 1 or 0 stock in Dow Jones and Nasdaq. You should enter under a 2 stocks")
    elif (number_stocks_DowJones==0 and number_stocks_Nasdaq==0):
        tkinter.messagebox.showinfo("Error Message", "Please not enter 1 or 0 stock in Dow Jones and Nasdaq. You should enter under a 2 stocks")
    elif (number_stocks_DowJones==1 and number_stocks_Nasdaq==0):
        tkinter.messagebox.showinfo("Error Message", "Please not enter 1 or 0 stock in Dow Jones and Nasdaq. You should enter under a 2 stocks")
    elif (number_stocks_DowJones==0 and number_stocks_Nasdaq==1):
        tkinter.messagebox.showinfo("Error Message", "Please not enter 1 or 0 stock in Dow Jones and Nasdaq. You should enter under a 2 stocks")
    else :
        #For, that read from User the Ticker in Dow Jones
        for i in range(0,number_stocks_DowJones):
        
            labelTickerDowJones = tk.Label(my_w,text='Enter a ticker of Dow Jones' + str(i+1), font=20, fg='blue')
            labelTickerDowJones.grid(row=i+3, column=0, padx=10)

            entryTickerDowJones = tk.Entry(my_w, font=20, bg='lightyellow')
            entryTickerDowJones.grid(row=i+3,column=1, padx=10, pady=10)

            refDowJones.append(entryTickerDowJones)
        
        #For, that read from User the Ticker in Nasdaq        
        for i in range(0,number_stocks_Nasdaq):
        
            labelTickerNasdaq = tk.Label(my_w,text='Enter a ticker of Nasdaq:' + str(i+1), font=20, fg='blue')
            labelTickerNasdaq.grid(row=i+number_stocks_DowJones+4, column=0, padx=10)

            entryTickerNasdaq = tk.Entry(my_w, font=20, bg='lightyellow')
            entryTickerNasdaq.grid(row=i+number_stocks_DowJones+4,column=1, padx=10, pady=10)

            refNasdaq.append(entryTickerNasdaq)
    
         


buttonOk = tk.Button(my_w, text="ENTER NUMBER OF STOCKS",bg='lightgreen', font=20, command=funEnterNumberOfStocks)
buttonOk.grid(row=2, column=1, padx=10, pady=5)



def funCalculator(refDowJones, refNasdaq):
    
    
     #Here I reading the indexes of Market Stock
    Data_Index = [[],[]]
    DataLn_Index = [[],[]]
    dataDowJones = yf.download(tickers="^DJI", period='1y', interval='1d')
    dataNasdaq = yf.download(tickers="^IXIC", period='1y', interval='1d')
    #In DataIndex[0] is the Dow Jones
    for j in range(0,len(dataDowJones['Close'])):
        Data_Index[0].append(dataDowJones['Close'][j])

    #In DataIndex[1] is the Nasdaq
    for j in range(0,len(dataNasdaq['Close'])):
        Data_Index[1].append(dataNasdaq['Close'][j])

        
    #Create a Dynamic List with number of stocks
    Data_DowJones = [[] for a in range(len(refDowJones))]
    Data_Nasdaq = [[] for b in range(len(refNasdaq))]

    #Create a Dynamic List with logarithmic performance
    DataLn_DowJones = [[] for c in range(len(refDowJones))]
    DataLn_Nasdaq = [[] for d in range(len(refNasdaq))]


    #Dynamic List for Average,Variance,Standard deviation and Coefficient Of Variation for Dow Jones
    DataAverage_DowJones = [[] for e in range(len(refDowJones))]
    DataVariance_DowJones = [[] for f in range(len(refDowJones))]
    DataStdev_DowJones = [[] for g in range(len(refDowJones))]
    DataCoefficientOfVariation_DowJones = [[] for h in range(len(refDowJones))]

    #Dynamic List for Average,Variance,Standard deviation and Coefficient Of Variation for Nasdaq
    DataAverage_Nasdaq = [[] for j in range(len(refNasdaq))]
    DataVariance_Nasdaq = [[] for g in range(len(refNasdaq))]
    DataStdev_Nasdaq = [[] for k in range(len(refNasdaq))]
    DataCoefficientOfVariation_Nasdaq = [[] for l in range(len(refNasdaq))]

    #Dynamic List for Beta and Alpha of Dow Jones
    Slope_Beta_DowJones = [[] for m in range(len(refDowJones))]
    Intercept_Alfa_DowJones = [[] for n in range(len(refDowJones))]

    #Dynamic List for Beta and Alpha of Nasdaq
    Slope_Beta_Nasdaq = [[] for o in range(len(refNasdaq))]
    Intercept_Alfa_Nasdaq = [[] for p in range(len(refNasdaq))]

    #Dynamic List for Covariance Matrix
    #DataCovMatrix = []
    DataCovMatrix_DowJones = []
    DataCovMatrix_Nasdaq = []

    #Isomere Portfolio
    Eq_Portfolio = []
    
    
    df = pd.DataFrame()
    
    
    assets_DowJones = []
    assets_Nasdaq = []
    count_DowJones = 0
    count_Nasdaq = 0
    
    for w in refDowJones:
        assets_DowJones.append(w.get().upper())
        
        #Read Data from Yahoo Finance for 1 year
        data = yf.download(tickers = assets_DowJones[count_DowJones], period='1y', interval='1d')
    
        df[count_DowJones] = data['Close']
    
        #For, that puts the data['Close'] in Dynamic List: Data
        for j in range(0,len(data['Close'])):
            Data_DowJones[count_DowJones].append(data['Close'][j])
            
        count_DowJones = count_DowJones + 1
    
    
    for x in refNasdaq:
        assets_Nasdaq.append(x.get().upper())
        
        #Read Data from Yahoo Finance for 1 year
        data = yf.download(tickers = assets_Nasdaq[count_Nasdaq], period='1y', interval='1d')
    
        df[count_Nasdaq+count_DowJones] = data['Close']
    
        #For, that puts the data['Close'] in Dynamic List: Data
        for j in range(0,len(data['Close'])):
            Data_Nasdaq[count_Nasdaq].append(data['Close'][j])
            
        count_Nasdaq = count_Nasdaq + 1
    
    assets_All = assets_DowJones + assets_Nasdaq
    #print(assets_All)
    
    
    
    #Here I calculate the logarithmic performance for Stocks in Dow Jones        
    for i in range(0,len(Data_DowJones)):   
        for k in range(0,len(Data_DowJones[i])-1):
            DataLn_DowJones[i].append(math.log(Data_DowJones[i][k+1]/Data_DowJones[i][k]))

    #Here I calculate the logarithmic performance for Stocks in Nasdaq
    for i in range(0,len(Data_Nasdaq)):   
        for k in range(0,len(Data_Nasdaq[i])-1):
            DataLn_Nasdaq[i].append(math.log(Data_Nasdaq[i][k+1]/Data_Nasdaq[i][k]))

        
    #Here I calculate the logarithmic performance for Indexes        
    for i in range(0,len(Data_Index)):   
        for k in range(0,len(Data_Index[i])-1):
            DataLn_Index[i].append(math.log(Data_Index[i][k+1]/Data_Index[i][k]))

        
    #Here I calculate Average,Variance and Standard deviation for Dow Jones    
    for i in range(0,len(DataLn_DowJones)):
        DataAverage_DowJones[i] = mean(DataLn_DowJones[i])
        DataVariance_DowJones[i] = variance(DataLn_DowJones[i]) 
        DataStdev_DowJones[i] = stdev(DataLn_DowJones[i])

 

    #Here I calculate Average,Variance and Standard deviation for Nasdaq  
    for i in range(0,len(DataLn_Nasdaq)):
        DataAverage_Nasdaq[i] = mean(DataLn_Nasdaq[i])
        DataVariance_Nasdaq[i] = variance(DataLn_Nasdaq[i]) 
        DataStdev_Nasdaq[i] = stdev(DataLn_Nasdaq[i])
 

     #Here I calculate Coefficient Of Variation for Dow Jones
    for i in range(0,len(DataAverage_DowJones)):
        DataCoefficientOfVariation_DowJones[i] = DataStdev_DowJones[i]/DataAverage_DowJones[i] 


    #Here I calculate Coefficient Of Variation for Nasdaq
    for i in range(0,len(DataAverage_Nasdaq)):
        DataCoefficientOfVariation_Nasdaq[i] = DataStdev_Nasdaq[i]/DataAverage_Nasdaq[i]  
           

        
    #Calculate Beta and Alpha of Stocks in Dow Jones
    for i in range(0,len(DataLn_DowJones)):
        Slope_Beta_DowJones[i], Intercept_Alfa_DowJones[i] = np.polyfit(DataLn_Index[0],DataLn_DowJones[i],1)
    
    
    #Calculate Beta and Alpha of Stocks in Nasdaq
    for i in range(0,len(DataLn_Nasdaq)):
        Slope_Beta_Nasdaq[i], Intercept_Alfa_Nasdaq[i] = np.polyfit(DataLn_Index[1],DataLn_Nasdaq[i],1)


    #Calculate Cov Matrix Dow Jone
    covMatrix_DowJones = np.cov(DataLn_DowJones,bias=True)

    #Calculate Cov Matrix Nasdaq
    covMatrix_Nasdaq = np.cov(DataLn_Nasdaq,bias=True)


    
    #Merge All Data    
    AllData = DataLn_DowJones + DataLn_Nasdaq

    #Calculate Cov Matrix for All Data
    covMatrix_AllData = np.cov(AllData,bias=True)


    total_stocks = len(refDowJones) + len(refNasdaq)
    m = (100/total_stocks)/100

    for i in range(0,total_stocks):
        Eq_Portfolio.append(m)
        #weights = np.array

    All_Average = DataAverage_DowJones + DataAverage_Nasdaq
    for i in range(0,total_stocks):
        #Anamenomenh Apodosh
        Expected_Performance = Eq_Portfolio[i] * All_Average[i]
    
    
    weight = np.array(Eq_Portfolio)


    #Diakymansh
    port_variance = np.dot(weight.T,np.dot(covMatrix_AllData,weight))

    #Typikh Apoklhsh
    port_volatility = np.sqrt(port_variance)
    
    
    
    # Portfolio Optimization
    # Calculate the expected returns and the annualized sample covariance matrix of asset returns
    mu = expected_returns.mean_historical_return(df)

    # Optimize for maximum sharpe ratio
    ef = EfficientFrontier(mu, covMatrix_AllData, weight_bounds=(None,None))
    #ef.add_constraint(lambda w: w[0]+w[1]+w[2] == 1)
    ef.add_constraint(lambda w: w >= 0.01)
    #ef.add_constraint(lambda w: w <= 0.25)
    #ef.add_constraint(lambda w: w <= 0.09)
    weight = ef.min_volatility()
    #weight = ef.max_sharpe()
    cleaned_weights = ef.clean_weights() 
    #print(cleaned_weights)
    ef.portfolio_performance(verbose=True)


    labelBeta = tk.Label(my_w,text= "Beta", font=20, fg='blue')
    labelBeta.grid(row=len(refDowJones)+len(refNasdaq)+5, column=2, padx=10)


    AllBeta = Slope_Beta_DowJones + Slope_Beta_Nasdaq


    for i in range(0,len(refDowJones) + len(refNasdaq)):
        #print(assets_All[i],':',"{:.2f}".format(cleaned_weights[i]*100),'%')
        ticker = assets_All[i]
        
        labelName = tk.Label(my_w,text= ticker, font=20, fg='blue')
        labelName.grid(row=i+len(refDowJones)+len(refNasdaq)+8, column=0, padx=10)
        
        m = "{:.2f}".format(cleaned_weights[i]*100),'%'
        
        labelPrice = tk.Label(my_w,text= m, font=20, fg='blue')
        labelPrice.grid(row=i+len(refDowJones)+len(refNasdaq)+8, column=1, padx=10)

        beta = "{:.3f}".format(AllBeta[i])
        labelBetaPrice = tk.Label(my_w,text= beta, font=20, fg='blue')
        labelBetaPrice.grid(row=i+len(refDowJones)+len(refNasdaq)+8, column=2, padx=10)



buttonCalculate = tk.Button(my_w, text="CALCULATE",bg='lightgreen', font=20, command=lambda: funCalculator(refDowJones, refNasdaq))
buttonCalculate.grid(row=200, column=1, padx=10, pady=5)


my_w.mainloop() # Keep the window open