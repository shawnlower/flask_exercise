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

The Vagrantfile that ships with the repo allows the automated creation of a CentOS/7 Vagrant box, which uses Ansible to provision the application. The steps are roughly:

0. Pull down base CentOS/7 box, and boot it
0. Install ansible within the new VM
0. Install git and nginx via ansible
0. Setup firewall, configs and SELinux
0. Clone our repo
0. Setup virtualenv with required packages
0. Setup users, permissions, and systemd service file
0. Enable and start our services

Example
-------

```
(.venv)[sstar@sstar01-lt tools]$ ( /usr/bin/time vagrant up ) |& tee vagrant_log
Bringing machine 'default' up with 'libvirt' provider...
==> default: Creating image (snapshot of base box volume).
==> default: Creating domain with the following settings...
==> default:  -- Name:              tools_default
==> default:  -- Domain type:       kvm
==> default:  -- Cpus:              1
==> default:  -- Memory:            1024M
==> default:  -- Management MAC:    
==> default:  -- Loader:            
==> default:  -- Base box:          centos/7
[...]
TASK [create our service file] *************************************************
changed: [default]

TASK [enable and start our service] ********************************************
changed: [default]

PLAY RECAP *********************************************************************
default                    : ok=15   changed=14   unreachable=0    failed=0   

1.73user 0.25system 4:00.68elapsed 0%CPU (0avgtext+0avgdata 96592maxresident)k
1928inputs+448outputs (2major+45447minor)pagefaults 0swaps
```

Above, we see that it took about 4 minutes to build our VM. The initial download of the CentOS base box may take significantly longer, depending on your connection speed.

Testing our Vagrant box
-----------------------

Since we should still have our local git checkout on the host, we can now issue the same curl commands, and point it at our VM.

- First, grab our IP address

```
[sstar@sstar01-lt tests]$ ip=$(vagrant ssh-config | grep HostName | awk '{print $2}'); echo $ip
192.168.121.90
```

[sstar@sstar01-lt tests]$ ./make_requests.sh $ip
```
[...]
======================
Running test 5: curl -v -H "Content-Type: application/json" -d '{"bar": "This is a bar test from curl"}' 192.168.121.90
======================
* Rebuilt URL to: 192.168.121.90/
*   Trying 192.168.121.90...
* Connected to 192.168.121.90 (192.168.121.90) port 80 (#0)
> POST / HTTP/1.1
> Host: 192.168.121.90
> User-Agent: curl/7.43.0
> Accept: */*
> Content-Type: application/json
> Content-Length: 39
> 
* upload completely sent off: 39 out of 39 bytes
< HTTP/1.1 422 UNPROCESSABLE ENTITY
< Server: nginx/1.10.1
< Date: Sat, 24 Sep 2016 02:06:04 GMT
< Content-Type: text/html; charset=utf-8
< Content-Length: 35
< Connection: keep-alive
< 
* Connection #0 to host 192.168.121.90 left intact
Bad Request (Key not found in JSON)


*** 5 tests run, 0 returned non-zero ***
```

