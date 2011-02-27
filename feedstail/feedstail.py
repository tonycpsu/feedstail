# -*- coding: utf-8 -*-
# Copyright (C) 2011 Romain Gauthier <romain.gauthier@masteri2l.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Import from the standard library
from time import sleep

# Import from FeedParser
from config import config
from feedparser import parse

tail = []

def isnew(entry):
    for item in tail:
        if entry.id == item.id:
            return False
    return True


def show(entry):
    print(config.format.format(**entry))


def main():
    def _main():
        global tail
        d = parse(config.url)
        for entry in d.entries:
            if isnew(entry):
                tail = [entry] + tail[:100]
                show(entry)

    _main()
    while not config.oneshot:
        sleep(config.interval)
        _main()
