from variables import *

# NUBOMEDIA platform images
download_images = False
kms_remote_img = 'http://repository.nubomedia.eu/images/kms-6.6.1-KVM.qcow2'
turn_remote_img = 'http://repository.nubomedia.eu/images/turn_server.qcow2'
monitoring_remote_img = 'http://repository.nubomedia.eu/images/nubomedia_monitoring.qcow2'
controller_remote_img = 'http://repository.nubomedia.eu/images/nubomedia_controller.qcow2'
repository_remote_img = 'http://repository.nubomedia.eu/images/nubomedia_repository.qcow2'
cloud_repository_remote_img = 'http://repository.nubomedia.eu/images/cloud_repository.qcow2'


# NUBOMEDIA Kurento Media Server - qemu image for KVM
kms_qemu_img = 'resources/images/kms-6.6.1-KVM.qcow2'
kms_image_name = 'kurento-media-server'
kms_image_description = 'Kurento Media Server image for KVM hypervisor'
kms_qemu_flavor = 'm1.medium'
kms_qemu_user_data = """#!/bin/bash
### KURENTO MEDIA SERVER CONFIGURATION ###
mkdir -p /opt/
echo export NUBOMEDIASTUNSERVERADDRESS=%s > /opt/envvars
echo export NUBOMEDIASTUNSERVERPORT=%s >> /opt/envvars
echo export NUBOMEDIATURNSERVERADDRESS=%s >> /opt/envvars
echo export NUBOMEDIATURNSERVERPORT=%s >> /opt/envvars
echo export NUBOMEDIAMONITORINGIP=%s >> /opt/envvars

cd /root/deploy && git pull origin master
mv /root/deploy/WebRtcEndpoint.conf.ini /etc/kurento/modules/kurento/WebRtcEndpoint.conf.ini
mv /root/deploy/fix.sh /usr/local/bin/
mv /root/deploy/logstash-forwarder.conf /etc/logstash-forwarder.conf
mv /root/deploy/collectd.conf /etc/collectd/collectd.conf

# Update the configurations
bash /usr/local/bin/fix.sh
""" % (instance_turn_ip, "3478", instance_turn_ip, "3478", instance_monitoring_ip)

# NUBOMEDIA Kurento Media Server Docker image for - Docker
kms_docker_img = 'nubomedia/kurento-media-server'
kms_docker_image_description = 'Please login with root user and your docker image root password'
kms_docker_flavor = 'd1.medium'
kms_docker_user_data = ''

# NUBOMEDIA Monitoring machine - qemu image for KVM
monitoring_qemu_img = 'resources/images/nubomedia_monitoring.qcow2'
monitoring_image_name = 'nubomedia-monitoring'
monitoring_image_description = 'Please login with ubuntu user and your private_key'
monitoring_flavor = 'm1.xlarge'
monitoring_user_data = """#!/bin/bash
### NUBOMEDIA MONITORING MACHINE CONFIGURATION ###
INSTANCE_NAME=$(curl http://169.254.169.254/latest/meta-data/hostname)
IFS='.' read -ra array <<< "$INSTANCE_NAME"
instance_name_simple=${array[0]}
sed -i " 1 s/.*/& $instance_name_simple/" /etc/hosts

EXTERNAL_IP=$(curl http://169.254.169.254/latest/meta-data/public-ipv4)
PUBLIC_IP="PUBLIC_IP"

HOST_TEMPLATE="HOSTNAMEMONITORING"

sed -i "s/${HOST_TEMPLATE}/${instance_name_simple}/g" /etc/collectd/collectd.conf
sed -i "s/${PUBLIC_IP}/${EXTERNAL_IP}/g" /etc/logstash-forwarder.conf
sed -i "s/${PUBLIC_IP}/${EXTERNAL_IP}/g" /etc/icinga2/features-enabled/graphite.conf

# Format the new attached disk for storing the metrics
(echo n; echo p; echo 1; echo ; echo; echo w) | fdisk /dev/vdb
mkfs.ext4 /dev/vdb1

# Add the new partition to be automounted on reboot
sed -i "\$a/dev/vdb1       /data   ext4    defaults 0 0" /etc/fstab

# Mount the partition
mount -a

reboot
"""

# NUBOMEDIA TURN Server machine - qemu image for KVM
turn_qemu_img = 'resources/images/turn_server.qcow2'
turn_image_name = 'nubomedia-turn'
turn_image_description = 'Please login with ubuntu user and your private_key'
turn_flavor = 'm1.small'
turn_user_data = ''

# NUBOMEDIA Repository Server machine - qemu image for KVM
repository_qemu_img = 'resources/images/nubomedia_repository.qcow2'
repository_image_name = 'nubomedia-repository'
repository_image_description = 'Please login with ubuntu user and your private_key'
repository_flavor = 'm1.medium'
repository_user_data = ''

