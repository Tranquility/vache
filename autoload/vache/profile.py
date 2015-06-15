import vache
import cProfile
import pstats
import os
import sys
import string
import platform

DOCSET_ROOT = None
if os.path.isdir('./test-data'):
    DOCSET_ROOT = os.path.join(os.getcwd(), 'test-data/docsets')
elif platform.system() == 'Linux':
    DOCSET_ROOT = os.path.join(
        os.environ['HOME'],
        '.local/share/Zeal/Zeal/docsets'
    )
elif platform.system() == 'Darwin':
    DOCSET_ROOT = os.path.join(
        os.environ['HOME'],
        'Library/Application Support/Dash/DocSets'
    )
elif platform.system() == 'Windows':
    DOCSET_ROOT = os.path.join(
        os.environ['APPDATA'],
        'Local/Zeal/Zeal/docsets'
    )
else:
    print 'could not recognise platform:', platform.system()
    sys.exit(1)


def family_names():
    plists = vache.get_plist_files_for_families(DOCSET_ROOT, ['go'])
    for _ in vache.get_names(plists):
        pass


def all_names():
    plists = vache.get_plist_files(DOCSET_ROOT)
    for _ in vache.get_names(plists):
        pass


def all_urls():
    last_family = None
    doc_paths = None
    bad_family = False
    bad_families = []

    for line in vache.get_names(vache.get_plist_files(DOCSET_ROOT)):
        family, name = string.split(line, '\t')
        if family != last_family:
            doc_paths = list(vache.doc_paths_for(
                vache.get_plist_files_for_families(DOCSET_ROOT, [family])
            ))
            last_family = family
            if bad_family:
                bad_family = False

        if bad_family:
            continue

        url_result = vache.get_url(doc_paths, name)
        try:
            url_result['ok']
        except KeyError:
            url_result['error']
        except TypeError as e:
            bad_family = True
            bad_families.append((family, e))

    print bad_families


def profile(expr, path):
    cProfile.run(expr, path)
    pstats.Stats(path).strip_dirs().sort_stats('cumulative').print_stats(15)


def main():
    profile('all_names()', 'all_names.prof')
    profile('family_names()', 'family_names.prof')
    profile('all_urls()', 'all_urls.prof')

if __name__ == '__main__':
    main()
