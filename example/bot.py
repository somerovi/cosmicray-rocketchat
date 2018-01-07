import os
import signal
import sys
import time


import rocketchat

from eliza import eliza, therapist


BOT_ROOM = ''
BOT_USER = ''
BOT_PASS = ''


class Bot(object):
    SLEEP_TIMEOUT = 3

    def __init__(self, room):
        self.me = rocketchat.models.User.me
        self.room = rocketchat.channels()[room]
        signal.signal(signal.SIGINT, self.quit)

    def run(self):
        self.room.send('_greetings! I am here to counsel you. '
                       'No direct messages. Messages must mention @{}_'.format(
                           self.me.name))
        rules = []
        for pattern, transforms in therapist.rules.items():
            pattern = eliza.remove_punct(str(pattern.upper()))
            transforms = [str(t).upper() for t in transforms]
            rules.append((pattern, transforms))

        while True:
            messages = self.room.messages.unread
            for message in messages:
                if self.me != message.user and self.me in message.user_mentions:
                    print(message)
                    response = eliza.respond(
                        rules,
                        eliza.remove_punct(message.msg).upper(),
                        list(map(str.upper, therapist.default_responses))
                    )
                    self.room.send(response)
            time.sleep(Bot.SLEEP_TIMEOUT)

    def quit(self, signum, frame):
        print('quitting')
        sys.exit(0)


if __name__ == '__main__':
    print('CTRL-C to quit')
    rocketchat.configure(config={
        'AUTH_STORE_TOKEN': False,
        'AUTH_CREDS_FROM_ENV': True
    })
    os.environ['RCHAT_USER'] = BOT_USER
    os.environ['RCHAT_PASSWORD'] = BOT_PASS
    bot = Bot(room=BOT_ROOM).run()
