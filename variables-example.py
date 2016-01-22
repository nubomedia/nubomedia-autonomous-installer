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


# NUBOMEDIA platform

# NUBOMEDIA Kurento Media Server qemu images for KVM
kms_qemu_img = '/private/tmp/cirros-0.3.4-x86_64-disk.img'
kms_image_name = 'kurento-media-server'
kms_image_description = 'Please login with ubuntu user and your private_key'

# NUBOMEDIA Kurento Media Server Docker images for Docker
kms_docker_img = 'nubomedia/kurento-media-server'
kms_docker_image_description = 'Please login with root user and your docker image root password'