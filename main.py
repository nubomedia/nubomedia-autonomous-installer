# Copyright 2016 Universitatea Stefan cel Mare Suceava www.usv.ro
# Copyright 2016 NUBOMEDIA www.nubomedia.eu
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from keystoneclient.v2_0 import client as keystoneClient
from glanceclient import Client as glanceClient
from keystoneclient import session as keystoneSession
from novaclient import client as novaClient
from credentials import *
from contextlib import contextmanager
import paramiko
import time
import os
import tempfile


class KeystoneManager(object):
    def __init__(self, **kwargs):
        """Get an endpoint and auth token from Keystone.
        :param username: name of user param password: user's password
        :param tenant_id: unique identifier of tenant
        :param tenant_name: name of tenant
        :param auth_url: endpoint to authenticate against
        :param token: token to use instead of username/password
        """
        kc_args = {}

        if kwargs.get('endpoint'):
            kc_args['endpoint'] = kwargs.get('auth_url')
        else:
            kc_args['auth_url'] = kwargs.get('auth_url')

        if kwargs.get('tenant_id'):
            kc_args['tenant_id'] = kwargs.get('tenant_id')
        else:
            kc_args['tenant_name'] = kwargs.get('tenant_name')

        if kwargs.get('token'):
            kc_args['token'] = kwargs.get('token')
        else:
            kc_args['username'] = kwargs.get('username')
            kc_args['password'] = kwargs.get('password')

        print kc_args

        self.ksclient = keystoneClient.Client(**kc_args)
        self.session = keystoneSession.Session(auth=self.ksclient)
        self.token = self.ksclient.auth_token
        self.tenant_id = self.ksclient.project_id
        self.tenant_name = self.ksclient.tenant_name
        self.username = self.ksclient.username
        self.password = self.ksclient.password
        self.project_id = self.ksclient.project_id
        self.auth_url = self.ksclient.auth_url

    def get_session(self):
        if self.session is None:
            self.session = keystoneSession.Session(auth=self.ksclient)
        return self.session

    def get_endpoint(self):
        if self.auth_url is None:
            self.auth_url = self.ksclient.auth_url
        return self.auth_url

    def get_token(self):
        if self.token is None:
            self.token = self.ksclient.auth_token
        return self.token

    def get_tenant_id(self):
        if self.tenant_id is None:
            self.tenant_id = self.ksclient.project_id
        return self.tenant_id

    def get_tenant_name(self):
        if self.tenant_name is None:
            self.tenant_name = self.ksclient.tenant_name
        return self.tenant_name

    def get_username(self):
        if self.username is None:
            self.username = self.ksclient.username
        return self.username

    def get_password(self):
        if self.password is None:
            self.password = self.ksclient.password
        return self.password

    def get_project_id(self):
        if self.project_id is None:
            self.project_id = self.ksclient.project_id
        return self.project_id


class NovaManager(object):
    def __init__(self, **kwargs):
        self.nova = novaClient.Client("2", **kwargs)
        self.docker_hypervisors = []

    def get_flavors(self):
        print self.nova.flavors.list()
        return self.nova.flavors.list()

    def get_hypervisors_number(self):
        x = self.nova.hypervisors.list()
        print "Number of hypervisors :", len(x)
        return len(x)

    def get_hypervisor_ip(self,id):
        return getattr(self.nova.hypervisors.get(id), "host_ip")

    def get_hypervisor_type(self,id):
        return getattr(self.nova.hypervisors.get(id), "hypervisor_type")

    def get_docker_hypervisors_ip(self):
        for x in range(1, novaManager.get_hypervisors_number()):
            if novaManager.get_hypervisor_type(x) == 'docker':
                self.docker_hypervisors.append(novaManager.get_hypervisor_ip(x))
        return self.docker_hypervisors

    def create_floating_ip(self):
        unused_floating_ips = 0
        y = None
        floating_ips_list = self.nova.floating_ips.list()
        for i in floating_ips_list:
            x = getattr(i, "fixed_ip")
            if x is None:
                unused_floating_ips += 1
        if unused_floating_ips == 0:
            y = self.nova.floating_ips.create(get_env_vars()['floating_ip_pool'])
            print y
        return y

    def associate_floating_ip(self, instance_id):
        floating_ips_list = self.nova.floating_ips.list()
        fip = None
        for i in floating_ips_list:
            x = getattr(i, "fixed_ip")
            if x is None:
                fip = getattr(i, "ip")
                self.nova.servers.find(id=instance_id).add_floating_ip(fip)
                return fip
            else:
                fip = self.nova.floating_ips.create(get_env_vars()['floating_ip_pool'])
                self.nova.servers.find(id=instance_id).add_floating_ip(fip)
                return fip
        return fip

    def start_kvm_instance(self, instance_name, image_id, flavor, private_key, user_data):
        instance = self.nova.servers.create(instance_name,
            image_id,
            flavor,
            meta=None,
            files=None,
            reservation_id=None,
            min_count=None,
            max_count=None,
            security_groups=None,
            userdata=user_data,
            key_name=private_key,
            availability_zone=None,
            block_device_mapping=None,
            block_device_mapping_v2=None,
            nics=None,
            scheduler_hints=None,
            config_drive=None,
            disk_config=None)
        print "Instance name is %s and instance id is %s" % (instance.name, instance.id)
        status = "PENDING"
        while status != "ACTIVE":
            instances = self.nova.servers.list()
            for instance_temp in instances:
                if instance_temp.id == instance.id:
                    status = instance_temp.status
            print "Instance %s status is %s" % (instance_name, instance.status)
            time.sleep(10)
        return instance.id

    def get_flavor_id(self, flavor_name):
        flavors = self.nova.flavors.list()
        for i in flavors:
            x = getattr(i,"name")
            if x == flavor_name:
                flavorid = getattr(i, "id")
        print "Flavor %s with id %s" % (flavor_name,flavorid)
        return flavorid

    def get_security_group_id(self, security_group):
        sec_groups = self.nova.security_groups.list()
        for i in sec_groups:
            x = getattr(i, "name")
            if x == security_group:
                sec_group_id = getattr(i, "id")
        print "Security group %s with id %s " % (security_group, sec_group_id)
        return sec_group_id

