import string
import sqlite3
import os
import subprocess

import db

SEP = '\t'


def resource_dir_for(doc_root):
    return string.replace(doc_root, os.path.basename(doc_root), 'Resources')


def doc_db_for(doc_root):
    return os.path.join(resource_dir_for(doc_root), 'docSet.dsidx')


def get_names(plists):
    for plist, path in plists:
        doc_db = doc_db_for(path)

        prefix = None
        try:
            prefix = path + SEP + str(plist[u'DocSetPlatformFamily']) + SEP
        except KeyError:
            prefix = path + SEP + 'unknown' + SEP

        try:
            for (name,) in db.get_names(doc_db):
                yield prefix + name

        except sqlite3.OperationalError as e:
            db.log_bad_docset_db(doc_db, e)


def get_url(path, name):
    uri_path = db.get_uri_path(doc_db_for(path), name)
    absolute_path = os.path.join(
        resource_dir_for(path), 'Documents', uri_path
    )
    return 'file:///' + absolute_path


def decode_url(line):
    path, family, name = string.split(line, SEP)
    return get_url(path, name)


def get_plist_files(docset_root):
    out = subprocess.check_output(
        ['find', docset_root,
         '-maxdepth', '4',
         '-type', 'f',
         '-name', '*.plist']
    )

    return db.fetchplists(string.split(out, os.linesep))


def get_plist_files_for_families(docset_root, families):
    for plist, path in get_plist_files(docset_root):
        try:
            if any([family == plist['DocSetPlatformFamily']
                    for family in families]):
                yield plist, path

        except KeyError as e:
            db.log_bad_plist(plist, e)
