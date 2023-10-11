# Summary
    Uses Alphavantage REST API to obtain the two previous days stock data for opening and closing. It then uses that data to determine the percentage change in stock market prices between closing and opening.
    It then takes the percentage data and if theres a change greater than 10 percent it pulls an API request from the Newsapiclient for all articles relating to Tesla and the stores the top articles in a dictionary. 
    The program then takes the data, opening value, closing value, percentage difference and news article if applicable and writes them to a csv file using pandas. 

## Libraries/Modules
    import os
    import requests
    import pandas as pd
    
    from datetime import datetime, timedelta
    from newsapi import NewsApiClient


### Usage
    In order to use this app for your own purposes, you will need to change a few items.
      -Update the API tokens with enviornment variables of your own. There are 2 specific API keys:
          -ALPHA_API_KEY
          -NEWS_API_KEY
      

 #### Design implementations
    - Currentlty this has no other functions other than exporting the data to a CSV, however I am going to implement more in the future in accordance with my TODO list found later in this README

##### TODO
    - Create a website with chart flows, that show the current data in a graphical format with changes and a history search
    - Update the python file with all the necessary documentation for each function via the "Docstring Method"



