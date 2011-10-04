#!/usr/bin/env python

import re
import sys
import gevent
import datetime

from girclib import signals
from girclib.client import IRCClient

class Jeeves(IRCClient):

    def on_privmsg(self, emitter, user=None, message=None):
        self.msg(user.nick, '|{0}|'.format(message))

    def preprocess(self, msg):
        return message.lower().strip()

    def on_chanmsg_to_me(self, emitter, channel=None, user=None, message=None):
        if re.match('.*is it 13:37.*', message):
            now = datetime.datetime.now()
            if (now.hour, now.minute) == (13, 37):
                self.notice(channel, "1337!")
            else:
                self.notice(channel, "No {nick}, it's not 13:37".format(nick=user.nick))
        elif re.match('.*is jpetazzo on a plane ?\?.*', message):
            self.msg(channel, "I'm pretty sure Jerome is on a plane.")

    def on_chanmsg(self, emitter, channel=None, user=None, message=None):
        message = message.lower().strip()
        if message.startswith(self.nickname.lower()):
            return self.on_chanmsg_to_me(emitter, channel, user, message[len(self.nickname):])


def main():
    chan = '#' + sys.argv[1]
    client = Jeeves('irc.freenode.net', 6667, 'jeeves', 'Jeeves')

    @signals.on_signed_on.connect
    def _on_motd(emitter):
        client.join(chan)

    @signals.on_disconnected.connect
    def disconnected(emitter):
        try:
            gevent.shutdown()
        except AssertionError:
            pass

    client.connect()
    try:
        while True:
            gevent.sleep(10)
    except KeyboardInterrupt:
        client.disconnect()


if __name__ == '__main__':
    main()
