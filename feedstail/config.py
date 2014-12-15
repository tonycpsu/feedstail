# -*- coding: utf-8 -*-
# Copyright (C) 2011 Romain Gauthier <romain.gauthier@masteri2l.org>
# Copyright (C) 2011 Laurent Peuch <cortex@worlddomination.be>
#
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

# Import from the standard library
from logging import basicConfig
from sys import version_info

import feedparser

# Import from feedstail
from utils import Storage
from error import *

class Config(Storage):

    def __init__(self, *args, **kwargs):
        Storage(self, *args, **kwargs)
        # default values
        self.key = kwargs.get('key', 'id')
        self.reverse = kwargs.get('reverse', False)
        self.number = kwargs.get('number', None)
        self.ignore_key_error = kwargs.get('ignore_key_error', False)
        self.no_endl = kwargs.get('no_endl', False)
        self.url = kwargs.get('url', None)

        if version_info < (2, 6):
            self.format = kwargs.get('format', u'Title: %(title)s')
            self.formatFct = format = lambda entry: self.format % entry
        else:
            self.format = kwargs.get('format', u'Title: {title}')
            self.formatFct = lambda entry: self.format.format(**entry)

        self.entry_class = type("Entry",
                                (feedparser.FeedParserDict,),
                                {'__str__': self.format_entry()})

    def format_entry(self):
        def mystr(x):
            try:
                output = self.formatFct(x)
                if self.no_endl:
                    output = re.sub(r"[\t\r\n\s]+", r" ", output)
            except KeyError, key:
                raise FeedKeyError(key.args[0])
            else:
                return output.encode('utf-8')

        return mystr

    def make_entry(self, d):
        entry = self.entry_class(**d)
        return entry

basicConfig(format='%(levelname)s: %(message)s')

