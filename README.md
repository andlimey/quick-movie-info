= QuickMovieInfoBot

* This is a Telegram bot that sends bite-size information about movies that users query for.
* It uses Selenium to query a website for the movie and parses the desired page for information using BeautifulSoup.
* The information that the bot will send are:
** Title
** Synopsis
** Critics Consensus
** Tomatometer
** Audience Score

== Information regarding the project

* The application is deployed on Heroku
** requirements.txt file is used to specify dependencies
** runtime.txt is used to specify the Python version to run
** Procfile is used to specify the commands that are executed by the app on startup.

* [Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python)
* [Procfile](https://devcenter.heroku.com/articles/procfile)
