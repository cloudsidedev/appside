Changes
=======

Appflow 1.0.1.5
~~~~~~~~~~~~~~~
Minor update introducing:
    - Appflow-playbooks versioning
    - Appflow-playbooks selectable branch
    - `appflow version` will now yield also the playbooks version:
        ``Appflow Version: 1.0.1.5``
        ``Playbooks Version 1.0.0``

Appflow 1.0.1.4
~~~~~~~~~~~~~~~

Released a little update including
    - introduced appflow version command
    - introduced appflow provision debug
    - fixed newline bug in appflow hosts

to update just use Pip: `pip3 install -U appflow`


Screencasts
~~~~~~~~~~~

To complement the documentation, we've added screencasts recorded on `asciinema.org <http://asciinema.org/>`__

Screencasts include the walkthrought of the basic setups and features of Appflow.
They include:
    
    - `Installation`_
    - `Basic setup`_
    - `Atlantis setup`_
    - `Atlantis provision`_
    - `Project provision`_


Varnish Grace mode
~~~~~~~~~~~~~~~~~~

`Grace mode <https://varnish-cache.org/docs/5.1/users-guide/vcl-grace.html>`_ has been a long expected feature and went production ready with
recent appflow-playbooks commit `f0d7f3817ffb1b2354f0c24a98e3dac37b72202d <https://github.com/ttssdev/appflow-playbooks/commit/f0d7f3817ffb1b2354f0c24a98e3dac37b72202d>`_.

This special operation mode in Varnish allows a website to remain online and running also when the backend components, like
MySQL or Apache2, are not running. This works beccause Varnish will serve all the web content directly from it's cache.

Backend operations like login to CMS or similar will obviously not work as expected but at least the public facing part of the
website will not be offline, so no 404s or similar for end-users.

Grace period is set by default to 6h but can be extended to one week or whatever your preference is, the main advantage
of Grace is that your site remains up when bad things happen and you'll get a time buffer for fixing whatever issue happened
to the backend.

Grace mode will be enabled by default, for any environment, if you perform:

::

    % appflow update
    % appflow provision --tags varnish-conf,apache2-conf,mysql

It's important to note that Grace mode is active by default from Varnish 5.1 upwards so if you're on 3.x
you'll need to upgrade varnish first, this can be done, in development, by:

::

    % appflow update
    % ssh atlantis "sudo service varnish stop"
    % appflow provision --tags varnish,apache2-conf,mysql

You also need to set the Varnish version in ``group_vars/webservers``:

::

    #
    # Varnish
    #
    conf_varnish_version: 51
    ...

a complete config setting for Varnish 5.1 and Grace would look like:

::

    #
    # Varnish
    #
    conf_varnish_version: 51
    conf_varnish_listen_port: 6081
    conf_varnish_listen_admin_port: 60821
    conf_varnish_backend_default: |
    .host = "127.0.0.1";
    .port = "8080";
    .max_connections = 800;
    conf_varnish_acl_purge: |
    "127.0.0.1";
    "localhost";
    "192.168.80.2";
    conf_varnish_vcl_recv: |
    {% if conf_lbtier_enable == false %}
    remove req.http.X-Forwarded-For;
    set req.http.X-Forwarded-For = client.ip;
    {% endif %}

    if (req.url ~ "/wp(-login|-admin|-cron|login|-comments-post.php)" ) {
        return (pass);
    }

    if (req.http.Cache-Control ~ "no-cache") {
        return (pass);
    }

    # Remove client-side cookies.
    set req.http.Cookie = regsuball(req.http.Cookie, "(^|;\s*)(_[_a-z]+|has_js|utmctr|utmcmd.|utmccn.|WT_FPC|_hjIncludedInSample)=[^;]*", "");

    # Remove a ";" prefix, if present.
    set req.http.Cookie = regsub(req.http.Cookie, "^;\s*", "");

    # Are there cookies left with only spaces or that are empty?
    if (req.http.cookie ~ "^\s*$") {
        unset req.http.cookie;
    }

    conf_varnish_vcl_backend_response: |
    # Allow stale content, in case the backend goes down.
    # make Varnish keep all objects for 6 hours beyond their TTL
    set beresp.grace = 6h;
    # set beresp.grace = 2m;

    conf_varnish_vcl_fetch: |
    # set beresp.grace = 2m;

    # If the URL is for one of static images or documents, we always want them to be cached.
    if (beresp.status == 200 && req.url ~ "\.(ico|jpe?g|jpe|gif|png|webp|svg|css|js)$") {
    # Cookies already removed.
    # Cache the page for 10 days.
        set beresp.ttl = 10d;
    # Remove existing Cache-Control headers.
        remove beresp.http.Cache-Control;
    # Set new Cache-Control headers for browser to store cache for 7 days.
        set beresp.http.Cache-Control = "public, max-age=604800";
    }

    # Cache 404 responses for 15 seconds.
    if (beresp.status == 404) {
        set beresp.ttl = 15s;
        set beresp.grace = 15s;
    }

    conf_varnish_vcl_deliver: |
    # For security and asthetic reasons, remove some HTTP headers before final delivery.
    unset resp.http.Server;
    unset resp.http.X-Powered-By;
    unset resp.http.Via;
    unset resp.http.X-Varnish;
    Once Varnish has been updated and Grace mode has been enabled you could test if it's working correctly:

    
Open one of the web projects you're hosting on Atlantis in the browser, everything should be there.

::

    % curl http://atlantis:8080/health.php
    MySQL running

    % ssh atlantis "sudo varnishadm backend.list"
    Backend name                   Admin      Probe
    boot.default                   probe      Healthy

    % ssh atlantis "sudo service mysql stop"

    % ssh atlantis "sudo varnishadm backend.list"
    Backend name                   Admin      Probe
    boot.default                   probe      Sick

Open the previous web project again in the browser, the website should be online as usual via Grace mode.

The same concept applies also to production where we have three or more nodes.


.. start-badges

.. _Installation: https://asciinema.org/a/0lglEIPiYhsceMExzOKHBUcdZ?autoplay=1&speed=1
.. _Basic setup: https://asciinema.org/a/VRlp5YqiT4gvKXrYFYZW9Oz3l?autoplay=1&speed=1
.. _Atlantis setup: https://asciinema.org/a/pcApeQ82UF7kXrygK5jnv9GBA?autoplay=1&speed=1
.. _Atlantis provision: https://asciinema.org/a/BlCYYwDRMFAg31XrfwAY6Z8yc?autoplay=1&speed=1
.. _Project provision: https://asciinema.org/a/lWERm9quxFM91hBnGDBr1UIgH?autoplay=1&speed=1
