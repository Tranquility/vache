import string
import sqlite3
import base64
import json
import os
import subprocess
import db

SEP = ','


def resource_dir_for(doc_root):
    return string.replace(doc_root, os.path.basename(doc_root), 'Resources')


def doc_db_for(doc_root):
    return os.path.join(resource_dir_for(doc_root), 'docSet.dsidx')


def get_names(is_logging_enabled, metas):
    for meta, path in metas:
        doc_db = doc_db_for(path)
        encoded_meta = base64.b64encode(json.dumps(meta))
        try:
            yield path, encoded_meta, db.get_names(doc_db)
        except sqlite3.OperationalError as e:
            if is_logging_enabled:
                db.log_bad_docset_db(doc_db, e)
            pass


def get_encoded_names(is_logging_enabled, metas):
    for path, encoded_meta, sql_rows in get_names(is_logging_enabled, metas):
        for (name,) in sql_rows:
            yield path + SEP + encoded_meta + SEP + name


def get_url(path, meta, name):
    uri_path = db.get_uri_path(doc_db_for(path), name)
    absolute_path = os.path.join(
        resource_dir_for(path), 'Documents', uri_path
    )
    return 'file:///' + absolute_path


def decode_url(line):
    path, encoded_meta, name = string.split(line, SEP)
    return get_url(path, json.loads(base64.b64decode(encoded_meta)), name)


def get_plist_files_with_path(docset_root):
    out = subprocess.check_output(
        ['find', docset_root,
         '-maxdepth', '3',
         '-type', 'f',
         '-name', '*.plist']
    )

    return db.retrying(db.fetchplists, string.split(out, os.linesep))


def get_plist_files_for_platform_families(docset_root, families):
    for meta, path in get_plist_files_with_path(docset_root):
        try:
            if any([family == meta['DocSetPlatformFamily']
                    for family in families]):
                yield meta, path
        except KeyError:
            pass
