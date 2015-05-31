if !exists('g:vache_default_docset_dir')
    if has('unix')
        let s:uname = system("uname -s")
        if s:uname == "Darwin\n"
            let g:vache_default_docset_dir = $HOME . '/Library/Application Support/Dash/DocSets'
        else
            let g:vache_default_docset_dir = $HOME . '/.local/share/Zeal/Zeal/docsets'
        endif
    elseif has('win32')
        let g:vache_default_docset_dir = $APPDATA . '/Local/Zeal/Zeal/docsets'
    else
        echoerr 'vache: problem: could not detect operating system'
        echoerr 'vache: solution: set g:vache_default_docset_dir manually'
    endif
endif

if !exists('g:vache_filetype_options')
    let g:vache_filetype_options = {}
endif

if !exists('g:vache_browser')
    if has('unix')
        let g:vache_browser = $BROWSER
    else
        echoerr 'vache: problem: could not detect default browser'
        echoerr 'vache: solution: set g:vache_browser'
    endif
endif

command! -nargs=? VacheLookup call vache#lookup(<f-args>)
command! -nargs=* VacheSift call vache#sift(<f-args>)
