#!/bin/bash

PUPPET_TARGET_VERSION="3.4.2"

PUPPET_VERSION=`dpkg -l | grep puppet-common | awk '{ print $3 }' | cut -d- -f1`
dpkg --compare-versions "$PUPPET_VERSION" "<" "$PUPPET_TARGET_VERSION"
OUTDATED=$?

PUPPET_MODULES_FILE="modules.txt"

if [ "$PUPPET_TARGET_VERSION" != "$PUPPET_VERSION" ] && [ $OUTDATED -eq 0 ] ; then
    release_name=`lsb_release -c -s`
    wget -O /tmp/puppet_apt.deb http://apt.puppetlabs.com/puppetlabs-release-$release_name.deb &> /dev/null
    dpkg -i /tmp/puppet_apt.deb
    DEBIAN_FRONTEND=noninteractive apt-get update -y
    DEBIAN_FRONTEND=noninteractive apt-get install puppet -y
fi

if [[ -f /vagrant/puppet/hiera.yaml ]]; then
    cp -f /vagrant/puppet/hiera.yaml /etc/puppet/hiera.yaml
fi

update-locale LC_ALL=''

function install_puppet_module {
    MODULE_NAME="$1"
    TARGET_VERSION="$2"

    CURRENT_VERSION=`puppet module list | grep $MODULE_NAME | sed 's/^.*[^0-9]\([0-9]*\.[0-9]*\.[0-9]*\).*$/\1/'`

    if [ "$CURRENT_VERSION" == "$TARGET_VERSION" ]; then
        return 0
    fi

    dpkg --compare-versions "$CURRENT_VERSION" "<" "$TARGET_VERSION"
    OUTDATED=$?

    if [ $OUTDATED -eq 0 ]  ; then
        if [ "$CURRENT_VERSION" == '' ] ; then
            COMMAND="install"
        else
            COMMAND="upgrade"
        fi
        puppet module $COMMAND $MODULE_NAME --version $TARGET_VERSION
    fi
}

echo Instaling puppet modules from "$PUPPET_MODULES_FILE"
if [[ -f "$PUPPET_MODULES_FILE" ]] ; then
    while read module version ; do
        install_puppet_module "$module" "$version"
    done < $PUPPET_MODULES_FILE
fi
