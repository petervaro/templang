(* Because the top level is just another element (root) it can handle the
   attributes and literals. In this case, the only built-in attribute, the
   `use` will load the `std` and the `html` packages *)
[use {std}]
[use {html}]

(doctype [html])
(html [lang {en}]
    (head
        (meta [charset {utf-8}]))
    (body
        ($markdown [path {sample.md}])
        (div [id {first-div}]
             [class {this-class}
                    {that-class}]
            {lorem ipsum dolor
             sit amet et cetera}
             (* The order of literals and children matters, however the order of
                the attributes does not. Though the convention is to write them
                as close to the `keyword` as possible *)
             (span [class {lang-keyword}]
                {-- oh, yeah!}))
        (pre
            {lorem ipsum dolor
             sit amet et cetera})
        (div [class {that-class}]
             [$literal-join {\n}]
            {one line here}
            {another one here}
            {and the last one here})))


(* The `std` package has basic logic and IO keywords, so it can handle loops,
   conditionals, and can print to console, or write this document *)
($for {i} ($range ($int {10}))
    ($write [$literal-raw] {index = })
    ($write ($to-string ($get {i}))(NEW-LINE)))

(* Empty parenthesis are valid elements too. The `std` package actually uses
   them as groups, here for example, if the `ifdef` does not succeed, it will
   tell this to its parent, which will search for an `elif` or an `else` branch
   in its children nodes *)
(($ifdef [DEVEL]
    ($write {Development build!\n}))
 ($else
    ($write {Release build!\n})))

(* The `std` package also contains a `shell` command to interact directly with
   the environment, which can of course run arbitrary scripts. The output of
   the script can be redirected to this document *)
($shell [$redirect-output]
        [python {script.py}])
