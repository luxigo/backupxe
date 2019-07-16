#!/bin/bash

set -e 
set -x

setDefaults() {
  NETWORK=192.168.237.0
  NETMASK=255.255.255.0
  DHCPIP=192.168.237.1
  LOWERIP=192.168.237.10
  UPPERIP=192.168.237.250
  VMNAME=network-boot
  OSTYPE=Linux
}

loadPrefs() {
  CONFIG=${_CONFIG:-~/.backupxe-vm}
  [ -f $CONFIG ] || return 0
  . $CONFIG
}

savePrefs() {
  cat > $CONFIG << EOF
VBOXNET=$VBOXNET
NETWORK=$NETWORK
LOWERIP=$LOWERIP
UPPERIP=$UPPERIP
VMNAME=$VMNAME
OSTYPE=$OSTYPE
EOF
}

parseCommandLine() {
	if ! options=$(getopt -o h,c:,n:,m:,i:,l:,u:,N:,t: -l help,config:,network,netmask,dhcp-server-ip:,dhcp-lower-ip:,dhcp-upper-ip,vm-name:,os-type -- "$@")
	then
			# something went wrong, getopt will put out an error message for us
			exit 1
	fi
	 
	eval set -- "$options"
	 
	while [ $# -gt 0 ] ; do
			case $1 in
			-h|--help) usage ;;
			-c|--config) _CONFIG=$2 ; [ -f "$_CONFIG" ] || exit ; shift ;;
			-n|--dhcp-network) _NETWORK=$2 ; shift ;;
			-m|--dhcp-netmask) _NETMASK=$2 ; shift ;;
			-i|--dhcp-server-ip) _DHCPIP=$2 ; shift ;;
			-l|--dhcp-lower-ip) _LOWERIP=$2 ; shift ;;
			-u|--dhcp-upper-ip) _UPPERIP=$2 ; shift ;;
			-N|--name) _VMNAME=$2 ; shift ;;
			-t|--os-type) _OSTYPE=$2 ; shift ;;
			(--) shift; break;;
			(-*) echo "$(basename $0): error - unrecognized option $1" 1>&2; exit 1;;
			(*) break;;
			esac
			shift
	done

	setDefaults 
	loadPrefs
	NETWORK=${_NETWORK:-$NETWORK}
	NETMASK=${_NETMASK:-$NETMASK}
	DHCPIP=${_DHCPIP:-$DHCPIP}
	LOWERIP=${_LOWERIP:-$LOWERIP}
	UPPERIP=${_UPPERIP:-$UPPERIP}
	VMNAME=${_VMNAME:-$VMNAME}
	OSTYPE=${_OSTYPE:-$OSTYPE}
}

createOrUpdateNetworkConfig() {
  VBoxManage list hostonlyifs | grep -q \ $VBOXNET$ || unset VBOXNET
  if [ -z "$VBOXNET" ] ; then
		VBOXNET=$(VBoxManage hostonlyif create | sed -r -n -e 's/.*(vboxnet[0-9]+).*/\1/p')
		[ -z "$VBOXNET" ] && exit 1
		savePrefs
		VBoxManage hostonlyif ipconfig $VBOXNET --ip $NETWORK
		VBoxManage dhcpserver add --ifname $VBOXNET --ip $DHCPIP --netmask $NETMASK --lowerip $LOWERIP --upperip $UPPERIP --enable
	else
		VBoxManage hostonlyif ipconfig $VBOXNET --ip $NETWORK
		VBoxManage dhcpserver modify --ifname $VBOXNET --ip $DHCPIP --netmask $NETMASK --lowerip $LOWERIP --upperip $UPPERIP --enable
	fi
}

createOrUpdateVM() {
	VBoxManage showvminfo $VMNAME > /dev/null 2>&1 || VBoxManage createvm --name $VMNAME --ostype $OSTYPE --register
	VBoxManage modifyvm $VMNAME --hostonlyadapter1 $VBOXNET
	VBoxManage modifyvm $VMNAME --nic1 hostonly
	VBoxManage modifyvm $VMNAME --boot1 net
}

startVM() {
  VBoxManage startvm network-boot 
}

main() {
  parseCommandLine "$@"
  createOrUpdateNetworkConfig
  createOrUpdateVM
  startVM
}

main "$@"
