flask_exercise
==============

This is a basic flask application demonstrating a few features, such as inspecting HTTP headers, receiving and acting upon POST data, and using environment-based configuration.

The tools directory also contains a working Vagrantfile and simple Ansible playbook for setting up the application.

*NOTE: You will require internet access from the guest, as installation involves pulling directly from github.*

Installation
------------

These installation steps cover what is necessary to setup and run the application interactively. For a persistent configuration using a systemd service file, please see the accompanying Ansible playbook.

First, clone the repo
```
[sstar@sstar01-lt scratch_space]$ git clone https://github.com/shawnlower/flask_exercise
Cloning into 'flask_exercise'...
remote: Counting objects: 96, done.
remote: Compressing objects: 100% (69/69), done.
remote: Total 96 (delta 24), reused 94 (delta 22), pack-reused 0
Unpacking objects: 100% (96/96), done.
Checking connectivity... done.
[sstar@sstar01-lt scratch_space]$ cd flask_exercise/
[sstar@sstar01-lt flask_exercise]$ 
```

Next, setup the virtualenv to isolate our dependencies
```
[sstar@sstar01-lt flask_exercise]$ virtualenv venv
New python executable in venv/bin/python2
Also creating executable in venv/bin/python
Installing setuptools, pip...done.
[sstar@sstar01-lt flask_exercise]$ . venv/bin/activate
```

The external dependencies are documented in the requirements.txt file, so we'll use that to install what we need.
```
(venv)[sstar@sstar01-lt flask_exercise]$ pip install -r requirements.txt 
[...]
Successfully installed Flask-0.10.1 Jinja2-2.8 MarkupSafe-0.23 Werkzeug-0.11.11 itsdangerous-0.24
```

We still haven't installed our application within the virtual environment, so we'll do that now. Normally this will pull from the remote PyPI, but since we've cloned the repo, we can just specify a local installation by using '.' as the name.
```
(venv)[sstar@sstar01-lt flask_exercise]$ pip install .
You are using pip version 6.0.8, however version 8.1.2 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
Processing /tmp/scratch_space/flask_exercise
Installing collected packages: flask-exercise
  Running setup.py install for flask-exercise
Successfully installed flask-exercise-0.1
```

Our code is now installed to our 'site-packages' directory within the virtualenv. This is enough to allow us to run the unit tests
```
(venv)[sstar@sstar01-lt flask_exercise]$ python tests/test_basic.py 
.....
----------------------------------------------------------------------
Ran 5 tests in 0.011s

OK
```
(Some more verbose output might be nice...)

We haven't specified an entrypoint for our code, and thus no binaries are created, so we'll need to run the file directly:
```
(venv)[sstar@sstar01-lt flask_exercise]$ python venv/lib/python2.7/site-packages/flask_exercise/flask_exercise.py
Server mode set to True
 * Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)
```
If we need to change the listening port, we can export e.g. SERVER_PORT=80


The tests directory also contains some shell scripts for issuing curl requests. It is *not* an actual test suite, as it does not validate return values, but it does allow us to inspect the output manually, and view warnings when we fail catastrophically.
This should be executed from a second shell, otherwise our app won't be running.
```
[sstar@sstar01-lt flask_exercise]$ ./tests/make_requests.sh 
url is set to: http://localhost:8080/
======================
Running test 1: curl -v http://localhost:8080/
======================
*   Trying 127.0.0.1...
* Connected to localhost (127.0.0.1) port 8080 (#0)
> GET / HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/7.43.0
> Accept: */*
> 
[...]

*** 5 tests run, 0 returned non-zero ***
```

In the first window, we should now see a log of all of the requests that we made via curl.
```
(venv)[sstar@sstar01-lt flask_exercise]$ python venv/lib/python2.7/site-packages/flask_exercise/flask_exercise.py
Server mode set to True
 * Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)

127.0.0.1 - - [24/Sep/2016 08:33:42] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [24/Sep/2016 08:33:42] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [24/Sep/2016 08:33:42] "GET / HTTP/1.1" 200 -
Someone posted a foo containing 'This is a foo test from curl'
a127.0.0.1 - - [24/Sep/2016 08:33:42] "POST / HTTP/1.1" 422 -
```

And similar messages in our log file
```
[sstar@sstar01-lt flask_exercise]$ cat server_log 
2016-09-24 08:32:09,099  INFO  Server mode set to True
2016-09-24 08:32:19,010  INFO  Server mode set to True
2016-09-24 08:33:42,457  INFO  Someone posted a foo containing 'This is a foo test from curl'
```

Vagrant test machine
---------------------

