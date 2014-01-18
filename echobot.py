#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import argparse
import configparser
import os.path

import sleekxmpp


class EchoBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler('message', self.message)
        self.add_event_handler('session_start', self.start)

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            msg.reply(msg['body']).send()

    def start(self, event):
        self.send_presence()

if __name__ == '__main__':

    p = argparse.ArgumentParser()
    p.add_argument('-c', '--config', nargs='?', default=os.path.expanduser('~/.xmpputils'), type=argparse.FileType('r'))
    try:
        global_args = p.parse_args()
    except argparse.ArgumentError as e:
        print(e)
        exit(1)

    conf = configparser.ConfigParser()
    conf.read_file(global_args.config)
    echobot_conf = conf['echobot']

    jid = sleekxmpp.basexmpp.JID(echobot_conf['jid'])
    jid.resource = jid.resource or 'echobot'
    xmpp = EchoBot(jid, echobot_conf['password'])
    print('Connecting as', jid)
    if xmpp.connect():
        xmpp.process(block=True)
    else:
        print('Unable to connect.')
        exit(1)
