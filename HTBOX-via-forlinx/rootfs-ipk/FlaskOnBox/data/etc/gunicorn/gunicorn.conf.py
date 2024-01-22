import multiprocessing
import os

debug = False
if debug:
    # Debugging
    reload = True
    reload_engine = 'auto'

    # Logging
    os.system("mkdir -p log")
    accesslog = "log/access.log"
    errorlog = "log/error.log"
    loglevel = 'debug'
    capture_output = True

    # Server Mechanics
    daemon = False
    os.system("mkdir -p run")
    pidfile = "run/gunicorn.pid"

    # Server Socket
    bind = "127.0.0.1:5000"

    # Worker Processes
    workers = 1
    threads = 1

else:
    # Logging
    os.system("mkdir -p /var/log/gunicorn")
    accesslog = "/var/log/gunicorn/access.log"
    errorlog = "/var/log/gunicorn/error.log"
    loglevel = 'warning'
    capture_output = True

    # Server Mechanics
    daemon = True
    pidfile = "/var/run/gunicorn.pid"
    user = "www-data"
    group = "www-data"

    # Server Socket
    bind = "0.0.0.0:8000"

    # Worker Processes
    workers = multiprocessing.cpu_count() * 2 + 1
    threads = multiprocessing.cpu_count() * 2 + 1
