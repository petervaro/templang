(* INFO **
** INFO *)

[use {file}
     {html5}
     {logic}]

($mixin [name {html5!}]
        [xarg {&title}]
        [xarg {&body}]
    (!doctype [html])
    (html [lang {en}]
        (head
            (meta [charset {utf-8}])
            (title (&title)))
        (body
            (&body))))

($export {html5!})
