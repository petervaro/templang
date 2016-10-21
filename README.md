[![[license: GPLv3]][1]][2]
[![[python: 3.5.2]][3]][4]

- - -

![templang][5]

- [Abstract](#abstract)
- [Rationale](#rationale)
- [Features](#features)
- [Formal grammar of templang](#formal-grammar-of-templang)
- [Valid characters](#valid-characters)
- [Naming conventions](#naming-conventions)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Packages](#packages)
- [Built-in package: `io`](#built-in-package-io)
- [Built-in package: `file`](#built-in-package-file)
- [Built-in package: `logic`](#built-in-package-logic)
- [Built-in package: `string`](#built-in-package-string)
- [Built-in package: `html5`](#built-in-package-html5)
- [Built-in package: `html`](#built-in-package-html)
- [License](#license)



Abstract
--------

Templang is a universal templating language and framework with a LISP flavoured
syntax. As its formal grammar shows, it is a very simple, yet a very powerful
one, not to mention its flexible and dynamic implementation (the framework),
which can be easily customised or extended to do any kind of *source-to-source*
compilation -- or even make templang a full blown programming language on its
own.



Rationale
---------

There are plenty of templating languages out there: `haml`, `slim` or `jade`
just to name a few. However non of them has a clear, consistent syntax, nor can
be extended to do any kind of templating other than what they are designed for.
I wanted to create an extremely flexible language, which is very easy to learn,
to use and to customise. Templang is designed to fulfill my specific needs,
however, it is suitable to serve others, and their own requirements.



Features
--------

- Nested comments support
- Full unicode character support (names can contain almost all characters)
- Highly customisable and easily extensible implementation
- built-in packages like: IO, file, logic, string, html, etc. support
- Powerful error reporting and debugging



Formal grammar of templang
--------------------------

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
    '&' + ELEMENT_NAME   : runtime defined variable (eg. argument)
    ELEMENT_NAME + '!'   : runtime defined element (eg. mixin)
    UPPERCASE_NAME       : constant



Usage
-----

    $ templang input.tl

    -u, --usepath <path>        Additional package path
    -o, --output <file>         Output name
    -d, --directory <path>      Output directory
    -w, --watch                 Watch for changes
    -p, --print                 Print instead of writing to file
    -v, --version               Version of templang
    -h, --help                  Print this text
    -*, --*                     Anything else will be passed to packages
                                (Eg. -D, --define is used by the logic package)



Dependencies
------------

Only packages have dependencies:

- `html`
    - [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup)
    - [Markdown](http://pythonhosted.org/Markdown)
    - [HTML5Lib](https://github.com/html5lib/html5lib-python)



Packages
--------

Templang's features can be extended via packages. To use a package, use the
`[use {<PACKAGE>}]` attribute expression at the top level of the document.

Packages are implemented in python, and are capable of altering almost anything
about the language! reusable code can be created inside templang as well with
the buil-int `file` package, though that won't change how the language is
working.



Built-in package: `io`
---------------------

- `$print`
- `$write`



Built-in package: `file`
------------------------

- `$import`
- `$export`
- `include`



Built-in package: `logic`
-------------------------

- `$define`
- `$undefine`
- `$expose`
- `$var`
- `$mixin`



Built-in package: `string`
--------------------------

- `join`
- `format`
- `to-string`



Built-in package: `html5`
------------------------

- all valid HTML5 tags + `!--`
- `markdown`



Built-in package: `html`
------------------------

> This package uses `html5` package under the hood, that is, anything available
> in `html5` is available in this package as well, therefore `use`ing `html5`
> along with this package is not necessary. It is highly recommended though to
> use the stricter `html5` package, since this one acts as a wild-card, meaning
> mistyped element names can lead to curious results, and silent errors!

- Any unregistered element will be treated as an html tag



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

<!-- -->

[1]: https://img.shields.io/badge/license-GNU_General_Public_License_v3.0-blue.svg
[2]: http://www.gnu.org/licenses/gpl.html
[3]: https://img.shields.io/badge/python-3.5.2-lightgrey.svg
[4]: https://docs.python.org/3
[5]: img/logo.png?raw=true "(temp[lang])"
