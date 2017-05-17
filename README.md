# Netzpolitik.us petition code

This is the petition code used to run the site Netzpolitik.us. The code is written in Python 3, based on the [Django](https://www.djangoproject.com/) web framework. I use a sqlite3 database to store the signatures. By default this gets stored as `db.sqlite3` in the application root. This can be adjusted by modifying the `netzpolitik/settings.py` file.

## Deployment

For deployment I used [uwgsi](https://uwsgi-docs.readthedocs.org/en/latest/WSGIquickstart.html) to run the Python code. I installed Django in a Python 3 virtualenv, and set the `home` setting in the `netzpolitik_uwsgi.ini` file to the path of this virtualenv (so that it uwsgi can find Django). I started 10 uwsgi workers on a socket, and then hooked up nginx to act as a proxy for the requests. All static files are being served by nginx as well (under the `/static` url). The wsgi configuration files are included in the root of this repository.

### Required installed packages

First of all, make sure that the following is installed:

* Python 3
* nginx
* uwsgi
* uwsgi-plugin-python3
* virtualenv
* git

Install these using `apt-get`, or any other package manager that your distro uses. I'm going to assume Debian in this README.

### Clone & Setting up virtualenv

```
git clone https://github.com/sandervenema/netzpolitik
cd netzpolitik
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
./manage.py migrate
./manage.py createsuperuser
```

This installs all the dependencies into the virtualenv, so Python can find the required packages etc. and there will be no conflicts with packages already installed on the system. It will execute the required database migrations. It also asks you to create a super user for the backend admin interface (reachable by default via `/openletter/admin`).

You should be able to deactivate the virtualenv after installing the required packages; we're going to later tell uwsgi to use the virtualenv environment. Exit the virtualenv by typing: `deactivate`.

### Setting up uwsgi

**Make sure you edit the `netzpolitik_uwsgi.ini` file to correct the paths!**

After editing the ini file, first check whether uwsgi works by executing:

```
uwsgi netzpolitik_uwsgi.ini
```

This should start 10 workers and the socket should now be created under /tmp. Check the log file to make sure. See **Basic nginx configuration** later in this README to see how to hook nginx up to this. Press `CTRL-C` to exit and kill the workers.

#### Daemonising uwsgi

To make sure that uwsgi stays up and starts when we start the server, we're going to daemonise, and use uwsgi's emperor mode to manage the app. We will use standard systemd tools to manage uwsgi in the future. To make this happen, we're first going to create the `/etc/uwsgi/emperor.ini` file, with the following contents:

```
[uwsgi]
emperor = /etc/uwsgi/vassals
uid = www-data
gid = www-data
```

Then we're going to create the vassals directory, and symlink our `netzpolik_uwsgi.ini` script in this repository to that location:

```
mkdir /etc/uwsgi/vassals
cd /etc/uwsgi/vassals
ln -s /path/to/this/repository/netzpolitik_uwsgi.ini netzpolitik_uwsgi.ini
```

So now when we will start uwsgi in emperor mode, it will know of our application. Go ahead and try it now by executing `uwsgi /etc/uwsgi/emperor.ini`. It should find the vassal and start the 10 workers again.

If you're getting permission denied errors, it's most likely because the log file cannot be created (because you run as www-data). In that case, fix permissions, or create the logfile in advance and fix permissions:

```
touch /var/log/netzpolitik.log
chown www-data:www-data /var/log/netzpolik.log
chmod 755 /var/log/netzpolitik.log
```

Also make sure the files in the repo directory is owned by the same user, so it can write to the database etc.:

```
chown -R www-data:www-data /path/to/netzpolik/git/working/directory
```

Once that's working, we need to create a systemd service file. Create a file at `/etc/systemd/system/emperor.uwsgi.service` and put the following into it:

```
[Unit]
Description=uWSGI Emperor
After=syslog.target

[Service]
ExecStart=/usr/bin/uwsgi --ini /etc/uwsgi/emperor.ini
# Requires systemd version 211 or newer:
RuntimeDirectory=uwsgi
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

Now run it using:

```
systemctl start emperor.uwsgi.service
```

and check it's status with:

```
systemctl status emperor.uwsgi.service
```

You should see in the output that it is now governing one vassal (our application). You can quit it using:

```
systemctl stop emperor.uwsgi.service
```

With uwsgi now running as a service, we can hook up nginx to serve the app under the right URL, do TLS config and serve static files.

### Basic nginx configuration

For nginx I used a basic config like the one below. I stripped a few non-relevant things from the config, but this is the basic gist.

```
upstream django {
  server unix:///tmp/netzpolitik.sock;
}

server {
   listen 80;
   listen 443 ssl spdy;
   server_name netzpolitik.us www.netzpolitik.us;
   
   # ssl settings here...
   
   add_header Strict-Transport-Security max-age=31536000;
   add_header X-Frame-Options DENY;
   spdy_headers_comp 6;
   
   # force TLS
   if ($scheme = http) {
     return 301 https://$server_name$request_uri;
   }
   
   location /static {
     alias /path/to/app/static;
   }
   
   location /openletter {
     uwsgi_pass django;
     include /path/to/uwsgi_params;
   }
}
```

And that should be all there is to it. Once you have uwsgi started and listening on a socket, and you set up nginx to act as the proxy, you should be good to go. If you need a little more info, check [how to deploy Django](https://uwsgi-docs.readthedocs.org/en/latest/WSGIquickstart.html#deploying-django) (from the uwsgi site).
