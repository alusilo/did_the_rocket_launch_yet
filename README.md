# Did The Rocket Launch Yet?

This bot is initiated by the "/start" command to then send an initial information message. Following
the information message it is send a frame of a rocket launch video within a question, asking
"Did the rocket launch yet?". This question has to be answered as "Yes" or "No" using two buttons.
The intention of this Bot is to answer several times till obtain, using the information given by the user,
the exact frame where the rocket take off. At the end of the search procedure, that use a bisection algorithm,
it is shown a message informing the number of the frame when the rocket was launched.

To check this project in action go to: [DidTheRocketLaunchYet](https://t.me/rocket_took_off_bot).

## Setup

To setup this Bot it is necesary to install requirements as follows

```console
$ pip install -r requirements.txt
```
This will install the following Python libraries:

- flask[async] (vversion == 2.2.2)
- python-telegram-bot (version == 13.14)
- requests (version == 2.28.1)
- python-dotenv(version == 0.21.0)
- gunicorn (vertion == 20.1.0)
- redis (version == 4.3.4)

After that, it is necessary to install Redis in the same server or in other server.

To setup this Bot it is necesary to install it in a dedicated server with a public IP address and SSL configured. In this server
it is necessary to define some environment variables:

```console
$ export MYCHATBOT_TOKEN=BOT_TOKE
$ export MYCHATBOT_USERNAME=BOT_USERNAME
$ export MYCHATBOT_URL=SERVER_HTTPS_URL
$ export REDIS_HOST=REDIS_URL
$ export REDIS_PASSWORD=REDIS_PASSWORD
$ export REDIS_DB=REDIS_DATABASE
$ export REDIS_PORT=REDIS_PORT
$ export VIDEO_URL=https://framex-dev.wadrid.net
$ export VIDEO_NAME="Falcon Heavy Test Flight (Hosted Webcast)-wbSwFU6tY1c"
$ export TOTAL_FRAMES=61695
```

This project was deployed in heroku cloud service following the instructions given at the moment the app is created.
