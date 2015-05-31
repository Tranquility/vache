import vache
import cProfile
import pstats
import os
import sys
import platform

DOCSET_ROOT = None
if platform.system() == 'Linux':
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


def all_names():
    results = vache.get_names(vache.get_plist_files_with_path(DOCSET_ROOT))
    for path, meta, names in results:
        yield list(names)


def family_names():
    plists = vache.get_plist_files_for_platform_families(['go'], DOCSET_ROOT)
    results = vache.get_names(plists)
    for path, meta, names in results:
        yield list(names)


def encoded_names():
    plists = vache.get_plist_files_with_path(DOCSET_ROOT)
    return vache.get_encoded_names(plists)


def profile(expr, path):
    cProfile.run(expr, path)
    pstats.Stats(path).strip_dirs().sort_stats('cumulative').print_stats(15)


def main():
    profile('list(all_names())', 'all_names.prof')
    profile('list(family_names())', 'family_names.prof')
    profile('list(encoded_names())', 'encoded_names.prof')

if __name__ == '__main__':
    main()
