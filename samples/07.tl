(* INFO **
** INFO *)

(* Use built-in packages *)
[use {io}
     {sys}
     {logic}
     {string}]


(*----------------------------------------------------------------------------*)
(* Dynamic variable name binding *)
($var {&prefix} {&})
($var {&type}   {uint64})
($var {&suffix} {_t})
($var (join (&prefix) (&type) (&suffix)) {12})

($print {prefix:}   (&prefix))
($print {type:}     (&type))
($print {suffix:}   (&suffix))
($print {uint64_t:} (&uint64_t))



(*----------------------------------------------------------------------------*)
(* Dynamic mixin variable names binding *)
(&suffix {!})
($mixin [name (join {mixin} (&suffix))]
    ($print {hello there `mixin!`}))
(mixin!)



(*----------------------------------------------------------------------------*)
($print (format [% {first: %0 = '%1', third: %4 = '%5', second: %2 = '%3'}]
            (to-string (&prefix)) (&prefix)
            (to-string (&type))   (&type)
            (to-string (&suffix)) (&suffix)))



(*----------------------------------------------------------------------------*)
($print {templang <<}
        (shell [redirect] {python -c "print('hello world!')"}))



(* ($var {&i} (int {12}))
($print (&i)) *)

(* ($for {i} ($range (int {12}))
    ($print ($to-string ($get {i})))) *)
