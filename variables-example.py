# Rename the file variables-example.py to variables.py and change the necessary values
# If you have password authentication disabled on you master then you have to provide a private key file
# location replacing master_id_rsa value for the master_key variable.

# Keystone
auth_url = 'http://x.x.x.x:5000/v2.0'
username = 'admin'
password = 'pass'
tenant_name = 'admin'

# Glance
glance_endpoint = 'http://x.x.x.x:9292'

# Master SSH credentials
master_ip = 'x.x.x.x'
master_user = 'root'
master_pass = None
master_key = 'master_id_rsa'

# Other variables
floating_ip_pool = 'external'
private_key = 'private_key_for_accesssing_instances'
openshift_ip = 'x.x.x.x'

# NUBOMEDIA platform

# NUBOMEDIA Kurento Media Server - qemu image for KVM
kms_qemu_img = '/private/tmp/cirros-0.3.4-x86_64-disk.img'
kms_image_name = 'kurento-media-server'
kms_image_description = 'Please login with ubuntu user and your private_key'
kms_qemu_flavor = 'm1.medium'
kms_qemu_user_data = 'ls -l'

# NUBOMEDIA Kurento Media Server Docker image for - Docker
kms_docker_img = 'nubomedia/kurento-media-server'
kms_docker_image_description = 'Please login with root user and your docker image root password'
kms_docker_flavor = 'd1.medium'
kms_docker_user_data = 'ls -l'

# NUBOMEDIA Monitoring machine - qemu image for KVM
monitoring_qemu_img = '/private/tmp/cirros-0.3.4-x86_64-disk.img'
monitoring_image_name = 'nubomedia-monitoring'
monitoring_image_description = 'Please login with ubuntu user and your private_key'
monitoring_flavor = 'm1.medium'
monitoring_user_data = 'ls -l'

# NUBOMEDIA TURN Server machine - qemu image for KVM
turn_qemu_img = '/private/tmp/cirros-0.3.4-x86_64-disk.img'
turn_image_name = 'nubomedia-turn'
turn_image_description = 'Please login with ubuntu user and your private_key'
turn_flavor = 'm1.medium'
turn_user_data = 'ls -l'

# NUBOMEDIA Repository Server machine - qemu image for KVM
repository_qemu_img = '/private/tmp/cirros-0.3.4-x86_64-disk.img'
repository_image_name = 'nubomedia-repository'
repository_image_description = 'Please login with ubuntu user and your private_key'
repository_flavor = 'm1.medium'
repository_user_data = 'ls -l'

# NUBOMEDIA Conroller machine - qemu image for KVM
controller_qemu_img = '/private/tmp/cirros-0.3.4-x86_64-disk.img'
controller_image_name = 'nubomedia-controller-template'
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

# Configure OpenBaton public IP
PUBLIC_IP="PUBLIC_IP"
sed -i "s/${PUBLIC_IP}/${EXTERNAL_IP}/g" /etc/openbaton/openbaton.properties

# Configure PaaS manager
PUBLIC_IP="PUBLIC_IP"
OPENSHIFT_IP_DEFAULT="OPENSHIFT_IP"
OPENSTACK_IP_DEFAULT="OPENSTACK_IP"
OPENSTACK_USERNAME_DEFAULT="OPENSTACK_USERNAME"
OPENSTACK_PASSWORD_DEFAULT="OPENSTACK_PASSWORD"
OPENSTACK_KEY_PAIR_DEFAULT="OPENSTACK_KEY_PAIR"
OPENSTACK_TENANT_DEFAULT="OPENSTACK_TENANT"

OPENSHIFT_IP=%s
OPENSTACK_IP=%s
OPENSTACK_TENANT=%s
OPENSTACK_PASSWORD=%s

OPENSTACK_KEY_PAIR=%s
OPENSTACK_USERNAME=%s

sed -i "s/${PUBLIC_IP}/${EXTERNAL_IP}/g" /etc/nubomedia/paas.properties
sed -i "s/${OPENSHIFT_IP_DEFAULT}/${OPENSHIFT_IP}/g" /etc/nubomedia/paas.properties
sed -i "s/${OPENSTACK_IP_DEFAULT}/${OPENSTACK_IP}/g" /etc/nubomedia/paas.properties
sed -i "s/${OPENSTACK_USERNAME_DEFAULT}/${OPENSTACK_USERNAME}/g" /etc/nubomedia/paas.properties
sed -i "s/${OPENSTACK_PASSWORD_DEFAULT}/${OPENSTACK_PASSWORD}/g" /etc/nubomedia/paas.properties
sed -i "s/${OPENSTACK_TENANT_DEFAULT}/${OPENSTACK_TENANT}/g" /etc/nubomedia/paas.properties
sed -i "s/${OPENSTACK_KEY_PAIR_DEFAULT}/${OPENSTACK_KEY_PAIR}/g" /etc/nubomedia/paas.properties

# cd /opt/openbaton/nfvo && ./openbaton.sh start
# sleep 40
# cd /opt/nubomedia/ms-vnfm && ./ms-vnfm.sh
# sleep 40
# cd /opt/nubomedia/nubomedia-paas && ./nubomedia-paas.sh start

## Other installation instructions that should be done on the web interfaces by the deployment administrator ##
# Should put the PoP configuration first, then MS-NSD, and after that NSD.
""" % (openshift_ip, iaas_ip, tenant_name, password, private_key, username)