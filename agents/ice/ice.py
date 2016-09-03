#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Zoe ICE
# https://github.com/rmed/zoe-ice
#
# Copyright (c) 2016 Rafael Medina García <rafamedgar@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from helper import messages as imsg
from os import environ as env
from os.path import join as path
from rwlock import RWLock
from tinydb import TinyDB, Query
from zoe.deco import Agent, Message, Timed
from zoe.models.users import Users
import datetime
import gettext
import zoe

gettext.install('ice')

DB_PATH = path(env['ZOE_HOME'], 'etc', 'ice', 'db.json')
RECORD = Query()
LOCK = RWLock()

LOCALEDIR = path(env['ZOE_HOME'], 'locale')
ZOE_LOCALE = env.get('ZOE_LOCALE', 'en')


@Agent(name='ice')
class ICE:

    def __init__(self):
        self.db = TinyDB(DB_PATH)

    @Timed(300)
    def deliver_ice(self):
        """Every 5 minutes check if ICEs should be delivered.

        Once sent to every email, the ICE record is disabled.
        """
        # Obtain all enabled ICEs
        delta = datetime.datetime.utcnow()
        records = self.db.search(RECORD.enabled == True)

        if not records:
            str_date = delta.strftime('%Y-%m-%d %H:%M:%S')
            self.logger.info('No enabled ICE records at %s' % str_date)
            return

        for record in records:
            user = record['user']
            date = record['date']

            try:
                converted = datetime.datetime.strptime(date, '%Y-%m-%d')

            except ValueError:
                self.sendbus(self._feedback(imsg.DATE_INVALID, user))
                continue

            # Skip future
            if converted > delta:
                continue

            msg = record['message']
            emails = record['emails']

            for mail in emails:
                self.sendbus(self._feedback(msg, mail, 'mail', 'Zoe ICE'))

            self.sendbus(self._feedback(imsg.ICE_SENT, user))

    @Message(tags=['add-mails'])
    def add_mails(self, parser):
        """Add recipient email addresses for ICE message.

        Args:
            emails (list[str]): List of emails to add.
            user (str): Unique ID of the user.
            src (str): Source agent.
        """
        emails = parser.get('emails')
        user = parser.get('user')
        src = parser.get('src')

        if not user:
            # Nothing to do
            return

        self._set_locale(user)

        # Add mails
        record = self._get_record(user)
        new_emails = list(set(record['emails']) | set(emails))

        self._update_record(user, emails=new_emails)

        return self._feedback(imsg.MAILS_UPDATED, user, src)

    @Message(tags=['disable-ice'])
    def disable_ice(self, parser):
        """Disable ICE delivery.

        Does not modify date.

        Args:
            user (str): Unique ID of the user.
            src (str): Source agent.
        """
        user = parser.get('user')
        src = parser.get('src')

        if not user:
            # Nothing to do
            return

        self._set_locale(user)

        # Disable
        self._update_record(user, enabled=False)

        return self._feedback(imsg.ICE_DISABLED, user, src)

    @Message(tags=['enable-ice'])
    def enable_ice(self, parser):
        """Enable ICE delivery.

        Does not modify date.

        Args:
            user (str): Unique ID of the user.
            src (str): Source agent.
        """
        user = parser.get('user')
        src = parser.get('src')

        if not user:
            # Nothing to do
            return

        self._set_locale(user)

        # Check date
        record = self._get_record(user)

        try:
            converted = datetime.datetime.strptime(record['date'], '%Y-%m-%d')

        except ValueError:
            return self._feedback(imsg.DATE_INVALID, user, src)

        if converted <= datetime.datetime.utcnow():
            return self._feedback(imsg.DATE_INPAST, user, src)

        # Enable
        self._update_record(user, enabled=True)

        return self._feedback(imsg.ICE_ENABLED, user, src)

    @Message(tags=['get-date'])
    def get_date(self, parser):
        """Obtain current ICE date for a specific user.

        Args:
            user (str): Unique ID of the user.
            src (str): Source agent.
        """
        user = parser.get('user')
        src = parser.get('src')

        if not user:
            # Nothing to do
            return

        self._set_locale(user)

        # Get user record
        record = self._get_record(user)
        date = record['date'] or imsg.DATE_NOTSET

        return self._feedback(imsg.DATE_SHOW % date, user, src)

    @Message(tags=['get-ice'])
    def get_ice(self, parser):
        """Get summary of the ICE for a specific user.

        Args:
            user (str): Unique ID of the user.
            src (str): Source agent.
        """
        user = parser.get('user')
        src = parser.get('src')

        if not user:
            # Nothing to do
            return

        self._set_locale(user)

        # Get user record
        record = self._get_record(user)

        emails = record['emails'].join(', ')
        date = record['date'] or imsg.DATE_NOTSET
        enabled = imsg.ICE_ENABLED if record['enabled'] else imsg.ICE_DISABLED

        return self._feedback(
            imsg.INFO_RECORD % (emails, date, enabled),
            user,
            src
        )

    @Message(tags=['get-msg'])
    def get_message(self, parser):
        """Obtain current ICE message for a specific user.

        Args:
            user (str): Unique ID of the user.
            src (str): Source agent.
        """
        user = parser.get('user')
        src = parser.get('src')

        if not user:
            # Nothing to do
            return

        self._set_locale(user)

        # Get user record
        record = self._get_record(user)

        return self._feedback(imsg.MSG_SHOW % record['message'], user, src)

    @Message(tags=['rm-mails'])
    def rm_mails(self, parser):
        """Remove recipient email addresses for ICE message.

        Args:
            emails (list[str]): List of emails to add.
            user (str): Unique ID of the user.
            src (str): Source agent.
        """
        emails = parser.get('emails')
        user = parser.get('user')
        src = parser.get('src')

        if not user:
            # Nothing to do
            return

        self._set_locale(user)

        # Remove mails
        record = self._get_record(user)
        new_emails = list(set(record['emails']) - set(emails))

        self._update_record(user, emails=new_emails)

        return self._feedback(imsg.MAILS_UPDATED, user, src)

    @Message(tags=['set-date'])
    def set_date(self, parser):
        """Set date in which the ICE message should be delivered.

        This does not enable the ICE.

        Args:
            date (str): Date to use for the delivery (YYYY-MM-DD)
            user (str): Unique ID of the user.
            src (str): Source agent.
        """
        date = parser.get('date')
        user = parser.get('user')
        src = parser.get('src')

        if not user:
            # Nothing to do
            return

        self._set_locale(user)

        # Check date is valid
        try:
            converted = datetime.datetime.strptime(date, '%Y-%m-%d')

        except ValueError:
            return self._feedback(imsg.DATE_INVALID, user, src)

        if converted <= datetime.datetime.utcnow():
            return self._feedback(imsg.DATE_INPAST, user, src)

        # Store date
        self._update_record(user, date=date)

        return self._feedback(imsg.DATE_UPDATED, user, src)

    @Message(tags=['set-msg'])
    def set_message(self, parser):
        """Set ICE message for a specific user.

        This only alters the contents of the message.

        Args:
            message (str): Message to store.
            user (str): Unique ID of the user.
            src (str): Source agent.
        """
        message = parser.get('message')
        user = parser.get('user')
        src = parser.get('src')

        if not user:
            # Nothing to do
            return

        self._set_locale(user)

        # Update user record
        self._update_record(user, message=message)

        return self._feedback(imsg.MSG_UPDATED, user, src)

    @Message(tags=['test-ice'])
    def test_ice(self, parser):
        """Test currently configured ICE.

        This sends an email to the user with their configured message.

        Args:
            user (str): Unique ID of the user.
        """
        user = parser.get('user')

        if not user:
            # Nothing to do
            return

        # Get user record
        record = self._get_record(user)

        return self._feedback(record['message'], user, 'mail', 'Zoe ICE test')

    def _feedback(self, message, user, dst=None, subject=None):
        """Send a message or mail to the given user.

        Args:
            message (str): Message to send.
            user (str): Unique ID of the user.
            dst (str): Destination of the message.
            subject (str): If using email, subject for the mail.
        """
        to_send = {
            'dst' : 'relay',
            'to'  : user
        }

        # Check destination
        if not dst:
            # If no preferred is found, default to mail
            users = zoe.Users()

            if user not in users.subjects():
                self.loger.info('Cannot send message, user %s not found' % user)
                return

            relayto = users.subject(user).get('preferred', 'mail')

        else:
            relayto = dst

        if relayto == 'mail':
            to_send['subject'] = subject or 'Zoe ICE'
            to_send['txt'] = message

        else:
            to_send['msg'] = message

        return zoe.MessageBuilder(to_send)

    def _get_record(self, user):
        """Obtain the record of a specific user.

        If the record does not exist, creates a new one so that future
        operations are updates.

        Args:
            user (str): Unique ID of the user.

        Returns:
            `dict` with the user record.
        """
        # Try to obtain existing record
        with LOCK.reader_lock:
            record = self.db.get(RECORD.user == user)

        if record:
            return record

        # Create new record
        record = {
            'name': user,
            'emails': [],
            'message': '',
            'enabled': False,
            'date': None
        }

        with LOCK.writer_lock:
            self.db.insert(record)

        return record

    def _set_locale(self, user):
        """Set the locale for messages based on the locale of the sender.

        If no locale is povided, Zoe's default locale is used or
        English (en) is used by default.
        """
        if not user:
            locale = ZOE_LOCALE

        else:
            conf = Users().subject(user)
            locale = conf.get('locale', ZOE_LOCALE)

        lang = gettext.translation(
            'ice',
            localedir=LOCALEDIR,
            languages=[locale,]
        )

        lang.install()

    def _update_record(self, user, **data):
        """Update the record of the given user.

        If the record does not exist, creates a new one.

        Args:
            user (str): Unique ID of the user.
            data (dict): Data to use in the update.

        Returns:
            `dict` with the updated values.
        """
        # Make sure record exists
        record = self._get_record(user)

        # Update info
        record.update(data)

        with LOCK.writer_lock:
            self.db.update(data, RECORD.user == user)

        return record
