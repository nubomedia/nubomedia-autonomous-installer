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
# Private key that should be defined on the Compute > Access & Security > Key Paris tab
private_key_name = 'nubomedia-private-key'


# NUBOMEDIA platform

# NUBOMEDIA Kurento Media Server - qemu image for KVM
kms_qemu_img = '/private/tmp/cirros-0.3.4-x86_64-disk.img'
kms_image_name = 'kurento-media-server'
kms_image_description = 'Please login with ubuntu user and your private_key'
kms_qemu_flavor = 'm1.medium'
kms_qemu_user_data = 'ls -la'

# NUBOMEDIA Kurento Media Server Docker image for - Docker
kms_docker_img = 'nubomedia/kurento-media-server'
kms_docker_image_description = 'Please login with root user and your docker image root password'
kms_docker_flavor = 'd1.medium'
kms_docker_user_data = 'ls -la'

# NUBOMEDIA Monitoring machine - qemu image for KVM
monitoring_qemu_img = '/private/tmp/cirros-0.3.4-x86_64-disk.img'
monitoring_image_name = 'nubomedia-monitoring'
monitoring_image_description = 'Please login with ubuntu user and your private_key'
monitoring_flavor = 'm1.medium'
monitoring_user_data = 'ls -la'

# NUBOMEDIA TURN Server machine - qemu image for KVM
turn_qemu_img = '/private/tmp/cirros-0.3.4-x86_64-disk.img'
turn_image_name = 'nubomedia-turn'
turn_image_description = 'Please login with ubuntu user and your private_key'
turn_flavor = 'm1.medium'
turn_user_data = 'ls -la'

# NUBOMEDIA Repository Server machine - qemu image for KVM
repository_qemu_img = '/private/tmp/cirros-0.3.4-x86_64-disk.img'
repository_image_name = 'nubomedia-repository'
repository_image_description = 'Please login with ubuntu user and your private_key'
repository_flavor = 'm1.medium'
repository_user_data = 'ls -la'

# NUBOMEDIA Conroller machine - qemu image for KVM
controller_qemu_img = '/private/tmp/cirros-0.3.4-x86_64-disk.img'
controller_image_name = 'nubomedia-controller'
controller_image_description = 'Please login with ubuntu user and your private_key'
controller_flavor = 'm1.medium'
controller_user_data = 'ls -la'