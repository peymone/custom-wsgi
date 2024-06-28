<h1 align="center">Custom WSGI</h1>

<p align="center">
    <img src="https://img.shields.io/github/downloads/peymone/custom-wsgi/total?style=social&logo=github" alt="downloads">
    <img src="https://img.shields.io/github/watchers/peymone/custom-wsgi" alt="watchers">
    <img src="https://img.shields.io/github/stars/peymone/custom-wsgi" alt="stars">
</p>

<h2>About</h2>

**_This application was created to demonstrate the interaction between a proxy server, a WSGI gateway (an application server such as Gunicorn) and web frameworks such as Flask._**

**_And also to consider something like:_**
**_* load balancing on application servers_**
**_* data encryption using SSH_**

**_Plus you can see how async works using the select system call and generators (proxy.py)_**


<h2>Program launch</h2>

* _Configurate config.ini file:_
    * _ModulePath - name of your wsgi application_
    * _ApplicationName - name of callable class instans in wsgi application_
    * _Host - server host_
    * _Port - server port_
* _Open terminal in progect directory_
* _Launch application `python wsgi.py`_

<br>

> _Explore this as you please_ 