import json
from typing import Optional
import urllib.parse
import redis
import telegram
from telebot.credentials import BOT_USERNAME, REDIS_HOST, REDIS_DB, \
        REDIS_PORT, REDIS_PASSWORD, VIDEO_URL, VIDEO_NAME, TOTAL_FRAMES, AFFIRMATIVE


class VideoFrameData:
    """ Class to manage data obtained from telegram """

    # attributes
    chat_id: Optional[int] = None
    msg_id: Optional[int] = None
    is_bot: Optional[bool] = None
    lower_frame = 0
    upper_frame = TOTAL_FRAMES - 1
    central_frame = int((lower_frame + upper_frame) / 2)
    answer: Optional[str] = None
    is_cbquery: Optional[bool] = True
    text: Optional[str] = None
    video_url = f"{VIDEO_URL}/api/video/{urllib.parse.quote(VIDEO_NAME)}/frame/{central_frame}/"
    # redis instance
    redis_instance = redis.Redis(host=REDIS_HOST, password=REDIS_PASSWORD, port=REDIS_PORT, db=REDIS_DB)


    def init(self, update: telegram.update.Update) -> None:
        """ Set class attributes from telegram update data """

        # set attributes
        # check if the event is a callback query
        self.is_cbquery = False if update.callback_query is None else True
        if self.is_cbquery:
            update = update.callback_query
            self.chat_id = update.message.chat.id
            self.msg_id = update.message.message_id
            self.is_bot = update.message.from_user.is_bot
            self.text = None
        else:
            self.chat_id = update.message.chat.id
            self.msg_id = update.message.message_id
            self.is_bot = update.message.from_user.is_bot
            self.text = None if update.message.text is None else update.message.text.encode('utf-8').decode()


    def delete_redis_data(self) -> None:
        """ Delete Radis data """

        # reset video attributes and user answer
        self.lower_frame = 0
        self.upper_frame = TOTAL_FRAMES - 1
        self.central_frame = int((self.lower_frame + self.upper_frame) / 2)
        self.answer = None
        self.video_url = f"{VIDEO_URL}/api/video/{urllib.parse.quote(VIDEO_NAME)}/frame/{self.central_frame}/"

        # delete redis data
        self.redis_instance.delete(f'{BOT_USERNAME}_{self.chat_id}')
    

    def read_redis_data(self) -> None:
        """ Read Redis data """
        data = self.redis_instance.get(f'{BOT_USERNAME}_{self.chat_id}')
        # change attributes if data read from Redis is not None
        if data is not None:
            # load data in dictionary
            loaded_data = json.loads(data.decode('utf-8'))
            # update attributes
            self.chat_id = loaded_data['chat_id']
            self.msg_id  = loaded_data['msg_id']
            self.is_bot = loaded_data['is_bot']
            self.lower_frame = loaded_data['lower_frame']
            self.upper_frame = loaded_data['upper_frame']
            self.central_frame = int((self.lower_frame + self.upper_frame) / 2)
            self.answer = loaded_data['answer']
            self.video_url = f"{VIDEO_URL}/api/video/{urllib.parse.quote(VIDEO_NAME)}/frame/{self.central_frame}/"
    

    def update_redis_data(self, msg_id: int, markup_response: str) -> None:
        # encode and decode response
        self.answer = markup_response.encode('utf-8').decode()
        # bisection algorithm
        # if answer is affirmative
        if self.answer == AFFIRMATIVE:
            # upper frame is now the central frame
            self.upper_frame = self.central_frame
        else:
            # lower frame is now the central frame
            self.lower_frame = self.central_frame
        # according to new lower and upper frames are modified the attributes
        self.msg_id = msg_id
        self.central_frame = int((self.lower_frame + self.upper_frame) / 2)
        self.video_url = f"{VIDEO_URL}/api/video/{urllib.parse.quote(VIDEO_NAME)}/frame/{self.central_frame}/"
        # data serialization
        serializer = json.dumps({
            'chat_id': self.chat_id,
            'msg_id': self.msg_id,
            'is_bot': self.is_bot,
            'lower_frame': self.lower_frame,
            'upper_frame': self.upper_frame,
            'answer': self.answer
        })
        # data stored or updated in Redis table
        self.redis_instance.set(f'{BOT_USERNAME}_{self.chat_id}', serializer)
