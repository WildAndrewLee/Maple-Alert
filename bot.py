import asyncio
import subprocess
import sys
import time
from threading import Thread
from textwrap import dedent
from discord import Client, User
from addresses import login_address
from db import add_user, clear_users, get_users, remove_user
from secrets import secrets

if '--debug' in sys.argv:
    __DEBUG__ = True
elif '-d' in sys.argv:
    __DEBUG__ = True
else:
    __DEBUG__ = False

delay = 15000 # 15000ms or 15s
ping_cmd = '{ping} -c 1 {address}'

def check(address):
    ping = subprocess.check_output('which ping', shell=True).strip()
    cmd = ping_cmd.format(**locals())

    if __DEBUG__:
        print(cmd)

    try:
        subprocess.check_output(cmd, shell=True)
        return True
    except:
        return False        

class Bot(object):
    server = None
    channel = None
    client = None

    def __init__(self):
        self.client = Client()

    def alert(self):
        users = get_users()

        for user in users:
            user = User('', user, '', '')
            self.client.send_message(user, 'MapleStory is back online!')

        clear_users()

    def run(self):
        self.client.login(secrets.email, secrets.password)

        @asyncio.coroutine
        @self.client.event
        def on_message(message):
            if message.channel.is_private:
                if message.content == 'cancel':
                    remove_user(message.author)
                    self.client.send_message(
                        message.author,
                        'You have been removed from the alert list.'
                    )
            elif any([m == self.client.user for m in message.mentions]):
                if 'subscribe' in message.content:
                    add_user(message.author)
                    self.client.send_message(
                        message.author,
                        dedent(
                            '''
                            You are now on the alert list.
                            Send "cancel" in private message to remove yourself from the list.
                            '''
                        ).strip()
                    )

                if 'help' in message.content:
                    self.client.send_message(
                        message.channel,
                        dedent(
                            '''
                            This bot will PM you when MapleStory is back online.
                            All inquiries should be sent to Reticence via PM.
                            '''
                        ).strip()
                    )

        thread = Thread(target=self.client.run)
        thread.daemon = True
        thread.start()

        while True:
            if all([check(addr) for addr in login_address]):
                if __DEBUG__:
                    print('maple online')

                self.alert()
            else:
                if __DEBUG__:
                    print('not online')
            
            time.sleep(delay)

bot = Bot()
bot.run()