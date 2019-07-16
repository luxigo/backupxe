all: build run

build:
	cd tftpboot && docker build . -t backupxe

run: run-container run-vm

run-vm:
	./pxevm.sh 192.168.237.0 255.255.255.0 192.168.237.10 192.168.237.250

run-container:
	docker start backupxe || docker run -d --rm --name backupxe --net=host backupxe --dhcp-range=192.168.237.1,proxy

