if [ -n "$CI" ]; then
    export HOME=/home/circleci/${CIRCLE_PROJECT_REPONAME}
    export HOMEROOT=/home/circleci/${CIRCLE_PROJECT_REPONAME}
    # Clone dependencies
    git clone -b master https://github.com/isb-cgc/ISB-CGC-Common.git
else
    export $(cat /home/vagrant/API/.env | grep -v ^# | xargs) 2> /dev/null
    export HOME=/home/vagrant
    export HOMEROOT=/home/vagrant/API
fi

# Remove .pyc files; these can sometimes stick around and if a
# model has changed names it will cause various load failures
find . -type f -name '*.pyc' -delete

export DEBIAN_FRONTEND=noninteractive

# Install and update apt-get info
echo "Preparing System..."
apt-get -y install software-properties-common

if [ -n "$CI" ]; then
    # Use these next 4 lines to update mysql public build key
    echo 'download mysql public build key'
    wget -O - -q 'https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x8C718D3B5072E1F5' | grep -v '>' | grep -v '<' | grep -v '{' > mysql_pubkey.asc
    apt-key add mysql_pubkey.asc || exit 1
    echo 'mysql build key update done.'
    wget https://dev.mysql.com/get/mysql-apt-config_0.8.9-1_all.deb
    apt-get install -y lsb-release
    dpkg -i mysql-apt-config_0.8.9-1_all.deb
fi

apt-get update -qq

# Install apt-get dependencies
echo "Installing Dependencies..."
if [ -n "$CI" ]; then
apt-get install -y --force-yes unzip libffi-dev libssl-dev libmysqlclient-dev python3-mysqldb python3-dev libpython3-dev git ruby g++ curl dos2unix python3.5
apt-get install -y --force-yes mysql-client
else
    apt-get install -qq -y --force-yes unzip libffi-dev libssl-dev libmysqlclient-dev python3-mysqldb python3-dev libpython3-dev git ruby g++ curl dos2unix python3.5 mysql-client-5.7
fi
echo "Dependencies Installed"

# If this is local development, clean out lib for a re-structuring
if [ -z "${CI}" ]; then
    # Clean out lib to prevent confusion over multiple builds in local development
    # and prep for local install
    echo "Emptying out ${HOMEROOT}/lib/ ..."
fi

# Install PIP + Dependencies
echo "Installing pip3..."
curl --silent https://bootstrap.pypa.io/get-pip.py | python3

# Install our primary python libraries
# If we're not on CircleCI, or we are but the lib directory isn't there (cache miss), install lib
if [ -z "${CI}" ] || [ ! -d "lib" ]; then
    echo "Installing Python Libraries..."
    pip3 install -r ${HOMEROOT}/requirements.txt -t ${HOMEROOT}/lib --upgrade --only-binary all
else
    echo "Using restored cache for Python Libraries"
fi

# Install Google App Engine
# If we're not on CircleCI or we are but google_appengine isn't there, install it
if [ -z "${CI}" ] || [ ! -d "google_appengine" ]; then
    echo "Installing Google App Engine..."
    wget https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.69.zip -O ${HOME}/google_appengine.zip
    unzip -n -qq ${HOME}/google_appengine.zip -d $HOME
    export PATH=$PATH:${HOME}/google_appengine/
    echo "Google App Engine Installed"
else
    echo "Using restored cache for Google App Engine. "
fi

# Install Google Cloud SDK
# If we're not on CircleCI or we are but google-cloud-sdk isn't there, install it
if [ -z "${CI}" ] || [ ! -d "google-cloud-sdk" ]; then
    echo "Installing Google Cloud SDK..."
    export CLOUDSDK_CORE_DISABLE_PROMPTS=1
    curl https://sdk.cloud.google.com | bash
    export PATH=$PATH:${HOME}/google-cloud-sdk/bin
    echo 'export PATH=$PATH:${HOME}/google-cloud-sdk/bin' | tee -a ${HOME}/.bash_profile
    echo "Google Cloud SDK Installed"
else
    echo "Using restored cache for Google Cloud SDK."
fi
