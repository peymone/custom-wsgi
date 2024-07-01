<h1 align="center">Custom WSGI</h1>

<p align="center">
    <img src="https://img.shields.io/github/downloads/peymone/custom-wsgi/total?style=social&logo=github" alt="downloads">
    <img src="https://img.shields.io/github/watchers/peymone/custom-wsgi" alt="watchers">
    <img src="https://img.shields.io/github/stars/peymone/custom-wsgi" alt="stars">
</p>

<h2>About</h2>

**_This application was created to demonstrate the interaction between a proxy server like nGinx, a WSGI gateway (an application server such as Gunicorn) and web frameworks such as Flask._**

_And also to consider something like this:_

* _load balancing on application servers (you can change number of application servers in config.ini)_
* _asynchronous works using the select system call and generators (proxy.py)_

<h2>DevOps via python installation</h2>

* Install python from [offisial site](https://www.python.org/downloads/)
  
_<p>Proxy server</p>_

* Download latest proxy release from my GitHub
* Configurate config.ini file
    * Server - proxy server configuration (host and port)
    * WSGI - application server configuration (host and port)
* Open terminal in project directory and ebter the command: `python proxy.py`

> _you can list more than one WSGI servers_

_<p>Application server</p>_

* Download latest wsgi release from my GitHub
* Configurate config.ini file:
    * WSGI - path to WSGI application and function with realization of WSGI protocol
    * Server - application server configuration (host and port)
* Open terminal in project directory and ebter the command: `python app.py`

