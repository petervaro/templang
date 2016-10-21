(* INFO **
** INFO **)

[use {logic}
     {types}
     {string}
     {html5}]

[use {io}
     {__debug}]

(!doctype [html])
(html [lang {en}]
    (!-- {this is the head of the document})
    (head
        (meta [charset {utf-8}])
        (title {Title}))
    (!-- {this is the body of the document})
    (body
        (p [class {beautiful-text}]
            {Some content})
        ($each [in {&i} (range [to {10}])]
            (p [class (join {class-} (&i))]
                (join {This is index:} (&i))))))