class GlanceManager(object):
    def __init__(self, **kwargs):
        kc_args = {}

        if kwargs.get('endpoint'):
            kc_args['endpoint'] = kwargs.get('endpoint')

        if kwargs.get('token'):
            kc_args['token'] = kwargs.get('token')

        print kc_args

        self.glclient = glanceClient('1', **kc_args)
        self.dockerimages = []

    def get_docker_images(self):
        imagelist = self.glclient.images.list()
        for i in imagelist:
            x = getattr(i,"container_format")
            if x == 'docker':
                imagename = getattr(i,"name")
                self.dockerimages.append(imagename)
        return self.dockerimages

    def upload_qemu_image(self, image_name, image_location, *image_description):
        image = self.glclient.images.create(name=image_name, container_format='bare', disk_format='qcow2')
        print image.status
        image.update(data=open(image_location, 'rb'))
        try:
            image_description
        except NameError:
            None
        else:
            image.update(properties=dict(description=image_description))
        with open(image_location, 'wb') as f:
            for chunk in image.data():
                f.write(chunk)
        print "Image %s has been uploaded" % image_name
        return image.status

    def upload_docker_image(self, docker_img_name, *docker_image_description):
        image = self.glclient.images.create(name=docker_img_name, container_format='docker', disk_format='raw')
        print image.status
        image.update(data=open('/dev/null', 'rb'))
        try:
            docker_image_description
        except NameError:
            None
        else:
            image.update(properties=dict(description=docker_image_description))
        with open('/dev/null', 'wb') as f:
            for chunk in image.data():
                f.write(chunk)
        return image.status

    def get_image_id(self, image_name):
        imagelist = self.glclient.images.list()
        for i in imagelist:
            x = getattr(i,"name")
            if x == image_name:
                imageid = getattr(i, "id")
        print "Image name %s" % imageid
        return imageid


class OpenStackManager(object):
    def __init__(self, **kwargs):
        print None

    def pull_docker_images(self):
        # Pull all docker images on all docker compute nodes, requires OpenStack admin user
        if get_keystone_creds()['username'] == 'admin':
            dockerIPs = novaManager.get_docker_hypervisors_ip()
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print get_master_creds()
            ssh.connect(get_master_ip(), **get_master_creds())
            for i in dockerIPs:
                print 'Docker hypervisor IP address:', i
                for j in dockerimages:
                    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("ssh %s 'docker pull %s'" % (i, j))
                    print ssh_stdout.readlines()
            ssh.close()
        return None


class NubomediaManager(object):
    def __init__(self, **kwargs):
        print None

    def run_user_data(self, instance_ip, instance_user, instance_key, user_data):
        # Upload user_data
        remote_path = "/tmp/"

        d = {}
        d['username'] = instance_user
        d['pkey'] = paramiko.RSAKey.from_private_key_file(instance_key)

        transport = paramiko.Transport(instance_ip, '22')
        transport.connect(**d)
        sftp = paramiko.SFTPClient.from_transport(transport)
        try:
            sftp.chdir(remote_path)  # Test if remote_path exists
        except IOError:
            sftp.mkdir(remote_path)  # Create remote_path
            sftp.chdir(remote_path)
        print sftp.listdir()

        @contextmanager
        def tempinput(data):
            temp = tempfile.NamedTemporaryFile(delete=False)
            temp.write(data)
            temp.close()
            yield temp.name
            os.unlink(temp.name)
        with tempinput(user_data) as tempfilename:
            sftp.put(tempfilename, 'nubomedia_run_script.sh')
        sftp.close()

        # Run user_data
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(instance_ip, **d)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo -- sh -c 'chmod +x /tmp/nubomedia_run_script.sh && cd /tmp && ./nubomedia_run_script.sh'")
        print ssh_stdout.readlines()
        return None

