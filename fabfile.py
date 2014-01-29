#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import put, sudo


'''
    for dev:
        fab <taskname> \
            -H 127.0.0.1 \
            --user=vagrant \
            --port=2222 \
            -i ~/.`vagrant.d/insecure_private_key \
            -D

    for test:
        fab <taskname>:release=True \
            -H 127.0.0.1 \
            --user=vagrant \
            --port=2222 \
            -i ~/.`vagrant.d/insecure_private_key \
            -D

    for product: (it will use your .ssh/config)
        fab <taskname>:release=True \
            -H <server IP> \
            --user=<user> \
            --port=<port> \
'''


def init(release=False):
    '''
        init server, such as:
            install saltstack
            config saltstack to use github.com as gitfs if release=True
    '''

    _apt_upgrade()

    _config_master(release)
    sudo('service salt-master restart')

    _config_minion()
    sudo('service salt-minion restart')

    print 'You may need to reboot manually'


def _apt_upgrade():
    _put_file(
        local_path='fab_init_conf/apt_source',
        remote_path='/etc/apt/sources.list')
    sudo('apt-get -q update')
    sudo('DEBIAN_FRONTEND=noninteractive '
         'apt-get '
         '-o Dpkg::Options::="--force-confdef" '
         '-o Dpkg::Options::="--force-confold" '
         'upgrade -q -y')
    sudo('DEBIAN_FRONTEND=noninteractive '
         'apt-get '
         '-o Dpkg::Options::="--force-confdef" '
         '-o Dpkg::Options::="--force-confold" '
         'dist-upgrade -q -y')

    sudo('apt-get install python-software-properties -q -y')
    sudo('add-apt-repository ppa:saltstack/salt -y')
    sudo('apt-get -q update')
    sudo('apt-get install salt-master salt-minion -q -y')

    sudo('apt-get autoremove -q -y')


def _config_master(release):
    sudo('rm -rf /etc/salt/master.d/*')

    _put_file(
        local_path='fab_init_conf/master',
        remote_path='/etc/salt/master.d/base.conf')

    if release:
        sudo('apt-get install git python-pip -q -y')
        sudo('pip install GitPython')
        _put_file(
            local_path='fab_init_conf/gitfs',
            remote_path='/etc/salt/master.d/gitfs.conf')


def _config_minion():
    sudo('rm -rf /etc/salt/minion.d/*')

    _put_file(
        local_path='fab_init_conf/minion',
        remote_path='/etc/salt/minion.d/base.conf')


def _put_file(local_path, remote_path):
    put(local_path,
        remote_path,
        use_sudo=True,
        mode=0644)
    sudo('chown root:root %s' % remote_path)