# NUBOMEDIA Cloud Repository image - qemu image for KVM
cloud_repository_qemu_img = 'resources/images/nubomedia_cloud_repository.qcow2'
cloud_repository_image_name = 'cloud-repository'
cloud_repository_image_description = 'Please login with ubuntu user and your private_key'
cloud_repository_flavor = 'm1.medium'
cloud_repository_user_data = ''

# NUBOMEDIA Conroller machine - qemu image for KVM
controller_qemu_img = 'resources/images/nubomedia_controller.qcow2'
controller_image_name = 'nubomedia-controller'
controller_image_description = 'Please login with ubuntu user and your private_key'
controller_flavor = 'm1.xlarge'
controller_user_data = """#!/bin/bash
### NUBOMEDIA MANAGER CONFIGURATION ###
INSTANCE_NAME=$(curl http://169.254.169.254/latest/meta-data/hostname)
IFS='.' read -ra array <<< "$INSTANCE_NAME"
instance_name_simple=${array[0]}
sed -i " 1 s/.*/& $instance_name_simple/" /etc/hosts

EXTERNAL_IP=$(curl http://169.254.169.254/latest/meta-data/public-ipv4)
LOCAL_IP=$(curl http://169.254.169.254/latest/meta-data/local-ipv4)

# Copy the OpenShift Keystore to the PaaS manager resources
rm -rf /opt/nubomedia/nubomedia-paas/resource/openshift-keystore
cp /tmp/openshift-keystore /opt/nubomedia/nubomedia-paas/resource/openshift-keystore

# Setup configuration files
mv /etc/openbaton/openbaton.properties.example /etc/openbaton/openbaton.properties
mv /etc/nubomedia/msvnfm.properties.example /etc/nubomedia/msvnfm.properties
mv /etc/nubomedia/paas.properties.example /etc/nubomedia/paas.properties

# Configure OpenBaton public IP
PUBLIC_IP="PUBLIC_IP"
sed -i "s/${PUBLIC_IP}/${EXTERNAL_IP}/g" /etc/openbaton/openbaton.properties

# Configure MSVNFM public IP
sed -i "s/${PUBLIC_IP}/${EXTERNAL_IP}/g" /etc/nubomedia/msvnfm.properties

# Configure PaaS manager
PUBLIC_IP="PUBLIC_IP"
OPENSHIFT_IP_DEFAULT="OPENSHIFT_IP"
OPENSTACK_IP_DEFAULT="OPENSTACK_IP"
OPENSTACK_USERNAME_DEFAULT="OPENSTACK_USERNAME"
OPENSTACK_PASSWORD_DEFAULT="OPENSTACK_PASSWORD"
OPENSTACK_KEY_PAIR_DEFAULT="OPENSTACK_KEY_PAIR"
OPENSTACK_TENANT_DEFAULT="OPENSTACK_TENANT"
OPENSHIFT_DOMAIN_DEFAULT="OPENSHIFT_DOMAIN"

OPENSHIFT_IP=%s
OPENSTACK_IP=%s
OPENSTACK_TENANT=%s
OPENSTACK_PASSWORD=%s

OPENSTACK_KEY_PAIR=%s
OPENSTACK_USERNAME=%s
OPENSHIFT_DOMAIN=%s

sed -i "s/${PUBLIC_IP}/${EXTERNAL_IP}/g" /etc/nubomedia/paas.properties
sed -i "s/${OPENSHIFT_IP_DEFAULT}/${OPENSHIFT_IP}/g" /etc/nubomedia/paas.properties
sed -i "s/${OPENSTACK_IP_DEFAULT}/${OPENSTACK_IP}/g" /etc/nubomedia/paas.properties
sed -i "s/${OPENSTACK_USERNAME_DEFAULT}/${OPENSTACK_USERNAME}/g" /etc/nubomedia/paas.properties
sed -i "s/${OPENSTACK_PASSWORD_DEFAULT}/${OPENSTACK_PASSWORD}/g" /etc/nubomedia/paas.properties
sed -i "s/${OPENSTACK_TENANT_DEFAULT}/${OPENSTACK_TENANT}/g" /etc/nubomedia/paas.properties
sed -i "s/${OPENSTACK_KEY_PAIR_DEFAULT}/${OPENSTACK_KEY_PAIR}/g" /etc/nubomedia/paas.properties
sed -i "s/${OPENSHIFT_DOMAIN_DEFAULT}/${OPENSHIFT_DOMAIN}/g" /etc/nubomedia/paas.properties

cd /opt/openbaton/nfvo && ./openbaton.sh clean compile start
sleep 40
cd /opt/openbaton/generic-vnfm && ./generic-vnfm.sh clean compile start
sleep 40
cd /opt/nubomedia/ms-vnfm && ./ms-vnfm.sh clean compile start
sleep 40
cd /opt/nubomedia/nubomedia-paas && ./nubomedia-paas.sh clean compile start

## Other installation instructions that should be done on the web interfaces by the deployment administrator ##
# Should put the PoP configuration first, then MS-NSD, and after that NSD.
""" % (openshift_ip, iaas_ip, tenant_name, password, private_key, username, openshift_domain)
