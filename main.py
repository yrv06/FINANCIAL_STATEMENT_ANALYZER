import yfinance as yf
import pandas as pd


tickers = []
n = int(input("for analysis of 1 company enter : 1 , for comparison between 2 or more enter no. of company"))
for i in range(n):
      com_name = input("enter company's name")
      tickers.append(com_name)



#  Fields to collect (including currentPrice and financial data)
fields = [
    "shortName", "symbol", "sector", "industry", "marketCap",
    "trailingPE", "forwardPE", "dividendYield", "returnOnEquity",
    "bookValue", "priceToBook", "fiftyTwoWeekHigh", "fiftyTwoWeekLow",
    "beta", "previousClose", "open", "dayHigh", "dayLow",
    "currentPrice"  # Stock current price
    
]

#  Fetch data
data = []

for ticker in tickers:
    stock = yf.Ticker(ticker)
    info = stock.info
    financials = stock.financials
    balance_sheet = stock.balance_sheet
    
    # Extract financial fields
    try:
        net_income = financials.loc['Net Income'].iloc[0] if 'Net Income' in financials.index else None
        total_revenue = financials.loc['Total Revenue'].iloc[0] if 'Total Revenue' in financials.index else None
        current_assets = balance_sheet.loc['Current Assets'].iloc[0] if 'Current Assets' in balance_sheet.index else None
        current_liabilities = balance_sheet.loc['Current Liabilities'].iloc[0] if 'Current Liabilities' in balance_sheet.index else None
        total_assets = balance_sheet.loc['Total Assets'].iloc[0] if 'Total Assets' in balance_sheet.index else None
        previous_total_assets = balance_sheet.loc['Total Assets'].iloc[1] if len(balance_sheet.loc['Total Assets']) > 1 else None
        average_total_assets = (total_assets + previous_total_assets) / 2 if total_assets and previous_total_assets else None
    except KeyError as e:
        # If any of the fields are not found, set them to None
        net_income, total_revenue, current_assets, current_liabilities, average_total_assets = [None] * 5

    # Add the requested data fields to the row

    net_profit_margin = (net_income / total_revenue) * 100 if net_income and total_revenue else None
    current_ratio = (current_assets/current_liabilities)if current_assets  and current_liabilities else None
    asset_turnover_ratio = (total_revenue/ average_total_assets)if total_revenue and average_total_assets  else None
      #Determine financial health
    if current_ratio and asset_turnover_ratio and net_profit_margin:
        if 1.5 <= current_ratio <= 3 and asset_turnover_ratio > 0.5 and net_profit_margin > 10:
            health = "Healthy"
        elif current_ratio < 1 or asset_turnover_ratio < 0.3 or net_profit_margin < 5:
            health = "High Risk"
        else:
            health = "Moderate Risk"
    else:
        health = "Insufficient Data"
    row = {field: info.get(field, None) for field in fields if field != "Net Income" and field != "Total Revenue" and field != "Current Assets" and field != "Current Liabilities" and field != "Total Assets"}
    
    # Add financial data to row
    row.update({
        "Net Income": net_income,
        "Total Revenue": total_revenue,
        "Current Assets": current_assets,
        "Current Liabilities": current_liabilities,
        "Average Total Assets": total_assets,
        "Net Profit Margin (%)": net_profit_margin, 
        "Current Ratio" : current_ratio,
        "Asset Turnover Ratio" : asset_turnover_ratio,          
        "Financial Health": health
    })

    data.append(row)

#  Create DataFrame
df = pd.DataFrame(data)

#  Display
pd.set_option('display.max_columns', None)

df[["symbol","marketCap","currentPrice","fiftyTwoWeekHigh","fiftyTwoWeekLow","Net Profit Margin (%)", "Current Ratio","Asset Turnover Ratio","Financial Health" ]]  
