(* INFO **
** INFO *)

[use {io}
     {logic}
     {string}]

($print {first line}
        {second line}
        {third line}
        {fourth line} [sep {\n}])

($print {first line}
        {second line}
        {third line}
        {fourth line} [sep {; }]
                      [end {\n\n}])

($print (to-string (alpha (beta (gamma [delta {epsilon}])))))

($print (to-string [path {../file}]))

($print {attribute =>} (to-string [my-attribute])
        {\nelement =>} (to-string (my-element)))

($write {writing to the document!})

($var {&first}  {alpha})
($var {&second} {beta})
($var {&third}  {gamma})

($print {-----})
($print (format [% {first = %0;\nthird = %2;\nsecond = %1;}]
                (&first) (&second) (&third)))

($print {-----})
($print (format [% {first = %?;\nsecond = %?;\nthird = %?;}]
                (&first) (&second) (&third)))
