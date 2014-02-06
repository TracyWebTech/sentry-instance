
include supervisor

supervisor::app { 'sentry':
  command   => '.virtualenvs/sentry/bin/sentry --config=sentry-config.py start',
  directory => '/home/sentry/',
  user      => 'sentry',
}

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

package { 'postgresql-9.2':
  ensure => installed,
}

package { 'build-essential':
  ensure => installed,
}

