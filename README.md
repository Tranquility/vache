Vache - graze on docs from vim
==============================================================

vache provides fuzzy documentation browsing / lookup for ([Dash][1] / [Zeal][2])
documentation sets, all from the comfort of (neo)vim


requirements
------------

* has('python')
* [fzf][3]
* a web-browser


use
---

* `:VacheSift` - sift through all documentation targets available

* `:VacheSift <docset-family> ...` - sift through all documentation for any
  of `<docset-family>`

* `:VacheLookup` - lookup only documentation targets appropriate to the
  current filetype

* `:VacheLookup <query>` - begin lookup with `<query>` as an initial --query
  parameter to fzf


configuration
-------------

vache follows convention over configuration and should be usable out of the
box for 90% of use cases. for the remaining 10%, global variables exist

* `g:vache_default_docset_dir` - the default directory under which docsets are
  stored. `VacheSift` always looks for documentation here, as does
  `VacheLookup` unless the current filetype is configured to use its own
  directory (see `g:vache_filetype_options`)

  _example_

      let g:vache_default_docset_dir = $HOME . '/docsets'

* `g:vache_filetype_options` - a dictionary where keys are filetypes and values
  are one of:
  - a list of docset families to associate with that filetype. `VacheLookup`
    only searches through documentation sets which belong to one of these
    families

  - a dictionary with the following associations
    - `'dir'` - an absolute directory path where docsets for the associated
      filetype are to be found. `VacheLookup` only searches through
      documentation sets which are found under this directory

  this value will be merged with the default filetype options dictionary each
  time `VacheLookup` or `VacheSift` are called, so feel free to dynamically
  update it

  _example_

      let g:vache_filetype_options = {
          \ 'haskell': { 'dir': $HOME . '/haskell_docsets' },
          \ 'javascript': [ 'javascript', 'jquery', 'jqueryui' ]
          \ }

* `g:vache_browser` - the name of a web browser executable to be used for
  opening documentation. defaults to `$BROWSER` on `has('unix')` systems

  _example_

      let g:vache_browser = 'chromium-browser'


supported docset families
-------------------------

all docsets should be assumed to work unless they are found in the list for
issue [#9][4]

the following is a list of associations from filetype to a list of docset
families enabledwhat has already been tested and added to the default families
enabled for each filetype. please submit issues / pull requests to add more
associations to this list


* haskell -> haskell
* go -> go
* js -> javascript, lodash, d3, moment
* r -> r
* css -> css
* less -> css, less
* svg -> svg


contributing
------------

please see CONTRIBUTING.md in this same project


known bugs
----------

* some documentation sets use unsupported schemas for their sqlite database
* windows support is incomplete until we have an implementation of a replacement
  for the unix `find` command


[1]: https://kapeli.com
[2]: http://zealdocs.org
[3]: https://github.com/junegunn/fzf
[4]: https://github.com/dnhgff/vache/issues/9
