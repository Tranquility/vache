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

function! s:quote(string)
    return '"' . a:string . '"'
endfunction

function! s:osx_browse_cmd(uri)
    return join([
        \ "osascript -e 'tell application",
        \ s:quote(g:vache_browser),
        \ 'to open location',
        \ s:quote(a:uri) . "'"
        \ ])
endfunction

function! s:default_browse_cmd(uri)
    return join([ g:vache_browser, s:quote(a:uri) ])
endfunction

let s:browse_cmd = function('s:default_browse_cmd')
if has('unix')
    let s:uname = system('uname -s')
    if s:uname == "Darwin\n"
        let s:browse_cmd = function('s:osx_browse_cmd')
    endif
endif

function! s:browse(line)
    let l:uri = pyeval('vache.decode_url(unicode(vim.eval("a:line").strip()))')

    let l:browse_cmd = s:browse_cmd(l:uri)
    let l:browser_out = system(l:browse_cmd)
    if v:shell_error != 0
        echoerr 'vache: browser err: ' . l:browser_out
    endif
endfunction

let s:get_docsets_cmd = 'python2 ' . expand('<sfile>:p:h') . '/vache/get_docsets.py'

function! vache#lookup(...)
    let l:filetype_options = extend(s:filetype_options, g:vache_filetype_options)

    let l:get_docsets_cmd = join([ s:get_docsets_cmd, g:vache_default_docset_dir ])
    if has_key(l:filetype_options, &ft)
        let l:options = filetype_options[&ft]
        if type(l:options) == 3
            let l:families = join(l:options, ',')
            let l:args = ['--families', l:families, g:vache_default_docset_dir]
            let l:get_docsets_cmd = join([ s:get_docsets_cmd ] + l:args)

        elseif type(l:options) == 4
            let l:get_docsets_cmd = join([ s:get_docsets_cmd, l:options.dir ])

        else
            echoerr 'vache: bad vache_filetype_options value for filetype: ' . &ft
        endif
    endif

    let l:fzf_options = '--with-nth=2,3 --delimiter="\t"'
    if a:0 == 1
        let l:fzf_options = l:fzf_options . ' --query=' . s:quote(a:1)
    endif

    call fzf#run({
        \ 'source': l:get_docsets_cmd,
        \ 'sink': function('s:browse'),
        \ 'options': l:fzf_options
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
        \ 'sink': function('s:browse'),
        \ 'options': '--with-nth=2,3 --delimiter="\t"',
        \ })
endfunction
