import bot
import os
import random
import time
import settings
import datetime

class HispaTroll(bot.TelegramBot):

    def __init__(self):
        random.seed(time.time())
        self.available_images = os.listdir(settings.IMAGES_DIR)
        bot.TelegramBot.__init__(self)

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
        self.send_msg(message.chat_id, settings.HELP_TEXT)

    def send_time(self, message):
        """
            Send the actually time
        """
        self.send_msg(message.chat_id, datetime.datetime.now())

    def send_matica(self, message):
        """
            Correct text changing 'matica' for a better one
        """
        self.send_msg(message.chat_id, message.text.replace("matica", "matica64"))

    def process_update(self, message):
        #print message.get_chat_title()
        if message.get_from_firstname() == 'Carlos' and random.random()>0.5:
            self.send_msg(message.chat_id, "De grandes como a ti te gustan RAVOSNons ;)")
        elif message.get_text() == '/tetas':
            self.send_tits(message)
        elif message.get_text() == '/help':
            self.send_help(message)
        elif message.get_text() == '/hora':
            self.send_time(message)
        elif message.get_text() == '/ubre':
            self.send_photo(message.chat_id, 'ubre.jpg')
        elif "matica" in message.get_text() and \
             not "matica64" in message.get_text():
            self.send_matica(message)


def main():
    bot = HispaTroll()
    bot.run()

if __name__ == '__main__':
    main()
