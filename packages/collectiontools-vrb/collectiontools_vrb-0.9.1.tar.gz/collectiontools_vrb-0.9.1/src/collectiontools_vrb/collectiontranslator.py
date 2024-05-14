import re
from typing import Any as Any

# [ ] Check implementation of translate_str()

class CollectionTranslator:
    """ Search strings, lists or dicts for placeholders using 
    a regular expression provided by the user. Replace the 
    matches with a value provided by a translator function, 
    which is as well provided by the user.
    For dicts and lists, the search is recursive.
    See constructor / functions for details.
    """

    def __init__(self, translator_func = None, regexp: str = r"(?<!\\){[^{}]*}"):
        """ Construct new CollectionTranslator object with default regular expression.

        Args:
            translator_func (_type_, optional): function to be called to
                translate a placeholder to its value. Defaults to None.
            regexp (str, optional): regular expression for finding
                placeholders. Defaults to r"(?<!\){[^{}]*}". That means
                that placeholders are marked by surrounding curly brackets,
                e.g. {KEY}.
        
        default regexp: a curly left bracket NOT preceded by a backslash starts
        a placeholder. It's name is denoted by the following sequence of characters
        NOT containing { or }. The end of the placeholder is a curly right bracket.

        translator_func and regexp may be changed later by assigning new
        values to self.translator_func and self.regexp
        """
        self.regexp = regexp;
        self.translator_func = translator_func;

    def translate(self, val: Any) -> Any:
        """ Convenience function which calls translate_dict, 
        translate_list or translate_str, depending on the type of val.
        For details: see these functions.

        Args:
            val (_Any_): value to be translated

        Returns:
            any: return value of the above functions
        """
        if isinstance(val, dict):
            # recursivley go down to nested dict
            val = self.translate_dict(val)
        elif isinstance(val, list):
            # recursivley go down to nested list
            val = self.translate_list(val)
        elif isinstance(val, str):
            # replace placeholders, if possible
            val = self.translate_str(val)
        #else: don't change
        return val
    
    # verwende eventuell str.format() für translate_str
    """
    { "schlüssel" : ["format string mit platzhaltern {0} und {1}", "key0", "key1"], ... }
    ->
    { "schlüssel" : "format string mit platzhaltern val0 und val1", ... }
    oder
    { "schlüssel" : { use_placeholders: true, 
                      format_string: "format string mit platzhaltern {0} und {1}",
                      keys: [ "key0", "key1" ]
                    }, ... }
    ->
    { "schlüssel" : "format string mit platzhaltern val0 und val1", ... }
    """
    def translate_str(self, s: str) -> str:
        r""" Search s for placeholders using self.regexp and
        replace them with a value provided by self.translator_func.
        Example: "{KEY}" -> "REPLACEMENT", if translator_func returns
        "REPLACEMENT" when calling translator_func("KEY").

        To insert a literal "{" or "}" into the string
        which is not to be treated as a bracket surrounding
        a placeholder, use "double-backslash-{" (or }) instead.
        To insert a literal backslash, use "double-backslash-/".
        Backslashes within placeholders are not allowed.

        Example when reading documentation:
        "val: \\\\{{KEY}\\\\} \\\\/x /y" results in
        "{REPLACEMENT} \\x /y"

        Same Example when reading source code:
        "val: \\{{KEY}\\} \\/x /y" results in
        "{REPLACEMENT} ", followed by backslash-x, "/y"

        Args:
            s (str): String with placeholders in curly brackets
            func (_type_): function to get replacement for placeholder

        Returns:
            str: String with replacements. s itself remains unchanged,
                 since strings are immutable.
        """
        if self.translator_func:
            # find and replace placeholders:
            mo = re.findall(self.regexp, s)
            for m in mo:
                val = self.translator_func(m[1:-1])
                s = re.sub(m, val, s, 1)
        # replace \\{, \\}, \\/ by {, }, \
        s = re.sub(r"\\{", "{", s)
        s = re.sub(r"\\}", "}", s)
        s = re.sub(r"\\/", r"\\", s)
        return s
    
    def translate_list(self, l: list) -> list:
        """ Translate all entries in the given list. Depending on the 
        type of the entry, self.translate_str, self.translate_list 
        or self.translate_dict is called.
        This combination of functions works recursively.
        
        The list items themselves are replaced by the translated versions.

        Args:
            l (list): List with items to be translated

        Returns:
            list: The (now changed) list itself.
        """
        # process all list items
        for i in range(len(l)):
            val = l[i]
            if isinstance(val, dict):
                # recursivley go down to nested dict
                self.translate_dict(l[i])
            elif isinstance(val, list):
                # recursivley go down to nested list
                self.translate_list(l[i])
            elif isinstance(val, str):
                # replace placeholders, if possible
                l[i] = self.translate_str(val)
            #else: ignore entry
        return l

    def translate_dict(self, d: dict) -> dict:
        """ Translate all values in the given dict. Depending on the 
        type of the value, self.translate_str, self.translate_list 
        or self.translate_dict is called. The keys are left unchanged.
        This combination of functions works recursively.
        
        The dict values themselves are replaced by the translated versions.

        Args:
            d (dict): dict with items to be translated

        Returns:
            list: The (now changed) dict itself.
        """
        # process whole dict
        for key in d:
            val = d[key]
            if isinstance(val, dict):
                # recursivley go down to nested dict
                self.translate_dict(val)
            elif isinstance(val, list):
                # recursivley go down to nested list
                self.translate_list(val)
            elif isinstance(val, str):
                # replace placeholders, if possible
                d[key] = self.translate_str(val)
            #else: ignore entry
        return d
