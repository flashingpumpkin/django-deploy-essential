# -*- coding: utf-8 -*-
from fabric.api import *
from contextlib import contextmanager

# What's the name of the application / module?
env.name = 'project'

# The repository of your app
env.repository = 'git@github.com:flashingpumpkin/chao.git'

env.username = 'application'

environments = {
    'dev': {
        'hosts': ['localhost:2222'],
        'branch': 'master',
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

# Default port to listen on for gunicorn
env.gport = 8000

# The path to the application
env.path = '/home/%s/%s' % (env.username, env.name)

# Hooks to update the environment
def dev():
    env.update(environments['dev'])

def stage():
    env.update(environments['stage'])
    
def live():
    env.update(environments['live'])

# Custom context manager to switch to the application user
@contextmanager
def user():
    with settings(user = env.username):
        yield

def clone():
    run('git clone %s %s' % (env.repository, env.path))

def fetch():
    with user():
        with cd(env.path):
            run('git fetch -v')

def checkout():
    with user():
        with cd(env.path):
            run('git reset --hard origin/%s' % env.branch)

def rollback(heads=1):
    with user():
        with cd(env.path):
            run('git reset --hard HEAD@{%s}' % heads)

def requirements():
    with user():
        with cd(env.path):
            run('pip install -r requirements.txt')

def develop():
    with user():
        with cd(env.path):
            run('python setup.py develop')

def install():
    with user():
        with cd(env.path):
            run('python setup.py install')

def manage(cmd):
    with user():
        with cd(env.path):
            run('python %s/manage.py %s' % (env.name, cmd))

def syncdb():
    manage('syncdb --noinput')

def migrate():
    manage('migrate')

def collectstatic():
    manage('collectstatic --noinput')

def foreman():
    with settings(user = 'root'):
        with cd(env.path):
            run('foreman export upstart /etc/init -u %s -p %s' % (env.username, env.gport))

def stop():
    with settings(user = 'root'):
        run('stop %s' % env.name)

def start():
    with settings(user = 'root'):
        run('start %s' % env.name)

def restart():
    stop()
    start()

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
    stop()
    foreman()
    start()


