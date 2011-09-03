from fabric.api import *

env.name = ''		 		# The main module name 
					# This assumes that the repository name
					# is equal to the module name

env.repository = ''			# Git repository url

env.branch = "master"			# Default Git branch

env.gip = '127.0.0.1'			# GUnicorn IP to listen on

env.gport = '8000'			# GUnicorn Port to listen on

# Custom settings for different environments.
env.settings = {
    'develop': {
        'hosts' : [''],
        'branch' : 'develop',
        'gip': '0.0.0.0',
        },
    'stage': {
        'hosts': [''],
        'branch': 'stage',
        'gip': '0.0.0.0',
        },
    'live':{
        'hosts': [''],
        }
}


env.hosts = ['']
env.path = 'src/%s' % env.name

def develop():
    env.update(env.settings['develop'])

def stage():
    env.update(env.settings['stage'])
    
def live():
    env.update(env.settings['live'])

def bootstrap():
    with settings(user='root'):
        run('apt-get -q -y update')
        run('apt-get -q -y upgrade')
        run('apt-get -q -y install wget ssl-cert ruby ruby-dev '
            'libopenssl-ruby rdoc ri irb build-essential')
        with cd('/tmp'):
            run('wget -q http://production.cf.rubygems.org/rubygems/rubygems-1.7.2.tgz')
            run('tar xf rubygems-1.7.2.tgz')
            with cd('rubygems-1.7.2'):
                run('ruby setup.rb --no-format-executable')
            run('rm -rf rubygems-1.7.2*')
        run('gem install chef --no-ri --no-rdoc')

def virtualenv():
    run('mkdir -p %s' % env.path)
    run('virtualenv %s/../../' % env.path)

def clone():
    run('mkdir -p %s' % env.path)
    run('git clone %s %s' % (env.repository, env.path))

def fetch():
    with(cd(env.path)):
        run('git fetch')

def update():
    with(cd(env.path)):
        run('git pull')

def checkout(branch=None):
    if not branch: branch = env.branch
    with(cd(env.path)):
        run('git checkout %s' % branch)

def install():
    with(cd(env.path)):
        run('source ../../bin/activate; make install')

def loaddata(datafile='data.json'):
    with(cd(env.path)):
        run('source ../../bin/activate; python %s/manage.py loaddata %s' % (env.name, datafile))

def start(ip=None, port=None, workers=None):
    if not ip: ip = env.gip
    if not port: port = env.gport
    if not workers: workers = 2
    with(cd(env.path)):
        run('source ../../bin/activate; python %s/manage.py run_gunicorn %s:%s --daemon --workers %s' % (
                env.name, ip, port))

def stop():
    with(cd(env.path)):
        run("kill $(ps aux | grep run_gunicorn | grep %s | awk '{ print $2 }' | sort -nr | tail -n 1)" % env.name)

def deploy():
    stop()
    fetch()
    checkout()
    update()
    install()
    start()

