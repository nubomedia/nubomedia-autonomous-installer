# Rename the file variables-example.py to variables.py and change the necessary values
# If you have password authentication disabled on you master then you have to provide a private key file
# location replacing master_id_rsa value for the master_key variable.

# Enable logging to installer.log file ?
enabled_logging = True

# Keystone
iaas_ip = 'x.x.x.x'
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
# OpenShift Keystore that should be generated using the Portacle tool from http://portecle.sourceforge.net/
openshift_keystore = 'openshift-keystore'
openshift_domain = 'apps.nubomedia-paas.eu'
openshift_token = 'oimqwoi29m31290xmu23904u2390z432mu90z432m90432mu90z42mz29031209z3m190z3n128...'
nubomedia_admin_paas = 'nubomediapaas'
use_kurento_on_docker = False
