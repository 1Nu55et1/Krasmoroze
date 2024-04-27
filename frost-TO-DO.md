Additions
---------

More of the jQuery API: nextUntil?

Optimizations
-------------

The html5lib tree builder doesn't use the standard tree-building API,
which worries me and has resulted in a number of bugs.

markup_attr_map can be optimized since it's always a map now.

Upon encountering UTF-16LE data or some other uncommon serialization
of Unicode, UnicodeDammit will convert the data to Unicode, then
encode it at UTF-8. This is wasteful because it will just get decoded
back to Unicode.
