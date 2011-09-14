# django-deploy-essential

## Synopsis

`django-deploy-essential` is a set of scripts that help you deploy fresh servers
with Python (Django) applications. 

	$ fab -f chef/fabfile.py bootstrap
	No hosts found. Please specify (single) host string for connection: localhost:2222
	[localhost:2222] run: apt-get -y update
	...
	 ✓  All done. localhost is good to go.
	
	$ fab deploy
	...
	✓  All done. Application is deployed.


## Usage

`chef/fabfile.py` is bootstrapping a clean server into a state where it's possible
to deploy Python applications with a `requirements.txt` file.

To customize what exactly is installed when bootstrapping, edit `chef/settings.py`.
The file is pretty much self explanatory and does a couple of sensible defaults
that Django applications tend to use: Nginx, pip, easy_install, Postgres, RabbitMQ,
git & co and some handy server utilities and development headers. 

`fabfile.py` in turn is crafted to deploy the actual application to a set of 
servers. You can define what servers & co by editing the file itself. It should
be self explanatory too.

