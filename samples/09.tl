(* INFO **
** INFO *)

(* Use built-in packages *)
[use {io}
     {file}
     {html}]

(* Markdown from external file *)
(markdown (include [path {../samples/09.md}]))

(* Markdown from literal *)
($print (markdown [$return]
{
Hello
=====

*world!*

How exactly
-----------

"**are** you, on this `beautiful` morning?"

-- What?!
}))
