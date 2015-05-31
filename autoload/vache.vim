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

    if has_key(l:filetype_options, &ft)
        let l:options = filetype_options[&ft]
        let l:encoded_options = pyeval('base64.b64encode(json.dumps(vim.eval("l:options")))')
        let l:get_docsets_cmd = s:get_docsets_cmd . ' --filetype ' . l:encoded_options
    else
        let l:get_docsets_cmd = s:get_docsets_cmd
    endif

    if a:0 < 1
        let l:query = ''
    else
        let l:query = a:1
    endif

    call fzf#run({
        \ 'source': l:get_docsets_cmd . ' ' . g:vache_default_docset_dir,
        \ 'sink': function('s:browse'),
        \ 'options': '--with-nth=3 --delimiter=, --query="' . l:query . '"'
        \ })
endfunction

function! vache#sift(...)
    if a:0 < 1
        let l:get_docsets_cmd = s:get_docsets_cmd
    else
        let l:families_encoded = pyeval('base64.b64encode(json.dumps(vim.eval("a:000")))')
        let l:get_docsets_cmd = s:get_docsets_cmd . ' --families ' . l:families_encoded
    endif

    call fzf#run({
        \ 'source': l:get_docsets_cmd . ' ' . g:vache_default_docset_dir,
        \ 'sink': function('s:browse'),
        \ 'options': '--with-nth=3 --delimiter=,',
        \ })
endfunction
