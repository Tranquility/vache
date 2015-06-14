python import vache
python import vim

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

function! vache#browse#browse(line) dict
    let l:uri = pyeval('vache.construct_url(vim.eval("self.docset_root"), unicode(vim.eval("a:line").strip()))')
    let l:browser_out = system(s:browse_cmd(l:uri))
    if v:shell_error != 0
        echoerr 'vache: browser err: ' . l:browser_out
    endif
endfunction
