
include memcached
include supervisor

package { 'python-dev':
  ensure => installed,
}

package { 'libev-dev':
  ensure => installed,
}

package { 'postgresql-server-dev-9.2':
  ensure => installed,
}

package { 'python-pip':
  ensure => installed,
}

package { 'build-essential':
  ensure => installed,
}

supervisor::app { 'sentry':
  command     => '/home/sentry/.virtualenvs/sentry/bin/sentry --config=sentry_config.py start --noupgrade',
  directory   => '/home/sentry/sentry/',
  user        => 'root',
  environment => hiera('environment'),
}
