import os
import webbrowser
from subprocess import TimeoutExpired, CalledProcessError, Popen
from sys import platform


def os_open_command():
    os_open_cmds = {'linux': 'xdg-open', 'win': 'start', 'darwin': 'open'}
    os_name = ''.join(ch for ch in platform if not ch.isdigit())
    return os_open_cmds[os_name] if os_name in os_open_cmds else 'open'


def _open_fallback(path):
    try:
        webbrowser.open(path)
    except:
        pass


def try_open(path):
    '''
    Versucht die Datei mit dem OS zugehörigen Standartprogram zu öffnen.
    '''
    try:
        open_with(path, os_open_command())
        return True
    except:
        _open_fallback(path)
        return False


def open_with(path, app):
    '''
    Öffnet das Program mit der angegeben Applikation.
    '''
    if not os.path.isfile(path):
        raise FileNotFoundError('File \'{}\' does not exist.'.format(path))

    runcmd('{} {}'.format(app, path))


def runcmd(command, cwd=None, timeout=None):
    args = command.split()
    FNULL = open(os.devnull, 'w')
    with Popen(args, stdout=FNULL, stderr=FNULL, cwd=cwd) as process:
        try:
            output, unused_err = process.communicate(timeout=timeout)
        except TimeoutExpired:
            process.kill()
            output, unused_err = process.communicate()
            raise TimeoutExpired(process.args, timeout, output=output)
        except:
            process.kill()
            process.wait()
            raise
        retcode = process.poll()
        if retcode:
            raise CalledProcessError(retcode, process.args, output=output)
    return output
