
import os

from fabric.api import sudo, run, env, put
from fabric.contrib.files import exists
from fabric.decorators import with_settings
from fabric.context_managers import settings, cd, prefix


VENV_NAME = 'sentry'
APP_USER = 'sentry'
APP_NAME = 'sentry'

REPO_PATH = '/home/{}/{}'.format(APP_USER, APP_NAME)
GIT_REPO = 'https://github.com/TracyWebTech/sentry-instance'

SOURCE_VENV = 'source /usr/local/bin/virtualenvwrapper.sh'
WORKON_ENV = '{} && workon {}'.format(SOURCE_VENV, VENV_NAME)

env.user = APP_USER
env.use_shell = False
env.hosts = ['162.243.127.83']


@with_settings(user='root')
def bootstrap():
    run('useradd {} -G sudo -m -s /bin/bash'.format(APP_USER), quiet=True)
    ssh_dir = '/home/{0}/.ssh/'.format(APP_USER)
    run('mkdir -p {0}; chmod 700 {0}'.format(ssh_dir))
    run('cp /root/.ssh/authorized_keys /home/{}/.ssh/'.format(APP_USER))
    run('chown -fR {0}:{0} {1}'.format(APP_USER, ssh_dir))

    sudoers_file = '/etc/sudoers.d/{}'.format(APP_USER)
    if not exists(sudoers_file):
        run('echo "{} ALL=NOPASSWD: ALL" > {}'.format(APP_USER, sudoers_file))
        run('chmod 440 {}'.format(sudoers_file))

    if not exists('/usr/bin/puppet'):
        aptget_install('puppet')

    if not exists('/usr/bin/git'):
        aptget_install('git')


def aptget_install(pkg):
    sudo('DEBIAN_FRONTEND=noninteractive apt-get install -y -q {}'.format(pkg))


def provision():
    sudo('puppet apply --modulepath={0}modules/ {0}manifests/init.pp'.format(
         REPO_PATH + '/puppet/'))


def upgrade_sentry():
    with prefix(WORKON_ENV):
        with cd(REPO_PATH):
            run('sentry --config=sentry_config.py upgrade')


def mkvirtualenv():
    if not exists('~/.virtualenvs/' + VENV_NAME):
        with prefix(SOURCE_VENV):
            run('mkvirtualenv ' + VENV_NAME)
            return True


def install_requirements():
    with cd(REPO_PATH), prefix(WORKON_ENV):
        run('pip install -r requirements.txt')


def update():
    if not exists(REPO_PATH):
        run('git clone {} {}'.format(GIT_REPO, REPO_PATH))

    with cd(REPO_PATH):
        run('git pull')

    provision()

    mkvirtualenv()
    install_requirements()
    upgrade_sentry()

    sudo('supervisorctl restart all')


def upload_ssl_cert(certificate, key):
    ssl_dir = '{}/ssl/'.format(REPO_PATH)
    cert_path = os.path.join(ssl_dir, APP_NAME+'.crt')
    key_path = os.path.join(ssl_dir, APP_NAME+'.key')

    run('mkdir -p {}'.format(ssl_dir))

    put(certificate, cert_path)
    put(key, key_path)

    run('chmod 600 {}'.format(key_path))
