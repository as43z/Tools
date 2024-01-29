#!/usr/bin/env python3
if __name__ != "__main__":
    raise Exception("Error: envc.py is only an executable, not a library")

import os
import sys

__TAB_CHAR="  "
# Harcoded for simplicity
VERSION="v0.1.0"
# Hardcoded for simplicity
ENVC_TABLE_PATH=os.environ.get("ENVC_TABLE_PATH", "/tmp")
# Very big table! Maybe it´s not the best way for representing the action list
"""
ACTION := {
    name: str
    help: str 
    arguments: list[Action | str]
}
"""
__ACTIONS = [
    {
        "name": "version",
        "help": "Displays version of the tool",
        "arguments": [],
    },
    {
        "name": "append",
        "help": "Appends an environment control variable to the current table",
        "arguments": [
            {
                "name": "<control_variable>",
                "help": "Control variable to add to the environment control table",
                "arguments": [
                    {
                        "name": "<initial_value>",
                        "help": "Initial value of the environment control variable",
                        "arguments": [],
                    },
                ],
            },
        ],
    },
    {
        "name": "show",
        "help": "Shows current control variable table",
        "arguments": [],
    },
    {
        "name": "remove",
        "help": "Remove a control variable from the table",
        "arguments": [
            {
                "name": "<control_variable>",
                "help": "Control variable to remove",
                "arguments": [
                    {
                        "name": "force",
                        "help": "Forces deletion (deletes permanently)",
                        "arguments": [],
                    },
                ],
            },
        ],
    },
    {
        "name": "restore",
        "help": "Restores a control variable from the table",
        "arguments": [
            {
                "name": "<control_variable>",
                "help": "Control variable to restore",
                "arguments": [],
            },
        ],
    },
    {
        "name": "update",
        "help": "Updates the value of a control environment from the table",
        "arguments": [
            {
                "name": "<control_variable>",
                "help": "Control varuable to update",
                "arguments": [
                    {
                        "name": "<value>",
                        "help": "Value for update",
                        "arguments": [],
                    },
                ],
            },
        ],
    },
    {
        "name": "create",
        "help": "Creates the envc control table",
        "arguments": [
            {
                "name": "<path>",
                "help": "Path value where it should be created, by default:" + ENVC_TABLE_PATH,
                "arguments": []
            },
        ]
    },
]

def _search_in_actions(target, actions=__ACTIONS):
    for action in actions:
        if target == action["name"]: return action
    return {}

def _print_action(action, indent=0):
    print(__TAB_CHAR*indent, action["name"], ":", action["help"])
    for subaction in action["arguments"]: _print_action(subaction, indent+1)

def __usage():
    print("Usage: envc [action] [opts] [arguments]\n")
    print(__TAB_CHAR, "List of supported actions:")
    for action in __ACTIONS:
        _print_action(action, indent=1)
        print()

    print("""
    Examples:
        # Show the table
        envc show

        # Append a control variable for VIRTUALENV
        envc append VIRTUALENV true

        # Update a control variable
        envc update VIRTUALENV false

        # Remove a control variable
        envc remove VIRTUALENV
        envc remove VIRTUALENV force

        # Restore (only the ones that have not been forced out
        envc restore VIRTUALENV

    """)

def parse_table(ignore_inactive=True):
    if not os.path.exists(ENVC_TABLE_PATH+"/000_envc_table"):
        print("Error: Table file not found.")
        exit(1)

    table = []
    stats = open(ENVC_TABLE_PATH+"/000_envc_table").readlines()
    for statement in stats:
        fields = statement.split('=')
        if len(fields) != 2:
            print("Error: statement %s does not match structure." % statement)
            exit(1)
        if statement.startswith("#") and ignore_inactive: continue 
        table.append((fields[0], fields[1]))
    return table

def update_in_table(target, value):
    if not os.path.exists(ENVC_TABLE_PATH+"/000_envc_table"):
        print("Error: Table file not found.")
        exit(1)

    stats = open(ENVC_TABLE_PATH+"/000_envc_table").readlines()
    wc = stats
    for i, statement in enumerate(stats):
        if statement.split('=')[0] == target:
            wc[i] = "{}={}".format(target, value)
            with open(ENVC_TABLE_PATH+"/000_envc_table", "w") as f:
                f.writelines(wc)
            return
    print("Error: could not find Control variable %s." % target)
    exit(1)

