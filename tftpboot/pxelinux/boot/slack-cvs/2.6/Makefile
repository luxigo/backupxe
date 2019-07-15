#
#    Copyright (C) 2008  Luc Deschenaux - (lucos @ sf net)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# NOTE: You must copy manually to directory ./initrd_overlay/lib/modules
# the modules you want to have in the initrd image.
	 
	
KVERSION=`( ls -1d linux-* || true ) | tail -n 1 | sed -r -e 's/.*-([0-9\.]+).*/\1/' -e 's/\.$$//'`
VER=`( ls -1d linux-* || true ) | tail -n 1 | sed -r -e 's/.*-([0-9]+\.[0-9]+).*/\1/'`

all: kernel initrd overlay image

menuconfig:
	cd linux-$(KVERSION) ; make menuconfig

kernel:
	# - Download the latest kernel,
	# - Apply the kernel config file located in this directory,
	#    (if you are lazy press <enter> for all prompts)
	# - Make menuconfig so that you can check if the kernel configuration
	#   meets your needs (just quit if you dont have special needs)
	# - Build the kernel and copy System.map and compressed kernel to ./
	# - Install the modules in ./modules/$VERSION
	# - Replace links and compress modules in ./modules/$VERSION
	# - Replace modules found in ./initrd-overlay/lib/modules with
	#   the ones from ./modules/$VERSION

	./kernel0.sh

initrd:
        # Download the latest initrd from slackware installation CD
        # and extract the content in ./initrd.d
       
	./initrd0.sh

overlay:
        # Copy the System.map from current dir to ./initrd.d/mnt/boot
	# Copy files from ./common/initrd_overlay and ./initrd_overlay to ./initrd.d
	
	./overlay.sh

image: 
	# Copy ./initrd.d content in the initrd image file
	./initrd-$(VER).sh

clean:
	rm ./vmlinuz || true
	rm ./bzImage || true
	rm ./modules -r || true
	rm ./initrd.d -r || true
	rm ./initrd.img || true
	 
distclean:
	rm ./vmlinuz || true
	rm ./bzImage || true
	rm ./modules -r || true
	rm ./initrd.d -r || true
	rm ./initrd.img || true
	rm ./initrd.img.orig || true
	rm ./linux-2.* -r || true
