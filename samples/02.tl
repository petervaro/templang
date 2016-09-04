(* CORNER CASES *)

(* Escape sequences *)
(special [\[characters\]] {\{every\\where\}} {\\\0\t})
(
    a (* !!! *)
)

(* {{} *)

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
    *)] (* !!! *)
{(*
    *)}

(a(**))
[a(**)] (* !!! *)
{a(**)}

(a(*
    *))
[a(*
    *)] (* !!! *)
{a(*
    *)}

(a (**))
[a (**)]
{a (**)}

(a (*
    *))
[a (*
    *)] (* !!! *)
{a (*
    *)}

((* a *))
[(* a *)] (* !!! *)
{(* a *)}

((*
    a *))
[(*
    a *)] (* !!! *)
{(*
    a *)}

[a b(**)] (* !!! *)
[a b(*
    *)] (* !!! *)
[a b (**)] (* !!! *)
[a b (*
    *)] (* !!! *)
[a b(* *)] (* !!! *)
[a b (* *)] (* !!! *)

(*  *)
(name[])
([attribute])
