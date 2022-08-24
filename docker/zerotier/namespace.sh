#!/bin/sh

set -e

# NOTE: this script creates a network namespace on your machine with the connectivity
# to the Internet with DNS enabled.

if [[ $(id -u) -ne 0 ]] ; then echo "Please run as root" ; exit 1 ; fi

source .env

OUTBOUND_NIC=`ip route show to default | grep -Eo "dev\s*[[:alnum:]]+" | sed 's/dev\s//g'`
if [ -d /home/test ]; then
    echo "-------------------------DETECTING PREVIOUS INSTALL!!----CLEANING-------------------------------------------"
    echo bye | iptables -t nat -D POSTROUTING -o ${OUTBOUND_NIC} -j MASQUERADE && echo Success. || echo Failure.
    echo bye | iptables -D FORWARD -i ${VETH_HOST_SIDE_NIC} -o ${OUTBOUND_NIC} -j ACCEPT && echo Success. || echo Failure.
    echo bye | iptables -D FORWARD -s 10.44.0.0/255.255.0.0 -d 172.16.0.0/255.255.255.0 -j DROP && echo Success. || echo Failure.
    echo bye | iptables -D FORWARD -s 10.44.0.0/255.255.0.0 -d 0.0.0/0.0.0.0 -j ACCEPT && echo Success. || echo Failure.
    echo bye | ip link del ${VETH_HOST_SIDE_NIC} && echo Success. || echo Failure.
    echo bye | ip netns del ${NET_NAMESPACE} && echo Success. || echo Failure.
    echo bye | rm -f /etc/netns/${NET_NAMESPACE}/resolv.conf && echo Success. || echo Failure.
    echo bye | rmdir /etc/netns/${NET_NAMESPACE} && echo Success. || echo Failure.
    rm -r /home/test
fi

#
# Variables. Please check this paragraph to make sure you have the correct NICs chosen
#
echo "Network namespace: ${NET_NAMESPACE}"
echo "Outbound NIC: ${OUTBOUND_NIC}"
echo "VETH NIC to be created in the namespace: ${VETH_CONTAINER_SIDE_NIC}"
echo "VETH NIC to be created on the host: ${VETH_HOST_SIDE_NIC}"

#
# Configurations section
#

# Set DNS settings
echo "[1/5] Setting up DNS for the namespace..."
mkdir -p /etc/netns/${NET_NAMESPACE}
touch /etc/netns/${NET_NAMESPACE}/resolv.conf
echo "nameserver 8.8.8.8" > /etc/netns/${NET_NAMESPACE}/resolv.conf
echo "[1/5] -> Setup for DNS configurations is completed, OK!"

# Create namespace
echo "[2/5] Creating a namespace..."
ip netns add ${NET_NAMESPACE}
ip -n ${NET_NAMESPACE} link set dev ${LOOPBACK_NIC} up
echo "[2/5] -> Namespace is created, OK! [netns=${NET_NAMESPACE}]"

# Add VETH pair
echo "[3/5] Adding a connectivity to the namespace..."
ip link add ${VETH_HOST_SIDE_NIC} type veth peer name ${VETH_CONTAINER_SIDE_NIC} netns ${NET_NAMESPACE}
ip link set ${VETH_HOST_SIDE_NIC} up
ip -n ${NET_NAMESPACE} link set ${VETH_CONTAINER_SIDE_NIC} up
echo "[3/5] -> A VETH pair is added to connect network namespace & host network, OK! [veth_ns=${VETH_CONTAINER_SIDE_NIC}, veth_host=${VETH_HOST_SIDE_NIC}]"

# Add addressing
echo "[4/5] Applying addressing to the VETH pair..."
ip addr add ${VETH_HOST_SIDE_ADDR}${VETH_SUBNET_SUFFIX} dev ${VETH_HOST_SIDE_NIC}
ip -n ${NET_NAMESPACE} addr add ${VETH_CONTAINER_SIDE_ADDR}${VETH_SUBNET_SUFFIX} dev ${VETH_CONTAINER_SIDE_NIC}
echo "[4/5] -> Addressing is set for VETH, OK! [veth_ns_ip=${VETH_CONTAINER_SIDE_ADDR}, veth_host_addr=${VETH_HOST_SIDE_NIC}, veth_subnet_suffix=${VETH_SUBNET_SUFFIX}]"

# Allow routing
echo "[5/5] Applying firewall settings..."
## 5.1 Add default route in the namespace
ip netns exec ${NET_NAMESPACE} ip route add default via ${VETH_HOST_SIDE_ADDR}
# 5.2 Tweak the Kernel to allow IPv4 traffic forwarding
sysctl -w net.ipv4.ip_forward=1
# 5.3 Allow traffic to flow from VETH to the outbound NIC
iptables -A FORWARD -i ${VETH_HOST_SIDE_NIC} -o ${OUTBOUND_NIC} -j ACCEPT
# 5.4 Masquerade traffic before it exits through the outbound NIC
iptables -t nat -A POSTROUTING -o ${OUTBOUND_NIC} -j MASQUERADE
iptables -I FORWARD -s 10.44.0.0/255.255.0.0 -d 172.16.0.0/255.255.255.0 -j DROP
iptables -A FORWARD -s 10.44.0.0/255.255.0.0 -d 0.0.0/0.0.0.0 -j ACCEPT
echo "[5/5] -> Firewall is ready, OK!"
mkdir /home/test
