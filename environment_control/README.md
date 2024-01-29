# envc, custom environment control variables manager

envc, manages environment control variables.

**DISCLAMER**: This tool is still in a proof-of-concept (POC) stage. The code is
dirty and convoluted.

## Environment Control Variables

Environment control variables are boolean variables that are set in order to
contextualize intsallation or scripts.

i.e.
```console
VIRTUALENV_IS_INSTALLED=true
JAVA_IS_INSTALLED=true

# ...
if JAVA_IS_INSTALLED; then
# ...
fi
```
## Usage

```console
Usage: envc [action] [opts] [arguments]

     List of supported actions:
     version : Displays version of the tool

     append : Appends an environment control variable to the current table
         <control_variable> : Control variable to add to the environment control table
             <initial_value> : Initial value of the environment control variable

     show : Shows current control variable table

     remove : Remove a control variable from the table
         <control_variable> : Control variable to remove
             force : Forces deletion (deletes permanently)

     restore : Restores a control variable from the table
         <control_variable> : Control variable to restore

     update : Updates the value of a control environment from the table
         <control_variable> : Control varuable to update
             <value> : Value for update

     create : Creates the envc control table
         <path> : Path value where it should be created, by default:/tmp
```

## TODO

- [ ] Code cleanup.
- [ ] Refactor.
- [ ] Better configurability.

## Known problems or Limitations

* When appending a new variable it adds a new line for each variable. This
will still work as the program is designed to only target specific string streams,
but creates an extra line while executing the `show` command.

* The tool only works for setting boolean values, `true` or `false`.

