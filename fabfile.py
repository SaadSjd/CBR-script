from fabric.api import *

env.hosts = ['10.10.24.63']
env.user = 'root'
env.password = 'changeme'
env.disable_known_hosts = True
env.reject_unknown_hosts = False


def show_list():
    run('ls')


def upload_file():
    put(local_path='fso-plugins-1.4.0-beta-3.tar.gz', remote_path='/var/lib/fireeye/fso')


def un_tar():
    run('tar xzvf fso-plugins-1.4.0-beta-3.tar.gz')


def show_logs(line):
    # run('tail -f /var/log/fireeye/fso/web/web.log')
    run('tail -n %s /var/log/fireeye/fso/web/web.log | grep --color -e warn -e error' % line)


def plugin_install():

    with settings(prompts={'Are you sure you want to install above selected plugins? [yes|no] :': 'yes',
                           'Do you wish to restart FSO engine [yes|no] ? ': 'no'}):
        run('./fso_content_install')
        #
        # run('./fso_content_install -l -v -v -v -v -v -d -g')  # install dependencies of GA
        # show_logs(50)

        # run('./fso_content_install -l -v -v -v -v -v -n virus')  # install dependencies of GA by name
        # show_logs(10)

        # run('./fso_content_install -l -v -d -e')  # install dependencies of EA
        # show_logs(50)
        #
        #
        # run('./fso_content_install -l -v -d')  # install dependencies of all the plugins
        # show_logs(100)
        #
        # run('./fso_content_install -l -v -d -f')  # force re install dependencies of all plugins
        # show_logs(120)
        #
        #
        # run('./fso_content_install -l -v')  # install all the plugins
        # show_logs(150)
        # run('./fso_content_install -l -v -f')  # force re install all the plugins
        # show_logs(200)
        #
        # run('./fso_content_install -l -v -g -f')  # force re install all the plugins
        # show_logs(100)
        #
        #
        # run('./fso_content_install -l -v -e')  # install EA plugins
        # show_logs(50)
        # run('./fso_content_install -l -v -e -f')  # force re install EA plugins
        # show_logs(100)
        #
        #
        # # run('./ fso_content_install -l -v -s')  # install specific plugin
        # run('./fso_content_install -l -v -c SIEM')  # install plugins by category
        # show_logs(50)
        # run('./fso_content_install -l -v -m fso')  # install plugins by vendor name
        # show_logs(100)

        # run('./fso_content_install -l -v -v -v -v -v -m fso')
        # show_logs(500)
        #
        # run('source /etc/profile')
        #
        # outp = run('fsocontent status -i')


def content_info():
    outp = run('fsocontent status -i')
    content = ['Adapters', 'Commands', 'Custom Scripts', 'Devices', 'Mustache Templates', 'Parameter Types',
               'Playbooks', 'Plugins', 'Summary Forms', 'Tables', 'User Groups', 'Users']
    d = dict()

    for stri in content:
        a = table_parse(stri, outp)
        d[stri] = a
    print(d)


def table_parse(lis, outp):
    # outp = run('fsocontent status -i')
    idx = outp.find(lis)
    print (outp[idx])
    idx = idx + len(lis)
    print (outp[idx - 1])

    while outp[idx].isdigit() is False:
        idx = idx + 1
    print (outp[idx])

    value = []
    while outp[idx].isdigit() is True:
        value.append(outp[idx])
        idx = idx + 1

    return "".join(value)


def status_check():
    out = run('fsocontent check')
    content = ['Valid Plug-ins', 'Invalid Plug-ins', 'Plug-in Warnings', 'Total Plug-ins']
    d = dict()
    for stri in content:
        b = table_parse(stri, out)
        d[stri] = b
    print(d)


def main():
    with cd('/var/lib/fireeye/fso'):  # root user so path must be specified first
        run('uptime')
        # upload_file()
        # un_tar()
        # show_list()
        # content_info()
        status_check()
        with cd('/var/lib/fireeye/fso/fso-plugins-1.4.0-beta-3'):
            show_list()
            # plugin_install()


