(* INFO **
** INFO *)

[use {io}]
[use {file}]
[use {logic}]

($define {P1} {sweet})

($write {hello} [end { }])
($import [path {../samples/08b.tl}])
($write ($include [path {../samples/08b.tl}]))

($print ($expose {P2}))
