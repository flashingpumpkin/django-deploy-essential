# -*- coding: utf-8 -*-
from fabric.api import *

# Set this to your applications module name.
env.module = 'application'

environments = {
    'dev': {
        'hosts': [],
        'branch': 'develop',
    },
    'stage': {
        'hosts': [],
        'branch': 'stage',
    },
    'live': {
        'hosts': [],
        'branch': 'master'  
    },
}

# Default environment is develop - just in case someone types
# deploy without specifying the environment we'll crash the 
# dev server ;)

env.update(environments['dev'])

# Hooks to update the environment
def dev():
    env.update(environments['dev'])

def stage():
    env.update(environments['stage'])
    
def live():
    env.update(environments['live'])

def clone():
    run('git clone %s %s' % (env.repository, env.name))

def fetch():
    with cd(env.name):
        run('git fetch -v')

def checkout():
    with cd(env.name):
        run('git reset --hard origin/%s' % env.name)

def rollback(heads=1):
    with cd(env.path):
        run('git reset --hard HEAD@{%s}' % heads)

def requirements():
    with cd(env.path):
        run('pip install -r requirements.txt')

def develop():
    with cd(env.path):
        run('python setup.py develop')

def install():
    with cd(env.path):
        run('python setup.py install')

def manage(cmd):
    with cd(env.path):
        run('python %s/manage.py %s' % (env.module, cmd))

def syncdb():
    manage('syncdb --noinput')

def migrate():
    manage('migrate')

def collectstatic():
    manage('collectstatic --noinput')

def bootstrap():
    clone()
    checkout()
    requirements()
    syncdb()
    migrate()
    collectstatic()

def deploy():
    fetch()
    checkout()
    requirements()
    syncdb()
    migrate()
    collectstatic()


