import contextlib

from fabric.api import *


env.hosts = ['la',]
env.use_ssh_config = True

server_project_dirs = {
    'prod': '~/webapps/laopenacres/livinglots-la',
}

server_collected_static = {
    'prod': '~/webapps/laopenacres_static',
}

server_virtualenvs = {
    'prod': 'laopenacres',
}

supervisord_programs = {
    'prod': 'laopenacres',
}

supervisord_conf = '~/var/supervisor/supervisord.conf'


@contextlib.contextmanager
def cdversion(version, subdir=''):
    """cd to the version indicated"""
    with prefix('cd %s' % '/'.join([server_project_dirs[version], subdir])):
        yield


@contextlib.contextmanager
def cdstatic(version, subdir=''):
    """cd to the version indicated"""
    with prefix('cd %s' % '/'.join([server_collected_static[version], subdir])):
        yield


@contextlib.contextmanager
def workon(version):
    """workon the version of indicated"""
    with prefix('workon %s' % server_virtualenvs[version]):
        yield

@task
def pull(version='prod'):
    with cdversion(version):
        run('git pull')


@task
def install_requirements(version='prod'):
    with workon(version):
        with cdversion(version):
            run('pip install -r requirements/base.txt')
            run('pip install -r requirements/production.txt')


@task
def build_static(version='prod'):
    with workon(version):
        run('django-admin.py collectstatic --noinput')
        with cdstatic(version, ''):
            run('bower install')
        with cdstatic(version, 'js'):
            run('r.js -o app.build.js')


@task
def syncdb(version='prod'):
    with workon(version):
        run('django-admin.py syncdb')


@task
def migrate(version='prod'):
    with workon(version):
        run('django-admin.py migrate')


@task
def restart_django(version='prod'):
    with workon(version):
        run('supervisorctl -c %s restart %s' % (supervisord_conf,
                                                supervisord_programs[version]))


@task
def restart_memcached():
    run('supervisorctl -c %s restart memcached' % supervisord_conf)


@task
def status():
    run('supervisorctl -c %s status' % supervisord_conf)


@task
def start(version='prod'):
    pull(version=version)
    install_requirements(version=version)
    syncdb(version=version)
    migrate(version=version)
    build_static(version=version)
    with workon(version):
        run('supervisorctl -c %s start %s' % (supervisord_conf,
                                              supervisord_programs[version]))


@task
def stop(version='prod'):
    with workon(version):
        run('supervisorctl -c %s stop %s' % (supervisord_conf,
                                             supervisord_programs[version]))


@task
def deploy():
    pull()
    install_requirements()
    syncdb()
    migrate()
    build_static()
    restart_django()


@task
def prepare_environment(version='prod'):
    # TODO
    # mkvirtualenv
    # clone code
    # add2virtualenv
    pass
