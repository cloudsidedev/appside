
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
