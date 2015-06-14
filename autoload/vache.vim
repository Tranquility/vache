if !has('python')
    echoerr 'vache: no python support found'
    finish
endif

python <<EOF
import vim
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

let s:python = 'python2'
if !executable(s:python)
    let s:python_version_out = system('python --version')
    let s:python_version = matchstr(s:python_version_out, 'Python 2\.')
    if empty(s:python_version)
        echoerr 'vache: could not find python 2'
        finish
    endif
    let s:python = 'python'
endif
let s:docset_script = expand('<sfile>:p:h') . '/vache/get_docsets.py'
let s:get_docsets_cmd = join([ s:python, s:docset_script ])

function! vache#lookup(...)
    let l:filetype_options = extend(s:filetype_options, g:vache_filetype_options)

    let l:get_docsets_cmd = join([ s:get_docsets_cmd, g:vache_default_docset_dir ])
    let l:docset_root = g:vache_default_docset_dir
    if has_key(l:filetype_options, &ft)
        let l:options = filetype_options[&ft]
        if type(l:options) == 3
            let l:families = join(l:options, ',')
            let l:args = ['--families', l:families, g:vache_default_docset_dir]
            let l:get_docsets_cmd = join([ s:get_docsets_cmd ] + l:args)

        elseif type(l:options) == 4
            let l:docset_root = l:options.dir
            let l:get_docsets_cmd = join([ s:get_docsets_cmd, l:options.dir ])

        else
            echoerr 'vache: bad vache_filetype_options value for filetype: ' . &ft
        endif
    endif

    let l:fzf_options = ''
    if a:0 == 1
        let l:fzf_options = l:fzf_options . ' --query="' . a:1 . '"'
    endif

    call fzf#run({
        \ 'source': l:get_docsets_cmd,
        \ 'sink': function('vache#browse#browse'),
        \ 'options': l:fzf_options,
        \ 'docset_root': l:docset_root,
        \ })
endfunction

function! vache#sift(...)
    if a:0 < 1
        let l:get_docsets_cmd = s:get_docsets_cmd
    else
        let l:families = join(a:000, ',')
        let l:get_docsets_cmd = join([ s:get_docsets_cmd, '--families', l:families ])
    endif
    echo 'cmd: ' . l:get_docsets_cmd

    call fzf#run({
        \ 'source': join([ l:get_docsets_cmd, g:vache_default_docset_dir ]),
        \ 'sink': function('vache#browse#browse'),
        \ 'docset_root': g:vache_default_docset_dir,
        \ })
endfunction
