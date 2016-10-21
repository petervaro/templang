(* INFO **
** INFO **)

($macro [name {#macro}]
        [* {&expressions}]
    ($var {&msg})
    ($for [in ($var {&expression}) (&expressions)]
        (switch [expr (typeof (&expression))]
            [case {Element}
                (&msg {We have an element:})]
            [case {Attribute}
                (&msg {We have an attribute:})]
            [case {Literal}
                (&msg {We have a literal:})])
        ($print (&msg) (to-string (&expression)))))

(#macro (p))