def remove_from_table(target, force=False):
    if not os.path.exists(ENVC_TABLE_PATH+"/000_envc_table"):
        print("Error: Table file not found.")
        exit(1)

    stats = open(ENVC_TABLE_PATH+"/000_envc_table").readlines()
    wc = stats
    for i, statement in enumerate(stats):
        if statement.split('=')[0] == target or statement.split('=')[0][2:] == target:
            if force:  
                del wc[i]
            else:
                wc[i] = "# {}={}".format(statement.split('=')[0], statement.split('=')[1])
            with open(ENVC_TABLE_PATH+"/000_envc_table", "w") as f:
                f.writelines(wc)
            return
    print("Error: could not find Control variable %s." % target)
    exit(1)

if len(sys.argv) <= 1:
    print("Error: number of supplied arguments does not suffice")
    __usage()
    exit(1)

main_action = _search_in_actions(sys.argv[1])
if main_action == {} or main_action == None:
    print("Error: %s not found in action list" % sys.argv[1])
    __usage()
    exit(1)

if main_action["name"] == "version":
    print(VERSION, end=" ")
    print(ENVC_TABLE_PATH+"/000_envc_table")
    exit(0)
elif main_action["name"] == "create":
    if len(sys.argv) == 3:
        path = sys.argv[2]
        if not os.path.exists(path):
            os.mkdir(path)
        open(path+'/000_envc_table', 'w').close()
        os.environ["ENV_TABLE_PATH"] = ENVC_TABLE_PATH
    elif len(sys.argv) == 2:
        if not os.path.exists(ENVC_TABLE_PATH):
            os.mkdir(ENVC_TABLE_PATH)
        open(ENVC_TABLE_PATH+'/000_envc_table', 'w').close()
    else:
        print("Error: supplied arguments do not match correct use.")
        __usage()
        exit(1)
elif main_action["name"] == "show":
    if not os.path.exists(ENVC_TABLE_PATH+"/000_envc_table"):
        print("Error: envc table is not created")
        exit(0)
    table = parse_table(ignore_inactive=False)
    if len(table) == 0:
        print("Empty table.")
        exit(0)
    inactive = []
    print("Active Control Variables")
    for entry in table:
        if entry[0].startswith('#'):
            inactive.append(entry)
            continue
        print(__TAB_CHAR, entry[0], entry[1])
    print("\nInactive Control Variables")
    for entry in inactive:
        print(__TAB_CHAR, entry[0][1:], entry[1])
    exit(0)
elif main_action["name"] == "append":
    if not os.path.exists(ENVC_TABLE_PATH+"/000_envc_table"):
        print("Error: envc table not created")
        exit(1)
    value = "true"
    cv = sys.argv[2]
    if len(sys.argv) == 4:
        value = sys.argv[3]
        if value != "true" and value != "false":
            print("Error: %s is not recognized as a value. Only accepts true or false" % value)
            exit(1)
    with open(ENVC_TABLE_PATH+"/000_envc_table", 'a') as f:
        f.write("{}={}\n".format(cv, value))
    exit(0)
elif main_action["name"] == "update":
    if not os.path.exists(ENVC_TABLE_PATH+"/000_envc_table"):
        print("Error: envc table not created")
        exit(1)
    value = "true"
    cv = sys.argv[2]
    if len(sys.argv) == 4:
        value = sys.argv[3]
        if value != "true" and value != "false":
            print("Error: %s is not recognized as a value. Only accepts true or false" % value)
            exit(1)
    update_in_table(cv, value)
    exit(0)
elif main_action["name"] == "remove":
    if not os.path.exists(ENVC_TABLE_PATH+"/000_envc_table"):
        print("Error: envc table not created")
        exit(1)
    cv = sys.argv[2]
    force = False
    if len(sys.argv) == 4:
        if sys.argv[3] != "force":
            print("Error: unrecognised argument %s. Only force works." % sys.argv[3])
            exit(1)
        force = True
    remove_from_table(cv, force)
    exit(0)
elif main_action["name"] == "restore":
    if not os.path.exists(ENVC_TABLE_PATH+"/000_envc_table"):
        print("Error: envc table not created")
        exit(1)
    cv = sys.argv[2]
    stats = open(ENVC_TABLE_PATH+"/000_envc_table", 'r').readlines()
    wc = stats
    for i, statement in enumerate(stats):
        if statement.split('=')[0] == '# ' + cv:
            wc[i] = "{}={}".format(cv, statement.split('=')[1])
            with open(ENVC_TABLE_PATH+"/000_envc_table", 'w') as f:
                f.writelines(wc)
            exit(0)
    print("Error: could not find inactive control variable %s" % cv)
    exit(1)
else:
    print("Error: should not raise")
    exit(1)