if __name__ == '__main__':
    # Connect to Keystone
    kwargs = {}
    kwargs = get_keystone_creds()
    keystoneManager = KeystoneManager(**kwargs)

    # Get the list of the docker images names
    kwargs = {}
    kwargs['token'] = keystoneManager.get_token()
    kwargs['endpoint'] = get_glance_creds()
    glanceManager = GlanceManager(**kwargs)
    dockerimages = glanceManager.get_docker_images()

    # Connect to Nova
    kwargs = get_nova_creds()
    novaManager = NovaManager(**kwargs)

    openStackManager = OpenStackManager()
    nubomediaManager = NubomediaManager()

    # Pull all docker images on all docker compute nodes, requires OpenStack admin user
    # openStackManager.pull_docker_images()

    # Create a floating IP if there is no floating IP on that tenant
    # print novaManager.create_floating_ip()

    ##############################
    # Start NUBOMEDIA deployment
    ##############################

    start_time = time.time()
    print 'Starting NUBOMEDIA deployment'

    ###########################
    # Upload NUBOMEDIA Images
    ###########################

    # Upload Kurento Media Server KVM Image on Glance
    print glanceManager.upload_qemu_image(kms_image_name, kms_qemu_img, kms_image_description)

    # Upload Kurento Media Server Docker Image on Glance
    print glanceManager.upload_docker_image(kms_docker_img, kms_docker_image_description)

    # Upload Monitoring machine Image on Glance
    print glanceManager.upload_qemu_image(monitoring_image_name, monitoring_qemu_img, monitoring_image_description)

    # Upload TURN Server Image on Glance
    print glanceManager.upload_qemu_image(turn_image_name, turn_qemu_img, turn_image_description)

    # Upload Repository Image on Glance
    print glanceManager.upload_qemu_image(repository_image_name, repository_qemu_img, repository_image_description)

    # Upload Controller Image on Glance
    print glanceManager.upload_qemu_image(controller_image_name, controller_qemu_img, controller_image_description)

    #######################################
    # Start NUBOMEDIA platform instances
    #######################################

    # Start Monitoring instance
    instance_monitoring = novaManager.start_kvm_instance(monitoring_image_name, glanceManager.get_image_id(monitoring_image_name), novaManager.get_flavor_id(monitoring_flavor), private_key, monitoring_user_data)
    instance_monitoring_ip = novaManager.associate_floating_ip(instance_monitoring)
    print "Monitoring instance name=%s , id=%s , public_ip=%s" % (monitoring_image_name, instance_monitoring, instance_monitoring_ip)

    # Start TURN Server instance
    instance_turn = novaManager.start_kvm_instance(turn_image_name, glanceManager.get_image_id(turn_image_name), novaManager.get_flavor_id(turn_flavor), private_key, turn_user_data)
    instance_turn_ip = novaManager.associate_floating_ip(instance_turn)
    print "TURN instance name=%s , id=%s , public_ip=%s" % (turn_image_name, instance_turn, instance_turn_ip)

    # Start Repository Server instance
    instance_repository = novaManager.start_kvm_instance(repository_image_name, glanceManager.get_image_id(repository_image_name), novaManager.get_flavor_id(repository_flavor), private_key, repository_user_data)
    instance_repostory_ip = novaManager.associate_floating_ip(instance_repository)
    print "Repository instance name=%s , id=%s , public_ip=%s" % (repository_image_name, instance_repository, instance_repostory_ip)

    # Start Controller instance
    instance_controller = novaManager.start_kvm_instance(controller_image_name, glanceManager.get_image_id(controller_image_name), novaManager.get_flavor_id(controller_flavor), private_key, controller_user_data)
    instance_controller_ip = novaManager.associate_floating_ip(instance_controller)
    print "Controller instance name=%s , id=%s , public_ip=%s" % (controller_image_name, instance_controller, instance_controller_ip)

    ##########################################
    # Configure  NUBOMEDIA services
    ##########################################

    time.sleep(60)
    nubomediaManager.run_user_data(instance_monitoring_ip, "ubuntu", private_key, monitoring_user_data)

    nubomediaManager.run_user_data(instance_controller_ip, "ubuntu", private_key, controller_user_data)

    nubomediaManager.run_user_data(instance_turn_ip, "ubuntu", private_key, turn_user_data)

    nubomediaManager.run_user_data(instance_repostory_ip, "ubuntu", private_key, repository_user_data)

    elapsed_time = time.time() - start_time
    print "Total time needed for deployment of the NUBOMEDIA platform was %s seconds " % elapsed_time




