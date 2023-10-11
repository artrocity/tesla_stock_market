# Import libraries
import os
import requests
import pandas as pd

from datetime import datetime, timedelta
from newsapi import NewsApiClient


def main():
    stock_data = get_stock_api_data()
    percentage_difference, news_data = compare_trading_days(stock_data)
    if percentage_difference > 10:
        write_to_csv(stock_data, percentage_difference, news_data)
    else:
        write_to_csv(stock_data, percentage_difference)


def get_stock_api_data() ->dict:
    # Fetch stock data
    ALPHA_API_KEY = os.environ.get("ALPHA_API_KEY")
    stock_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY"
    stock_parameters = {
        "apikey": ALPHA_API_KEY,
        "symbol" : "TSLA"
    }
    try:
        stock_response = requests.get(stock_url, params=stock_parameters)
        stock_response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching stock data: {e}")
        return None
    stock_data = stock_response.json()
    
    # Get todays and yesterdays date
    day_before_yesterday = datetime.today() - timedelta(days=2)
    day_before_yesterdays_date = day_before_yesterday.strftime("%Y-%m-%d")
    yesterday = datetime.today() - timedelta(days=1)
    yesterdays_date = yesterday.strftime("%Y-%m-%d")
    
    # Ensure dates are in the data prior to accessing them
    if day_before_yesterdays_date not in stock_data["Time Series (Daily)"]:
        print(f"No stock data found for {day_before_yesterdays_date}")
        return None
    if yesterdays_date not in stock_data["Time Series (Daily)"]:
        print(f"No stock data found for {yesterdays_date}")
        return None
    
    # Create an empty dictionary to return
    stock_daily_dict = {}
    if day_before_yesterdays_date in stock_data["Time Series (Daily)"]:
        stock_daily_dict[day_before_yesterdays_date] = {
            "Daily Open" : float(stock_data["Time Series (Daily)"][day_before_yesterdays_date]["1. open"]),
            "Daily Close" : float(stock_data["Time Series (Daily)"][day_before_yesterdays_date]["4. close"])
        }
    if yesterdays_date in stock_data["Time Series (Daily)"]:
        stock_daily_dict[yesterdays_date] = {
            "Daily Open" : float(stock_data["Time Series (Daily)"][yesterdays_date]["1. open"]),
            "Daily Close" : float(stock_data["Time Series (Daily)"][yesterdays_date]["4. close"])
        }
   
    return stock_daily_dict


def compare_trading_days(stock_data: dict):
    # Get todays and yesterdays date
    day_before_yesterday = datetime.today() - timedelta(days=2)
    day_before_yesterdays_date = day_before_yesterday.strftime("%Y-%m-%d")
    yesterday = datetime.today() - timedelta(days=1)
    yesterdays_date = yesterday.strftime("%Y-%m-%d")

    day_before_close = stock_data[day_before_yesterdays_date]["Daily Close"]
    prev_day_open = stock_data[yesterdays_date]["Daily Open"]

    #Calculate and check if there's a 10% difference between the two
    difference = abs(day_before_close - prev_day_open)
    percentage_difference = (difference / day_before_close) * 100

    if percentage_difference > 10:
        news = get_news_data()
        return percentage_difference, news
    else:
        return percentage_difference, None

def get_news_data() -> dict:
    NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
    print(NEWS_API_KEY)
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    try:
        top_headlines = newsapi.get_top_headlines(q='Tesla',
                                              language='en',
                                              country='us')
    except Exception as e:
        print("Error: ", str(e))
    
    articles = top_headlines.get("articles", [])
    if articles:
        article = articles[0]
        news_data = {
            "title" : article.get("title"),
            "description" : article.get("description"),
            "url" : article.get("url")
        }
        return news_data
    else:
        return {}


def write_to_csv(stock_data: dict, percentage_difference: float, news: dict = None) -> None:   
    columns = ["Date", "Open", "Close", "Percentage Difference", "News Article"]
    dates = list(stock_data.keys())
    latest_day = stock_data[dates[1]]
    
    # Prepare data for dataframe
    data = {
        "Date" : dates[1],
        "Open" : latest_day["Daily Open"],
        "Close" : latest_day["Daily Close"],
        "Percentage Difference" : percentage_difference,
        "News Article" : news.get("title", "") if news else None
    }

    # Create a new DataFrame
    new_data_df = pd.DataFrame([data], columns=columns)

    # Append new data to the existing CSV
    if not pd.io.common.file_exists("tesla_stock_data.csv"):
        new_data_df.to_csv("./tesla_stock_data.csv", mode="a", index=False)
    else:
        new_data_df.to_csv("./tesla_stock_data.csv", mode="a", index=False, header=False)


if __name__ == "__main__":
    main()
