
# Applications to install while bootstrapping. This is the bare minimum
# to create a machine that will provide everything to get Python and 
# Chef going.

# Applications to install with `apt-get`.
APT = (
    'wget', 
    'curl',
    'htop',
    'python',
    'python-dev',
    'python-setuptools',
    'ruby', 
    'ruby-dev',
)

# Packages to install globally with `easy_install`
EASY_INSTALL = (
    'pip',
)

# Packages to install globally with `pip`
PIP = (
    'virtualenv',
    'virtualenvwrapper',
)

# Packages to install globally with `gem`
GEM = (
    'chef',
    'foreman',
)

# The user you will deploy this application as
USER = 'application'

# Set up a virtual environment? This requires virtualenvwrapper to be installed
VIRTUALENV = True

# The name for the virtual environment
VIRTUALENV_NAME = 'application'

# Configuring chef. Everything in this dictionary will be dumped into the
# hosts node.json file
CHEF = {
    # Chef recipes to run
    "recipes": [
        # Essentials
        "build-essential",                          
        # Utilities
        "vim", "screen", "htop",               
        # Version control
        "git", "mercurial", "subversion",               
        # Languages
        "python",                                       
        # Apps
        "nginx", "rabbitmq", "memcached", "postgresql",
        # Random
        "libjpeg", 
        
        # Create users
        "users",
        
        # Install handy dotfiles for our application user
        "application",   

    ],

    # Virtualenv data for the templates
    "virtualenv": {
        "name": VIRTUALENV_NAME
    },

    # List of groups to create
    "groups": [

    ],
    
    # List of user accounts to create
    "users":[
        {
            # Username
            "id": USER,
            "comment": "The application user",
            "shell": "/bin/bash",
            "password": "hash",
            
            # List of authorized ssh keys
            "authorized_keys": [
                
            ]
        },
    ],

    # Where the application will serve and nginx will proxy to
    "application": {
        "ip": "127.0.0.1",
        "port": "8000"
    },
    
    # Where nginx will listen and serve from
    "nginx": {
        "hostname": "localhost.com",
        "port": "80",
        "root": "/usr/share/nginx/www"
    },
    
    # The application user
    "user": USER,  
}
