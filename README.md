# nubomedia-autonomous-installer
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
## Keystone
```
auth_url = 'http://x.x.x.x:5000/v2.0'
username = 'admin'
password = 'pass'
tenant_name = 'admin'
```
*x.x.x.x* is the public IP address of your OpenStack.

## Glance
```
glance_endpoint = 'http://x.x.x.x:9292'
```
*x.x.x.x* is the public IP address of your OpenStack.

## Master SSH credentials
```
master_ip = 'x.x.x.x'
master_user = 'root'
master_pass = None
master_key = 'master_id_rsa'
```
*x.x.x.x* is the public IP address of your OpenStack.
*master_user* is a ssh user with root permission on the OpenStack. For authentication you should either define the master_pass as a string variable betwen queotes or you can copy to the autonomous-installer directory the necessary private key for authenticatin on the master. The private key should not be password proteted.

## Other variables
floating_ip_pool = 'external'
private_key = 'private_key_for_accesssing_instances'
openshift_ip = 'x.x.x.x'


## Run the installer
To start the installer you should run the following command:
```
python main.py
```

