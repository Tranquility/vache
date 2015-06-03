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


def family_names():
    plists = vache.get_plist_files_for_families(DOCSET_ROOT, ['go'])
    for _ in vache.get_names(plists):
        pass


def all_names():
    plists = vache.get_plist_files(DOCSET_ROOT)
    for _ in vache.get_names(plists):
        pass


def profile(expr, path):
    cProfile.run(expr, path)
    pstats.Stats(path).strip_dirs().sort_stats('cumulative').print_stats(15)


def main():
    profile('all_names()', 'all_names.prof')
    profile('family_names()', 'family_names.prof')

if __name__ == '__main__':
    main()
