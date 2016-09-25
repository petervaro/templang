(* INFO **
** INFO *)

(* Use built-in packages *)
[use {io}
     {logic}]


(*----------------------------------------------------------------------------*)
($var {&var} {hello world})
($print {&var =} (&var))

(&var {12})
($print {&var =} (&var))


(*----------------------------------------------------------------------------*)
($mixin [name {printer!}]
    ($print {I am printing!\n}))

(printer!)


(*----------------------------------------------------------------------------*)
($mixin [name {printer!}]
        [args {&x} {&y}]
    ($print (&x) (&y)))

(printer! {hello} {world!})
(printer! {hello} [&y {world!}])
(printer! [&y {world!}] {hello})
(printer! [&x {hello}]
          [&y {world!}])



(*----------------------------------------------------------------------------*)
($mixin [name {printer!}]
        [args {&x} {&y}]
        [xarg {&sep} {, }]
    ($print (&x) (&sep) (&y) [sep {}]))

(printer! {hello} {world!})
(printer! {hello} [&sep { -> }] {world!})


(*
    ($define {VAR})
    (($if ($defined {VAR})
        ($print {`VAR` is defined}))
     ($else
        ($print {`VAR` is not defined})))

    ($undefine {VAR})
    (($if ($defined {VAR})
        ($print {`VAR` is defined}))
     ($else
        ($print {`VAR` is not defined})))
*)

(*
    (?  [if ()]
        [else ()])
    (? () ())

    (switch [case ()]
            [case ()]
            [default ()])
 *)
