import vache
import sys
import json
import base64

def get_filetype_docsets(docset_root, options):
    if isinstance(options, dict):
        return vache.get_plist_files_with_path(options['dir'])

    elif isinstance(options, list):
        return vache.get_plist_files_for_platform_families(options, docset_root)
    else:
        print 'echoerr "vache: vache_filetype_option[&ft]: must be either a list or dict"'
        sys.exit(1)


def get_family_docsets(docset_root, families):
    return vache.get_plist_files_for_platform_families(families, docset_root)


def usage():
    print 'get_docsets [ --families <families> | --filetype <filetype> ] <docset_dir>'
    sys.exit(1)


def main():
    args = sys.argv[1:]

    second_arg_map = {
        '--families': get_family_docsets,
        '--filetype': get_filetype_docsets
    }
    docsets = None
    if len(args) == 1:
        docsets = vache.get_plist_files_with_path(args[0])
    elif len(args) == 3:
        try:
            parsed_arg = json.loads(base64.b64decode(args[1]))
            docsets = second_arg_map[args[0]](args[2], parsed_arg)
        except KeyError:
            usage()
    else:
        usage()

    for encoded in vache.get_encoded_names(docsets):
        print encoded.encode('utf-8')


if __name__ == '__main__':
    main()
