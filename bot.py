import asyncio
import socket
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

delay = 5 # 5 seconds

def check(address):
    addr = address.split(':')[0]
    port = address.split(':')[1]
    
    try:
        # 0.5 second timeout
        s = socket.create_connection((addr, port), 0.5)
        s.close()
        return True
    except:
        return False

client = Client()
client.login(secrets.email, secrets.password)

@asyncio.coroutine
@client.event
def on_alert():
    users = get_users()

    for user in users:
        user = User('', user, '', '')
        client.send_message(user, 'MapleStory is back online!')

    clear_users()

@asyncio.coroutine
@client.event
def on_message(message):
    if message.channel.is_private:
        if message.content == 'cancel':
            remove_user(message.author)
            client.send_message(
                message.author,
                'You have been removed from the alert list.'
            )
    elif any([m == client.user for m in message.mentions]):
        if 'subscribe' in message.content:
            add_user(message.author)
            client.send_message(
                message.author,
                dedent(
                    '''
                    You are now on the alert list.
                    Type "cancel" to remove yourself from the list.
                    '''
                ).strip()
            )

        if 'help' in message.content:
            client.send_message(
                message.channel,
                dedent(
                    '''
                    This bot will PM you when MapleStory is back online.
                    All inquiries should be sent to Reticence via PM.

                    Usage:
                    @Maple Alert subscribe
                    @Maple Alert help
                    '''
                ).strip()
            )

def check_servers():
    while True:
        # let the discord client connect
        time.sleep(delay)

        if any([check(addr) for addr in login_address]):
            if __DEBUG__:
                print('maple online')

            client.dispatch('alert')
        else:
            if __DEBUG__:
                print('not online')

checker = Thread(target=check_servers)
checker.daemon = True
checker.start()

client.run()