(* INFO **
** INFO *)

[use {file}
     {html5}]

($import [path {../samples/11b.tl}])

(html5!
    [&title {External mixin}]
    [&body
        (p [$return] {First page generated with external mixin})])
