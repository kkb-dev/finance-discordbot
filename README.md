# finance-discordbot
Python - Financial Webscraper + Discord Bot

1.fndiscord
-Launch discord bot, log in
-import config.py
  -get configuration settings
  
2.Run background task to loop
-Check current time against configuration setting, post time.
  -20 second interval
  
If current time matches post time & Not a weekend or holiday.
  -Run concurrent.py
    -Asynch multiprocessing webscrape script
    -Create workers to asynchronously webscrape data from finviz.com
    -Check stocknames.txt for specific stocks to gather data on
    -Webscrape table into a dictionary
    -Merge table of all stocks into single dictionary
    -Create master text file containing dictionary
  
  -Run rereun.py
    -Check master text file against stocknames to check for missing data.
    -(Data may be lost on poor/wireless connections)
   
  -Run alerts.py
    -Read master text file, use data to create calculations
   
  -Run excel.py
    -Convert master text file into an excel file
  
  -Use data from alerts.py to post to discord (Discord channels directed by configuration settings)
  -Sleep for 1 hour.
