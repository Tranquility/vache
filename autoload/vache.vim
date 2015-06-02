if !has('python')
    echoerr 'vache: no python support found'
endif

python <<EOF
import vim
import base64
import json
import os
import sys
sys.path.append(
    os.path.join(vim.eval("expand('<sfile>:p:h')"), 'vache/')
)
import vache
EOF

let s:filetype_options = {
    \ 'haskell': [ 'haskell' ],
    \ 'go': [ 'go' ],
    \ 'js': [ 'lodash', 'd3', 'moment', 'javascript' ],
    \ 'r': [ 'r' ],
    \ 'css': [ 'css' ],
    \ 'less': [ 'css', 'less' ],
    \ 'svg': [ 'svg' ],
    \ }

function! s:browse(line)
    let l:uri = pyeval('vache.decode_url(unicode(vim.eval("a:line").strip()))')

    let l:ff_out = system(eval('g:vache_browser') . ' ' . eval('l:uri'))
    if v:shell_error != 0
        echoerr 'vache: browser err: '.l:ff_out
    endif
endfunction

let s:get_docsets_cmd = 'python ' . expand('<sfile>:p:h') . '/vache/get_docsets.py'

function! vache#lookup(...)
    let l:filetype_options = extend(s:filetype_options, g:vache_filetype_options)

    let l:get_docsets_cmd = join([s:get_docsets_cmd, g:vache_default_docset_dir])
    if has_key(l:filetype_options, &ft)
        let l:options = filetype_options[&ft]
        if type(l:options) == 3
            let l:families = join(l:options, ',')
            let l:args = ['--families', l:families, g:vache_default_docset_dir]
            let l:get_docsets_cmd = join([s:get_docsets_cmd] + l:args)

        elseif type(l:options) == 4
            let l:get_docsets_cmd = join([s:get_docsets_cmd, l:options.dir])

        else
            echoerr 'vache: bad vache_filetype_options value for filetype: ' . &ft
        endif
    endif

    if a:0 < 1
        let l:query = ''
    else
        let l:query = a:1
    endif

    call fzf#run({
        \ 'source': l:get_docsets_cmd,
        \ 'sink': function('s:browse'),
        \ 'options': '--with-nth=3 --delimiter=, --query="' . l:query . '"'
        \ })
endfunction

function! vache#sift(...)
    if a:0 < 1
        let l:get_docsets_cmd = s:get_docsets_cmd
    else
        let l:families = join(a:000, ',')
        let l:get_docsets_cmd = s:get_docsets_cmd . ' --families ' . l:families
    endif
    echo 'cmd: ' . l:get_docsets_cmd

    call fzf#run({
        \ 'source': l:get_docsets_cmd . ' ' . g:vache_default_docset_dir,
        \ 'sink': function('s:browse'),
        \ 'options': '--with-nth=3 --delimiter=,',
        \ })
endfunction
