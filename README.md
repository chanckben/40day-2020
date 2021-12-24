# 40day 2020
Telegram bot hosted on Heroku that pulls data from the 40 Days of Prayer website, https://lovesingapore.org.sg/40day/2020  
Username: @forty_day_bot\
Disclaimer: This is not the original bot for the 40 Days of Prayer. The original bot's username is @LLJ_bot.

To obtain the prayer entry for a particular date:  
1. Enter the command: `\getdateentry`. You will be prompted to enter a date.
2. Type the desired date using the format \<month>\<date>, e.g. July 20.

**Developer Notes**  
- [Python Telegram Bot](https://python-telegram-bot.readthedocs.io/) is used as the intermediary between Telegram's API and the code logic.
- [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/) is used to extract relevant data scraped from the website.
- [Redis database](https://redis-py.readthedocs.io/en/stable/) is used to keep track of unique user IDs when they enter the command `\getdateentry`. When the user enters a valid date afterwards, the user ID will be deleted.
