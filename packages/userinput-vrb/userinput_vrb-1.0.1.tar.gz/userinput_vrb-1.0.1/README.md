# userinput_vrb

Helper functions for console user input.

This module defines:

```function input_with_default()```
  
Read string from stdin. If empty, return dflt.

```function getpass_not_empty()```

Read password from stdin, don't allow empty password.()

```function choose_from()```

Read character from stdin. The user must input one of
the characters passed in choices. A default may be given.