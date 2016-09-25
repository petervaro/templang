[use {io}
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
