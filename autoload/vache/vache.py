import string
import sqlite3
import os
import subprocess
import platform

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
            prefix = str(plist[u'DocSetPlatformFamily']) + SEP
        except KeyError:
            prefix = 'unknown' + SEP

        try:
            for (name,) in db.get_names(doc_db):
                yield prefix + name

        except sqlite3.OperationalError as e:
            db.log_bad_docset_db(doc_db, e)


def get_url(doc_paths, name):
    try:
        for doc_db, resource_dir in doc_paths:
            uri_path = db.get_uri_path(doc_db, name)
            if uri_path is None:
                continue

            absolute_path = os.path.join(
                resource_dir, 'Documents', uri_path
            )
            return {'ok': 'file:///' + absolute_path}

    except sqlite3.OperationalError as e:
        db.log_bad_docset_db(doc_db, e)
        return {'error': repr(e)}

    except db.NameMatchFailure as e:
        db.log_bad_name_match(doc_db, name)
        return {'error': repr(e)}


def doc_paths_for(plists):
    for _, path in plists:
        yield doc_db_for(path), resource_dir_for(path)


def construct_url(docset_root, line):
    family, name = string.split(line, SEP)
    plists = get_plist_files_for_families(docset_root, [str(family)])
    doc_paths = doc_paths_for(plists)
    return get_url(doc_paths, name)


def get_plist_files(docset_root):
    maxdepth = '3'
    if platform.system() == 'Darwin':
        maxdepth = '4'

    find_p = subprocess.Popen(
        ['find', docset_root,
         '-maxdepth', maxdepth,
         '-type', 'f',
         '-name', '*.plist'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = find_p.communicate()
    if find_p.returncode != 0:
        print 'get_docsets.py :', err

    return db.fetchplists(string.split(out, os.linesep))


def get_plist_files_for_families(docset_root, families):
    for plist, path in get_plist_files(docset_root):
        try:
            if any([family == plist['DocSetPlatformFamily']
                    for family in families]):
                yield plist, path

        except KeyError as e:
            db.log_bad_plist(plist, e)
        except GeneratorExit as e:
            raise e
        except BaseException as e:
                raise Exception('{} : {} : {}'.format(
                    docset_root, families, repr(e)
                ))
