(* INFO **
** INFO *)

[use {io}]
[use {file}]
[use {logic}]

($define {STRING1} {sweet})

($write {hello} [end { }])
($import [path {../samples/08b.tl}])
($print ($expose {STRING2}))

($write (include [path {../samples/08b.tl}]) [end {}])
