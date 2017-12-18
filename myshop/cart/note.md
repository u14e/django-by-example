Django offers the following options for storing session data:
- **Database sessions**: Session data is stored in the database. This is the default
session engine.
- **File-based sessions**: Session data is stored in the file system.
- **Cached sessions**: Session data is stored in a cache backend. You can specify
cache backends using the  CACHES setting. Storing session data in a cache
system offers best performance.
- **Cached database sessions**: Session data is stored in a write-through cache
and database. Reads only use the database if the data is not already in
the cache.
- **Cookie-based sessions**: Session data is stored in the cookies that are sent
to the browser.

You can customize sessions with other settings. Here are some of the important
session related settings:
- **SESSION_COOKIE_AGE** : This is the duration of session cookies in seconds. The
default value is  1209600 (2 weeks).
- **SESSION_COOKIE_DOMAIN** : This domain is used for session cookies. Set this to
.mydomain.com to enable cross-domain cookies.
- **SESSION_COOKIE_SECURE** : This is a boolean indicating that the cookie should
only be sent if the connection is an HTTPS connection.
- **SESSION_EXPIRE_AT_BROWSER_CLOSE** : This is a boolean indicating that the
session has to expire when the browser is closed.
- **SESSION_SAVE_EVERY_REQUEST** : This is a boolean that, if  True , will save
the session to the database on every request. The session expiration is also
updated each time.

设置SESSION_EXPIRE_AT_BROWSER_CLOSE为True之后，SESSION_COOKIE_AGE就不起作用了，
也可以在 request.session.set_expiry()中设置当前session的期限