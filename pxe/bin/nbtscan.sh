#!/bin/sh

cat /pxe/etc/ip_ranges > /tmp/ip_ranges.$$.tmp
echo $@ >> /tmp/ip_ranges.$$.tmp

for range in `cat /tmp/ip_ranges.$$.tmp` ; do
	nbtscan $range | tr ':' '-' | /usr/local/bin/sed -r -n -e 's/([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+) +([^\ ]+).* (00\-[0-9a-f\-]+)/\1 \3 \2/p'
done

rm /tmp/ip_ranges.$$.tmp

#arp  -n 192.168.100.112  |  sed -r -n -e 's/.* ([0-9A-F][0-9A-F]:[0-9A-F\:]+).*/\1/p'


#nbtscan $@ | sed -r -n -e 's/([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+) +([^\ ]+).* (00\-[0-9a-f\-]+)/\1 \3 \2/p'
#sed -r -n -e 's/([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+) +([^\ ]+).* (00\-[0-9a-f\-]+)/\1 \3 \2/p' /root/nbtscan.out
