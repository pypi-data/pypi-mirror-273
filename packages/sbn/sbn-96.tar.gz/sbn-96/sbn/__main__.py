# This file is placed in the Public Domain.
#
# pylint: disable=C0413,W0212,W0611


"main"


import getpass
import os
import pathlib
import pwd
import readline
import sys
import termios
import time


sys.path.insert(0, os.getcwd())


from sbn.client  import Client, cmnd, parse
from sbn.disk    import Workdir, skel
from sbn.handler import Event
from sbn.log     import debug, enable
from sbn.object  import Default
from sbn.run     import broker, init, scan
from sbn.thread  import errors, setout


from sbn import modules


Cfg             = Default()
Cfg.dis         = ""
Cfg.mod         = "cmd,err,log,mod,req,tdo,thr,tmr"
Cfg.opts        = ""
Cfg.name        = "sbn"
Cfg.version     = "96"
Cfg.wdr         = os.path.expanduser(f"~/.{Cfg.name}")
Cfg.pidfile     = os.path.join(Cfg.wdr, f"{Cfg.name}.pid")


Workdir.workdir = Cfg.wdr


class Console(Client):

    "Console"

    def __init__(self):
        Client.__init__(self)
        broker.add(self)

    def announce(self, txt):
        "disable announce."

    def callback(self, evt):
        "wait for callback."
        Client.callback(self, evt)
        evt.wait()

    def poll(self):
        "poll console and create event."
        evt = Event()
        evt.orig = object.__repr__(self)
        evt.txt = input("> ")
        evt.type = "command"
        return evt

    def say(self, _channel, txt):
        "print to console"
        txt = txt.encode('utf-8', 'replace').decode()
        print(txt)


def daemon(pidfile, verbose=False):
    "switch to background."
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    pid2 = os.fork()
    if pid2 != 0:
        os._exit(0)
    if not verbose:
        with open('/dev/null', 'r', encoding="utf-8") as sis:
            os.dup2(sis.fileno(), sys.stdin.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as sos:
            os.dup2(sos.fileno(), sys.stdout.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as ses:
            os.dup2(ses.fileno(), sys.stderr.fileno())
    os.umask(0)
    os.chdir("/")
    if os.path.exists(pidfile):
        os.unlink(pidfile)
    path = pathlib.Path(pidfile)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(pidfile, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def daemoned():
    "run in background"
    Cfg.opts += "d"
    main()


def privileges(username):
    "drop privileges."
    pwnam = pwd.getpwnam(username)
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)


def wrap(func):
    "restore console."
    old2 = None
    try:
        old2 = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        print("")
    finally:
        if old2:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old2)


def main():
    "main"
    parse(Cfg, " ".join(sys.argv[1:]))
    skel()
    if not "d" in Cfg.opts:
        enable(print)
        setout(print)
    if "a" in Cfg.opts:
        Cfg.mod = ",".join(modules.__dir__())
    if "v" in Cfg.opts:
        dte = " ".join(time.ctime(time.time()).replace("  ", " ").split()[1:])
        debug(f'{dte} {Cfg.name.upper()} {Cfg.opts.upper()} {Cfg.mod.upper()}')
    if "h" in Cfg.opts:
        print(__doc__)
    if "d" in Cfg.opts:
        Cfg.mod  = ",".join(dir(modules))
        Cfg.user = getpass.getuser()
        daemon(Cfg.pidfile, "-v" in sys.argv)
        privileges(Cfg.user)
        scan(modules, Cfg.mod)
        init(modules, Cfg.mod)
        while 1:
            time.sleep(1.0)
        return
    scan(modules, Cfg.mod, Cfg.sets.dis)
    if "c" in Cfg.opts:
        init(modules, Cfg.mod, Cfg.sets.dis)
        csl = Console()
        csl.start()
        while 1:
            time.sleep(1.0)
    elif Cfg.otxt:
        cmnd(Cfg.otxt, print)


if __name__ == "__main__":
    main()
    errors()
