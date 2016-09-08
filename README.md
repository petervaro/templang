templang
========

Universal templating language and framework with a LISP flavoured syntax.


Rationale
---------

There are plenty of templating languages out there: `haml`, `slim` or `jade`
just to name a few. However non of them has a clear, consistent syntax, nor can
be extended to do any kind of templating other than what they are designed for.
I wanted to create an extremely flexible language, which is very easy to learn,
to use and to customise.



Features
--------

- Nested comments support
- Full unicode character support (names can contain almost all characters)
- Highly customisable and extensible



Formal grammar of `templang`
----------------------------

    comment         : '(*' [ANYTHING | comment] '*)'
    element         : '(' [comment] [ELEMENT_NAME] [element_child]* ')'
    element_child   : comment | element | attribute | literal
    attribute       : '[' [comment] [ATTRIBUTE_NAME] [attribute_child]* ']'
    attribute_child : comment | literal
    literal         : '{' [LITERAL] '}'



Valid characters
----------------

    ANYTHING       : All characters
    ELEMENT_NAME   : ANYTHING, except '(', ')', '[', ']', '{', '}'
    ATTRIBUTE_NAME : ANYTHING, except '[', ']', '{', '}'
    LITERAL        : ANYTHING + '\{' + '\}' + '\\', except '{', '}'



Naming conventions
------------------

In general all names are using snake casing, but not with underscore (`_`), but
with hyphen (`-`).

    '$' + ELEMENT_NAME   : element with side effect(s)
    '$' + ATTRIBUTE_NAME : internal attribute
    UPPERCASE_NAME       : constant



References
----------

    () : empty element OR group
    [] : empty attribute
    {} : empty literal



License
-------

Copyright &copy; 2015-2016 **Peter Varo**

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program, most likely a file in the root directory, called 'LICENSE'.
If not, see <http://www.gnu.org/licenses>.
