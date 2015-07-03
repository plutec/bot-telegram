#!/usr/bin/env python

import requests
import settings
import time

class Message(object):
    NORMAL_MESSAGE = 1
    JOIN_GROUP = 2
    LEFT_GROUP = 3

    def __init__(self, obj):
        self.obj = obj
        #Extract the most used values
        self.chat_id = self.obj['message']['chat']['id']
        self.update_id = self.obj['update_id']
        self.text = None
        self.type = self.NORMAL_MESSAGE
        if self.obj['message'].has_key('new_chat_participant'):
            self.type = self.JOIN_GROUP
        elif self.obj['message'].has_key('left_chat_participant'):
            self.type = self.LEFT_GROUP
        print "OBJ %s" % str(obj)

    def from_username(self):
        to_ret = self.obj['message']['from'].get('username', None)
        if not to_ret:
            to_ret = self.obj['message']['from']['first_name']
        return to_ret

    def from_id(self):
	return self.obj['message']['chat']['id']

    def get_left_chat_username(self):
	try:
	    return self.obj['message']['left_chat_participant']['username']
	except:
	    try:
		return self.obj['message']['left_chat_participant']['first_name']
	    except:
		return ""

    def to_username(self):
        chat_title = self.get_chat_title()
	if chat_title == self.from_username():
	    return "Me" 
	return self.get_chat_title()

    def get_chat_id(self):
        return self.chat_id

    def get_text(self):
        if self.type != self.NORMAL_MESSAGE:
            return ""
        if not self.text:
            try:
                self.text = self.obj['message']['text']
            except:
                self.text = ""
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

    def allowed(self, message):
	if message.type == Message.NORMAL_MESSAGE:
	    return message.from_id() in settings.ALLOWED_CHATS
	return False

    def updates(self):
        data = {'offset': self.offset}
        r = self.query('getUpdates', data)
        for update in r['result']:
            message = Message(update)
            if settings.DEBUG:
                if message.type == Message.NORMAL_MESSAGE:
                    print "[%s->%s]: %s" % (message.from_username(),
                                           message.to_username(),
                                           message.get_text())
                elif message.type == Message.JOIN_GROUP:
                    print "%s JOIN GROUP %s" % \
                        (update['message']['new_chat_participant']['username'],
                         message.get_chat_title())
                elif message.type == Message.LEFT_GROUP:
                    print "%s LEFT GROUP %s" % \
                        (message.get_left_chat_username(),
                         message.get_chat_title())
	    if self.allowed(message):
            	self.process_update(message)
	    else:
		self.send_msg(message.chat_id, "Quiero irme, no estoy agusto")
            self.offset = message.update_id
            self.offset += 1
        open('offset', 'wt').write('%s' % self.offset)

    def process_update(self, message):
        raise NotImplementedError

    def send_photo(self, chat_id, filename):
        resp = self.query('sendPhoto', params={'chat_id':chat_id},
                                       files= {'photo':open(filename, 'rb')})

    def send_msg(self, to, msg):
        resp = self.query('sendMessage', {'chat_id': to, 'text': msg})
        return resp

    def run(self):
        while True:
            self.updates()
            time.sleep(1)
