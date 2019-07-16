# based on https://github.com/ferrarymarco/docker-pxe from Marco Ferrari
FROM debian:buster-slim

RUN apt update \
 && apt install -y \
      dnsmasq \
      wget \
 && rm -rf /var/lib/apt/lists/*

COPY pxelinux/ /tftpboot/pxelinux
WORKDIR /tmp

ARG SYSLINUX=syslinux-6.03
ARG MEMTEST_VERSION=5.01

RUN wget https://www.kernel.org/pub/linux/utils/boot/syslinux/${SYSLINUX}.tar.gz -O -| tar -xz \
 && mkdir -p /tftpboot/pxelinux \
 && for f in \
      pxelinux.0 \
      chain.c32 \
      ethersel.c32 \
      mboot.c32 \
      memdisk \
      menu.c32 \
      libutil.c32 \
      ldlinux.c32 \
      memdisk ;\
    do find /tmp/$SYSLINUX/bios/ -type f -name $f -exec cp -v {} /tftpboot/pxelinux/ \; ; done \
 && wget -q http://www.memtest.org/download/"$MEMTEST_VERSION"/memtest86+-"$MEMTEST_VERSION".bin.gz -O - | gunzip > /tftpboot/pxelinux/memtest86+.bin

# copy dnsmasq default configuration
COPY etc/ /etc

ENTRYPOINT ["dnsmasq", "--no-daemon", "--dhcp-broadcast"]

ARG DHCP_IP=192.168.56.1
ENV DHCP_IP ${DHCP_IP}

CMD ["--dhcp-range=$DHCP_IP,proxy"]
