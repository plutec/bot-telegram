import bot
import os
import random
import time
import settings
import datetime
import koodous

class HispaTroll(bot.TelegramBot):

    def __init__(self):
        random.seed(time.time())
        self.available_images = os.listdir(settings.IMAGES_DIR)
        bot.TelegramBot.__init__(self)

    def _send_tits(self, message):
        """
            Send a random image
        """
        num = random.randrange(0, len(self.available_images))
        path = os.path.join(settings.IMAGES_DIR, self.available_images[num])
        self.send_photo(message.chat_id, path)

    def _send_help(self, message):
        """
            Send commands availables to the group
        """
        self.send_msg(message.chat_id, settings.HELP_TEXT)

    def _send_time(self, message):
        """
            Send the actually time
        """
        self.send_msg(message.chat_id, datetime.datetime.now())

    def _send_matica(self, message):
        """
            Correct text changing 'matica' for a better one
        """
        self.send_msg(message.chat_id, message.text.replace("matica", "matica64"))

    def _send_hash_info(self, message, info):
        msg = """Package name: %s
APP Name: %s
Detected: %s
Developer: %s
""" % (info['package_name'], info['app'], info['detected'],info['company'])
        self.send_msg(message.chat_id, msg)

    def process_update(self, message):
        #print message.get_chat_title()
        if message.get_from_firstname() == 'Carlos' and \
		message.get_text() != 'De grandes como a ti te gustan RAVOSNons ;)' and random.random()>0.5:
            self.send_msg(message.chat_id, "De grandes como a ti te gustan RAVOSNons ;)")
        elif message.get_text() == '/tetas':
            self._send_tits(message)
        elif message.get_text() == '/help':
            self._send_help(message)
        elif message.get_text().startswith('/koodous'):
            try:   
                sha256 = message.get_text().split(' ')[1]
                info = koodous.apk_info(sha256)
                self._send_hash_info(message, info)
            except:
                self.send_msg(message.chat_id, "No entiendo lo que quieres de Koodous")
        elif message.get_text() == '/hora':
            self._send_time(message)
        elif message.get_text() == '/ubre':
            self.send_photo(message.chat_id, 'ubre.jpg')
        elif "matica" in message.get_text() and \
             not "matica64" in message.get_text():
            self._send_matica(message)


def main():
    bot = HispaTroll()
    bot.run()

if __name__ == '__main__':
    main()
