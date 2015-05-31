import sqlite3
import plistlib
import platform
import os
import sys
import cPickle

USER_CACHE_DIR = None
if platform.system() == 'Windows':
    USER_CACHE_DIR = os.environ['LocalAppData']
elif platform.system() == 'Linux':
    try:
        USER_CACHE_DIR = os.environ['XDG_CACHE_HOME']
    except KeyError:
        USER_CACHE_DIR = os.path.join(os.environ['HOME'], '.cache')
elif platform.system() == 'Darwin':
    USER_CACHE_DIR = os.path.join(os.environ['HOME'], 'Library/Caches')
else:
    print 'could not recognise platform: ', platform.system()
    sys.exit(1)

VACHE_CACHE_DIR = os.path.join(USER_CACHE_DIR, 'vache')
DOC_SET_PLATFORM_FAMILY_CACHE_PATH = os.path.join(
    VACHE_CACHE_DIR, 'DocSetPlatformFamily.cache'
)
if not os.path.exists(DOC_SET_PLATFORM_FAMILY_CACHE_PATH):
    if not os.path.exists(VACHE_CACHE_DIR):
        os.makedirs(VACHE_CACHE_DIR)

    with open(DOC_SET_PLATFORM_FAMILY_CACHE_PATH, 'w') as f:
        conn = sqlite3.connect(DOC_SET_PLATFORM_FAMILY_CACHE_PATH)
        conn.execute('CREATE TABLE t (path BLOB, plist BLOB)')


def get_names(doc_db):
    conn = sqlite3.connect(doc_db)
    c = conn.cursor()
    c.execute('SELECT name FROM searchIndex')
    return c


def get_uri_path(doc_db, name):
    conn = sqlite3.connect(doc_db)
    c = conn.cursor()
    c.execute('SELECT path FROM searchIndex WHERE name = ?', (name,))
    (out,) = c.fetchone()
    return out


def retrying(f, x):
    try:
        return f(x)
    except:
        return retrying(f, x)


def fetchplists(paths):
    with sqlite3.connect(DOC_SET_PLATFORM_FAMILY_CACHE_PATH) as conn:
        conn.text_factory = str
        c = conn.cursor()
        cache = {}
        c.execute('SELECT * FROM t')
        for path, plist in c:
            cache[path] = cPickle.loads(plist)
        newInserts = {}

        for path in paths:
            if not path:
                break

            if path in cache:
                yield cache[path], path
            else:
                parsed = plistlib.readPlist(path)
                cache[path] = parsed
                newInserts[path] = parsed
                yield parsed, path

        for k, v in newInserts.iteritems():
            c.execute(
                'INSERT INTO t (path, plist) VALUES (?, ?)',
                (k, cPickle.dumps(v))
            )
