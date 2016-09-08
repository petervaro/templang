(* CORNER CASES *)

(* Escape sequences *)
({\{every\\where\}} {\\\0\t})

(* Space before names *)
(
    a (* !!! *)
)
[
    a (* !!! *)
]

(* Element syntax inside attribute and literal *)
[()]
{()}

(* Literal syntax inside attribute *)
[{}]

(* Element and attribute syntax inside literal *)
{()}
{[]}

(* Comment syntax inside element, attribute and literal *)
((**))
[(**)]
{(**)}

((*
    *))
[(*
    *)]
{(*
    *)}

(a(**)) ((**)a)
[a(**)] (* !!! *) [(**)a]
{a(**)}

(a(*
    *))
[a(*
    *)] (* !!! *)
{a(*
    *)}

(a (**)) ((**) a)
[a (**)] [(**) a]
{a (**)}

(a (*
    *))
[a (*
    *)]
{a (*
    *)}

((* a *))
[(* a *)]
{(* a *)}

((*
    a *))
[(*
    a *)]
{(*
    a *)}

[a {b}(**)]
[a {b}(*
      *)]
[a {b} (**)]
[a {b} (*
        *)]
[a {b}(* *)]
[a {b} (* *)]

(*  *)
(name[])
([attribute])
