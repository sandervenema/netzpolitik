# Netzpolitik.us petition code

This is the petition code used to run the site [Netzpolitik.us](https://netzpolitik.us/statement/). The code is written in Python 3, based on the [Django](https://www.djangoproject.com/) web framework. I use a sqlite3 database to store the signatures. By default this gets stored as `db.sqlite3` in the application root. This can be adjusted by modifying the `netzpolitik/settings.py` file.

## Deployment

For deployment I used [uwgsi](https://uwsgi-docs.readthedocs.org/en/latest/WSGIquickstart.html) to run the Python code. I installed Django in a Python 3 virtualenv, and set the `home` setting in the `netzpolitik_uwsgi.ini` file to the path of this virtualenv (so that it uwsgi can find Django). I started 10 uwsgi workers on a socket, and then hooked up nginx to act as a proxy for the requests. All static files are being served by nginx as well (under the `/static` url). The wsgi configuration files are included in the root of this repository.

### Basic nginx configuration

For nginx I used a basic config like the one below. I stripped a few non-relevant things from the config, but this is the basic gist.

```
upstream django {
  server unix:///path/to/netzpolitik.sock;
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
   
   location /statement {
     uwsgi_pass django;
     include /path/to/uwsgi_params;
   }
}
```

And that should be all there is to it. Once you have uswgi started and listening on a socket, and you set up nginx to act as the proxy, you should be good to go. If you need a little more info, check [how to deploy Django](https://uwsgi-docs.readthedocs.org/en/latest/WSGIquickstart.html#deploying-django) (from the uswgi site).
