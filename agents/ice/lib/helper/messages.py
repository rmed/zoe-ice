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

"""Message definitions."""

# NOTE: Date is in the past
DATE_INPAST = 'DATE_INPAST'
# NOTE: Date has invalid format
DATE_INVALID = 'DATE_INVALID'
# NOTE: Date is not set (when enabling ICE)
DATE_NOTSET = 'DATE_NOTSET'
# NOTE: Token is current date
DATE_SHOW = 'DATE_SHOW %s'
DATE_UPDATED = 'DATE_UPDATED'
ICE_DISABLED = 'ICE_DISABLED'
ICE_ENABLED = 'ICE_ENABLED'
ICE_SENT = 'ICE_SENT'
# NOTE: Tokens are mails, date and if the ICE is enabled or not
INFO_RECORD = 'INFO_RECORD %s %s %s'
MAILS_UPDATED = 'MAILS_UPDATED'
# NOTE: Token is current message
MSG_SHOW = 'MSG_SHOW %s'
MSG_UPDATED = 'MSG_UPDATED'
