"""
This bot search for the exact frame of a video where a rocket launched.
"""
import time
from flask import Flask, request
import telegram
from telebot.credentials import BOT_TOKEN, BOT_URL, AFFIRMATIVE, NEGATIVE
from telebot.model import VideoFrameData

# Bot instance
bot = telegram.Bot(token=BOT_TOKEN)

# Flask instance
app = Flask(__name__)

# VideoFrame instance
bot_data = VideoFrameData()

# question replay markup
reply_markup = telegram.InlineKeyboardMarkup([
    [telegram.InlineKeyboardButton('Yes', callback_data=AFFIRMATIVE)],
    [telegram.InlineKeyboardButton('No', callback_data=NEGATIVE)]
])

# Bot route function
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
async def response() -> dict:
    """
    Asynchroneous function to manage responses to user messages. This function
    reads out the information given by the telegram API through `telegram.update.Update`
    and obtains chat and message information to then process the text given by
    the user. If the given text is "/start" command the Bot send an information message
    and send a frame of a rocket launch video within a question, asking "Did the rocket launch yet?",
    to be answered as "Yes" or "No" using two buttons. The intention of this Bot is to obtain,
    using the information given by the user, the exact frame where the rocket take off. At the end
    of the search procedure, that use a bisection algorithm, it is shown a message informing
    the number of the frame.
    """
    # update data from telegram message
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    # initialize VideoFrameData instance
    bot_data.init(update)
    # check if event is a callback query
    if bot_data.is_cbquery:
        # read redis data
        bot_data.read_redis_data()
        msg_id = update.callback_query.message.message_id
        markup_response = update.callback_query.data
        if msg_id > bot_data.msg_id or bot_data.answer is None:
            # update redis data
            bot_data.update_redis_data(msg_id, markup_response)
            # Bot get the take off frame if central frame is equal to lower frame or if central frame is equal to upper frame
            if bot_data.central_frame == bot_data.lower_frame or bot_data.central_frame == bot_data.upper_frame:
                time.sleep(1.5)
                bot.sendMessage(
                    chat_id=bot_data.chat_id,
                    text=f"<b>The frame where the rocket launched is the {bot_data.central_frame} frame.</b>",
                    parse_mode='HTML'
                )
            else:
                try:
                    # send photo
                    bot.sendChatAction(chat_id=bot_data.chat_id, action="upload_photo")
                    time.sleep(2)
                    bot.sendPhoto(chat_id=bot_data.chat_id, photo=bot_data.video_url)
                    question_text = "<i>Did the rocket launch yet?</i>"
                    # send question
                    bot.sendChatAction(chat_id=bot_data.chat_id, action="typing")
                    time.sleep(1.5)
                    bot.sendMessage(
                        chat_id=bot_data.chat_id,
                        text=question_text,
                        parse_mode='HTML',
                        disable_web_page_preview=True,
                        reply_markup=reply_markup
                    )
                except Exception as error:
                    bot.sendChatAction(chat_id=bot_data.chat_id, action="typing")
                    time.sleep(1.5)
                    bot.sendMessage(
                        chat_id=bot_data.chat_id,
                        text=f'Other error: {error}'
                    )

        return {'status': 'question answered'}, 200
    else:
        # command to start asking if did the rocket launch yet
        if bot_data.text == '/start' and not bot_data.is_bot:
            # deleted redis data
            bot_data.delete_redis_data()
            # bot welcome message
            bot_welcome = """
            <b>Welcome to DidTheRocketLaunchYet!</b>.
This bot send photos for a rocket launch and ask for the time the rocket is launched,
when flames are evident at the base of the rocket. Contact <a href="https://t.me/alusilo">@alusilo</a>
if you have any question about this Bot.
            """
            bot_welcome = bot_welcome.strip().replace('\n', ' ')
            # send welcome message to user
            bot.sendChatAction(chat_id=bot_data.chat_id, action="typing")
            time.sleep(1.5)
            bot.sendMessage(
                chat_id=bot_data.chat_id,
                text=bot_welcome,
                disable_web_page_preview=True,
                parse_mode='HTML'
            )
            try:
                # send photo
                bot.sendChatAction(chat_id=bot_data.chat_id, action="upload_photo")
                time.sleep(2)
                bot.sendPhoto(chat_id=bot_data.chat_id, photo=bot_data.video_url)
                question_text = "<i>Did the rocket launch yet?</i>"
                # send question
                bot.sendChatAction(chat_id=bot_data.chat_id, action="typing")
                time.sleep(1.5)
                bot.sendMessage(
                    chat_id=bot_data.chat_id,
                    text=question_text,
                    parse_mode='HTML',
                    disable_web_page_preview=True,
                    reply_markup=reply_markup
                )
            except Exception as error:
                # send if any error occurs
                bot.sendChatAction(chat_id=bot_data.chat_id, action="typing")
                time.sleep(1.5)
                bot.sendMessage(
                    chat_id=bot_data.chat_id,
                    text=f'Other error: {error}'
                )
        return {'status': 'you are a bot' if bot_data.is_bot else 'ok'}, 200


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook() -> tuple:
    """
    Function to setup Web Hook.
    """
    wh_setup = bot.setWebhook(f'{BOT_URL}{BOT_TOKEN}')
    status = 'webhook setup ok' if wh_setup else 'webhook setup failed'
    return {'status': status}, 200


@app.route('/')
def index() -> tuple:
    """
    Main view of the Bot App.
    """
    return {'status': 'ok'}, 200


if __name__ == '__main__':
    app.run(threaded=True)
