"""
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
"""

from getpass import getpass

def input_with_default(msg: str, dflt: str) -> str:
    """read string from stdin. If empty, return dflt.

    Args:
        msg (str): prompt for input
        dflt (str): default value (if user enters empty string)

    Returns:
        str: string read from stdin or dflt, if empty.
    """
    return input(f"{msg} [{dflt}]: ").strip() or dflt

def getpass_not_empty(msg: str) -> str:
    """read password from stdin, don't allow empty password.

    Args:
        msg (str): prompt for input

    Returns:
        str: password read from stdin
    """
    passwd = ""
    while not passwd:
        passwd = getpass(msg)
    return passwd
    
def choose_from(msg: str = "", choices: str = "yn", 
                end: str = ":", dflt: str = "") -> str:
    """read character from stdin. The user must input one of
    the characters passed in choices (all characters will be
    converted to lowercase). If dflt is given (and if dftl 
    is in choices), the corresponding letter will be displayed
    in uppercase and entering an empty string will result in
    returning the dflt character.
    The input prompt is: msg+choices+end, where choices will
    be displayed with slashes between the allowed characters,
    e.g. "Do you want to continue "+"y/N" + "? "

    Args:
        msg (str, optional): prompt for input. Defaults to "".
        choices (str, optional): allowed chars for input. Defaults to "yn".
        end (_type_, optional): part of prompt behind choices. Defaults to ":".
        dflt (str, optional): default choice if just Enter is pressed. Defaults to "".

    Returns:
        str: character read from stdin
    """
    # make all choices lowercase
    choices = choices.lower()

    # construct message prompt
    prompt = ""
    # insert slash between possible answers ("yn" -> "y/n")
    for pos in range(len(choices)-1):
        prompt += choices[pos] + "/"
    prompt += choices[-1]
    # make default choice uppercase (-> e.g. "y/N")
    if dflt:
        pos = prompt.find(dflt.lower())
        if pos >= 0:
            prompt = prompt[:pos] + prompt[pos].upper() + prompt[pos+1:]
    # start prompt with given msg text and append given end
    prompt = msg + prompt + end

    result = ""
    while not result:
        result = input(prompt).lower()
        # If default is given, empty answer means default value
        if dflt and (result == ""):
            result = dflt.lower()
        # otherwise answer must be one of the given choices
        elif not result or (result not in choices):
            result = ""
    # return character is always lowercase
    return result

