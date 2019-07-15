#!/bin/sh
# backuPXE - Copyright (C) 2006-2019 Luc Deschenaux, all rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


cat /pxe/etc/ip_ranges > /tmp/ip_ranges.$$.tmp
echo $@ >> /tmp/ip_ranges.$$.tmp

for range in `cat /tmp/ip_ranges.$$.tmp` ; do
	nbtscan $range | tr ':' '-' | /usr/local/bin/sed -r -n -e 's/([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+) +([^\ ]+).* (00\-[0-9a-f\-]+)/\1 \3 \2/p'
done

rm /tmp/ip_ranges.$$.tmp

#arp  -n 192.168.100.112  |  sed -r -n -e 's/.* ([0-9A-F][0-9A-F]:[0-9A-F\:]+).*/\1/p'


#nbtscan $@ | sed -r -n -e 's/([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+) +([^\ ]+).* (00\-[0-9a-f\-]+)/\1 \3 \2/p'
#sed -r -n -e 's/([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+) +([^\ ]+).* (00\-[0-9a-f\-]+)/\1 \3 \2/p' /root/nbtscan.out
