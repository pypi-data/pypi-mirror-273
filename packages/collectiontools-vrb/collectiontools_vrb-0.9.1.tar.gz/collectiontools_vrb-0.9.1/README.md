# collectiontools_vrb

Various tools to handle collection I/O and transformations.

  - On PyPI: https://pypi.org/project/collectiontools-vrb/
  - On GitHub: https://github.com/v-r-b/collectiontools_vrb 

## \_\_init__.py

```function update_dict_from_url()```

Read collection data from the given URL. 

```function update_dict_from_key_value_file()```

Read collection data from the given file. 

```function dict_contains_path()```

Tests if a given path is a valid key inside the given dict.

```function update_dict_from_json_file()```
  
Read collection data from config file. Check for mandatory keys.

## collectiontranslator.py

```class CollectionTranslator```

Search strings, lists or dicts for placeholders using a 
regular expression provided by the user. Replace the matches 
with a value provided by a translator function, which is 
as well provided by the user.