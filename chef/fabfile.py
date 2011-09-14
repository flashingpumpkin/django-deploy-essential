# This file's purpose is to bootstrap a server to have chef running
import os
import re
import json
import random
import tempfile
import string

from fabric.api import *
from fabric import operations
from fabric.colors import green, red
from fabric.contrib import files

import settings as conf

env.hosts = conf.HOSTS
env.user = conf.USER

def password():
    """ Creates a random password """
    chars = list(string.letters + string.letters.upper() + string.digits)
    return ''.join(random.sample(chars, 30))

def bootstrap():
    with settings(user='root'):
        upgrade()
        install()
        chef()
        virtualenv()
        
def upgrade():
    with settings(user='root'):
        run('apt-get -y update')
        run('apt-get -y upgrade')
    
def install():
    with settings(user = 'root'):
        if conf.APT:
            run('apt-get -y install %s' % ' '.join(conf.APT))
        
        if conf.EASY_INSTALL:
            run('easy_install %s' % ' '.join(conf.EASY_INSTALL))
        
        if conf.PIP:
            run('pip install %s' % ' '.join(conf.PIP))
    
        if conf.GEM:
            run('gem install -n /usr/local/bin %s --no-ri --no-rdoc --verbose' % ' '.join(conf.GEM))

def chef():
    with settings(user = 'root'):
        local('mkdir -p chef/')

        with open('chef/node.json', 'w') as f:
            json.dump(conf.CHEF, f)
        
        local('cp solo.rb chef/solo.rb')
        local('cp -r cookbooks/ chef/cookbooks')
        local('tar -f chef.tgz -cz chef/')

        operations.put('chef.tgz', '/tmp/chef.tgz')        

        run('mkdir -p /var/chef')

        with cd('/tmp'):
            run('tar -xf chef.tgz')
            run('cp -r chef/* /var/chef/')        
        
        with cd('/var/chef'):
            run('chef-solo -c solo.rb -j node.json')
        
        local('rm chef.tgz')
        local('rm node.json')
        local('rm -rf chef/')

def virtualenv():
    """ 
    Installing the virtual environment with fabric due to
    issues when running it from chef
    """
    with settings(user = conf.USER):
        run('mkvirtualenv project')
