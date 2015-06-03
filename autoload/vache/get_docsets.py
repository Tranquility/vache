import vache
import sys
import string
import os


def usage():
    print 'usage: get_docsets [ --log ] [ --families <families> ] <docset_dir>'
    sys.exit(1)


def main():
    args = sys.argv[1:]

    if len(args) < 1:
        usage()

    docsets = None
    docset_root = args[-1]
    if not os.path.isdir(docset_root):
        if docset_root == '--families':
            print 'error: flag --families present without <families> argument'
        elif len(args) > 2:
            print "error: '{}' is not a directory".format(docset_root)
        else:
            print 'error: missing <docset_dir> argument'
        usage()

    if len(args) == 1:
        docsets = vache.get_plist_files(docset_root)

    elif len(args) == 3 and args[0] == '--families':
        families = string.split(args[1], ',')

        docsets = \
            vache.get_plist_files_for_families(docset_root, families)
    else:
        usage()

    for encoded in vache.get_names(docsets):
        print encoded


if __name__ == '__main__':
    main()
