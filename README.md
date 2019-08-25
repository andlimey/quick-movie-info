# QuickMovieInfoBot

* This is a Telegram bot that sends bite-size information about movies that users query for.
* It uses Selenium to query a website for the movie and parses the desired page for information using BeautifulSoup.
* The information that the bot will send are:
    1. Title
    2. Synopsis
    3. Critics Consensus
    4. Tomatometer
    5. Audience Score

## How to use the bot

* Below is a list of commands that the bot will understand

    ### start
    
    ![/start](/img/start_command.png)
    
    ### info
    
    ![/info](/img/info_command.png)
    
    ### find
    
    ![/find](/img/find_command.png)
    
    ### Upon clicking one of the buttons, the bot will send the movie information.
    
    ![Results](/img/results.png)

## Information regarding the project

* The application uses the python-telegram-bot library and is deployed on Heroku
    * requirements.txt file is used to specify dependencies
    * runtime.txt is used to specify the Python version to run
    * Procfile is used to specify the commands that are executed by the app on startup.

* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
* [Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python)
* [Procfile](https://devcenter.heroku.com/articles/procfile)
