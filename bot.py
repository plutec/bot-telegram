#!/usr/bin/env python

import time
import requests
import settings
import os
import datetime
import random

class Message(object):
    def __init__(self, obj):
        self.obj = obj
        #Extract the most used values
        self.chat_id = self.obj['message']['chat']['id']
        self.update_id = self.obj['update_id']
        self.text = None

    def from_username(self):
        to_ret = self.obj['message']['from'].get('username', None)
        if not to_ret:
            to_ret = self.obj['message']['from']['first_name']
        return to_ret

    def to_username(self):
        return self.get_chat_title()

    def get_chat_id(self):
        return self.chat_id

    def get_text(self):
        if not self.text:
            self.text = self.obj['message']['text']
        return self.text

    def get_chat_title(self):
        to_ret = self.obj['message']['chat'].get('title', None)
        if not to_ret:
            to_ret = self.obj['message']['chat'].get('username', None)
        return to_ret

class TelegramBot:
    def __init__(self):
        self.api = 'https://api.telegram.org/bot%s/' % settings.TOKEN
        self.offset = int(open('offset').read().strip())
        self.me = self.query('getMe')

    def query(self, method, params=None, files=None):
        url = self.api + method
        params = params if params else {}
        res = requests.post(url, params=params, files=files)
        return res.json()

    def updates(self):
        print('Updating')
        data = {'offset': self.offset}
        r = self.query('getUpdates', data)
        for update in r['result']:
            message = Message(update)
            if settings.DEBUG:
                print "[%s->%s]: %s" % (message.from_username(), 
                                       message.to_username(), 
                                       message.get_text())
            self.process_update(message)
            self.offset = message.update_id
            self.offset += 1
        open('offset', 'wt').write('%s' % self.offset)

    def process_update(self, message):
        raise NotImplementedError

    def send_photo(self, chat_id, filename):
        resp = self.query('sendPhoto', params={'chat_id':chat_id},
                                       files= {'photo':open(filename, 'rb')})

    def reply(self, to, msg):
        resp = self.query('sendMessage', {'chat_id': to, 'text': msg})
        return resp

    def run(self):
        while True:
            self.updates()
            time.sleep(1)


class HispaTroll(TelegramBot):

    def __init__(self):
        random.seed(time.time())
        self.available_images = os.listdir(settings.IMAGES_DIR)
        TelegramBot.__init__(self)

    def send_tits(self, message):
        """
            Send a random image
        """
        num = random.randrange(0, len(self.available_images))
        path = os.path.join(settings.IMAGES_DIR, self.available_images[num])
        self.send_photo(message.chat_id, path)

    def send_help(self, message):
        """
            Send commands availables to the group
        """
        self.reply(message.chat_id, settings.HELP_TEXT)

    def send_time(self, message):
        """
            Send the actually time
        """
        self.reply(message.chat_id, datetime.datetime.now())

    def process_update(self, message):
        #print message.get_chat_title()
        if message.get_text().startswith('/tetas'):
            self.send_tits(message)
        elif message.get_text().startswith('/help'):
            self.send_help(message)
        elif message.get_text().startswith('/hora'):
            self.send_time(message)
        elif message.get_text().startswith('/ubre'):
            self.send_photo(message.chat_id, 'ubre.jpg')


def main():
    bot = HispaTroll()
    bot.run()

if __name__ == '__main__':
    main()