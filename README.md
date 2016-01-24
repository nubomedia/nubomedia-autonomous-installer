# NAI - nubomedia-autonomous-installer
NUBOMEDIA Autonomous Installer - http://www.nubomedia.eu

## Prerequisites
In order to be able to install the nubomedia-autonomous-installer you have to check that your current python version is 2.7.XX  with the following command:
```
python --version
```
Then you should install pip and after that you should install the dependecies using the following commands. When asked for any kind read it first and then confirm:
```
easy_install pip
pip install -r requirements.txt --upgrade
```
Before starting the installation you will first have to rename the *variables-examples.py* to *variables.py*. And then replace each variable with the desired value.
```
mv variables-example.py variables.py
```
### Keystone
```
auth_url = 'http://x.x.x.x:5000/v2.0'
username = 'admin'
password = 'pass'
tenant_name = 'admin'
```
*x.x.x.x* is the public IP address of your OpenStack.

### Glance
```
glance_endpoint = 'http://x.x.x.x:9292'
```
*x.x.x.x* is the public IP address of your OpenStack.

### Master SSH credentials
```
master_ip = 'x.x.x.x'
master_user = 'root'
master_pass = None
master_key = 'master_id_rsa'
```
*x.x.x.x* is the public IP address of your OpenStack.  
*master_user* is a ssh user with root permission on the OpenStack.  
For authentication you should either define the *master_pass* as a string variable betwen queotes or you can copy to the autonomous-installer directory the necessary private key for authenticatin on the master. The private key should not be password proteted.

### Other variables
```
floating_ip_pool = 'external'
private_key = 'private_key_for_accesssing_instances'
openshift_ip = 'x.x.x.x'
```
You should define the floating (public) IP pool name for the OpenStack.  
It is best to also add a public key on the OpenStack tenant you want to deploy NUBOMEDIA and then add the private key file to the autonomous-installer directory in order to allow it to customize the instances after deployment.

## NUBOMEDIA images
You should download all the NUBOMEDIA images and store them on the *repository/images/* directory.

# NUBOMEDIA Kurento Media Server - qemu image for KVM
```
kms_qemu_img = 'resources/images/kurento-media-server.qcow2'
kms_image_name = 'kurento-media-server'
kms_image_description = 'Kurento Media Server image for KVM hypervisor'
kms_qemu_flavor = 'm1.medium'
```
Kurento Media Server requires a flavor with at least 2GB of ram, 1 x86_64 CPU and 5GB of RAM.

# NUBOMEDIA Kurento Media Server Docker image for - Docker
```
kms_docker_img = 'nubomedia/kurento-media-server'
kms_docker_image_description = 'Please login with root user and your docker image root password'
kms_docker_flavor = 'd1.medium'
```
The Docker image for kurento-media-server is stored on the NUBOMEDIA dockerhub repository (https://hub.docker.com/r/nubomedia/kurento-media-server/ ).  The minimum flavor type would be at least 2GB of ram, 1 x86_64 CPU and 5GB of RAM.

# NUBOMEDIA Monitoring machine - qemu image for KVM
```
monitoring_qemu_img = '/private/tmp/cirros-0.3.4-x86_64-disk.img'
monitoring_image_name = 'nubomedia-monitoring'
monitoring_image_description = 'Please login with ubuntu user and your private_key'
monitoring_flavor = 'm1.medium'
```
## Run the installer
When you have defined all the necessary variables you can start the installer with the following command:
```
python main.py
```

