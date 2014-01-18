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
import sys

import sleekxmpp


class SendMsgBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, recipients, message, subject):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.recipients = recipients
        self.msg = message
        self.subject = subject
        self.add_event_handler('session_start', self.start)

    def start(self, event):
        self.send_presence()
        for recipient in self.recipients:
            self.send_message(mto=recipient,
                              msubject=self.subject,
                              mbody=self.msg,
                              mtype='normal')
        self.disconnect(wait=True)

def FirstOf(*types, error='argument "{}" is not valid'):
    def f(s):
        for t in types:
            try:
                return t(s)
            except:
                pass
        raise argparse.ArgumentTypeError(error.format(s))
    return f

file_or_jid = FirstOf(argparse.FileType('r'),
                      sleekxmpp.basexmpp.JID,
                      error='"{}" is neither a file nor a valid JID')

if __name__ == '__main__':

    p = argparse.ArgumentParser()
    p.add_argument('recipients', metavar='<file or JID>', nargs='+', type=file_or_jid, help='file format is one JID per line')
    p.add_argument('-c', '--config', nargs='?', default=os.path.expanduser('~/.xmpputils'), type=argparse.FileType('r'))
    p.add_argument('-s', '--subject', nargs='?', default='')
    try:
        global_args = p.parse_args()
    except argparse.ArgumentError as e:
        print(e)
        exit(1)
    r = []
    for recipient in global_args.recipients:
        if isinstance(recipient, sleekxmpp.basexmpp.JID):
            r.append(recipient)
        else:
            r.extend(map(sleekxmpp.basexmpp.JID, filter(None, recipient.read().split('\n'))))
    global_args.recipients = r

    conf = configparser.ConfigParser()
    conf.read_file(global_args.config)
    sendxmpp_conf = lambda key: conf.get('sendxmpp', key)

    jid = sleekxmpp.basexmpp.JID(sendxmpp_conf('jid'))
    jid.resource = jid.resource or 'sendxmpp.py'
    xmpp = SendMsgBot(jid, sendxmpp_conf('password'), global_args.recipients, sys.stdin.read(), global_args.subject)

    if xmpp.connect():
        xmpp.process(block=True)
    else:
        print('Unable to connect.')
        exit(1)
