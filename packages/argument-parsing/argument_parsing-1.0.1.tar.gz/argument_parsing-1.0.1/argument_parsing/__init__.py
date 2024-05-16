__version__ = '1.0.1'

__all__ = ['parse_arguments', 'set_report_options']


#######################################
#               LOGGING               #
#######################################


REPORT_ERROR  :bool = True
REPORT_WARNING:bool = True
RAISE_ERROR   :bool = False
RAISE_WARNING :bool = False
SILENT        :bool = False


def set_report_options(report_error:bool=True, report_warning:bool=True,
                       raise_error:bool=False, raise_warning:bool=False,
                       silent:bool=False) -> None:
    """
    Decide how the Argument Parsing module should report errors and warnings encountered during parsing.
    Independent of these settings, `parse_arguments` will always return True of False based on successful parsing.

    Options
    -------
    report_error, report_warning: bool
        Print the error or warning and then continue if possible.

    raise_error, raise_warning: bool
        Raise an exception with the error or warning message, thus terminating parsing.
        Supersedes report_error / report_warning.

    silent: bool
        Ignore all warnings and errors and continue parsing if possible.
        Supersedes all other report options for errors and warnings alike.

    Returns
    -------
    options: dict
        Echoes back the current state of the available report options as a dict.
    """
    global REPORT_ERROR, REPORT_WARNING
    global RAISE_ERROR , RAISE_WARNING
    global SILENT
    REPORT_ERROR, REPORT_WARNING = report_error, report_warning
    RAISE_ERROR , RAISE_WARNING  = raise_error , raise_warning
    SILENT = (silent or not (report_error or report_warning or raise_error or raise_warning))
    return {'report_error'  : REPORT_ERROR,
            'report_warning': REPORT_WARNING,
            'raise_error'   : RAISE_ERROR ,
            'raise_warning' : RAISE_WARNING,
            'silent'        : SILENT}

# TODO: Maybe allow a user to overwrite report_error and report_warning
#       in order to implement custom behaviour.

def report_error(err:Exception):
    if   SILENT: pass
    elif RAISE_ERROR : raise err
    elif REPORT_ERROR: print(f'[{err.__class__.__name__}]: {err}')


def report_warning(warn:str):
    if   SILENT: pass
    elif RAISE_ERROR : raise Warning(warn)
    elif REPORT_ERROR: print(f'[Warning]: {warn}')


#######################################
#           TYPE CONVERSION           #
#######################################


def to_integer(value:str) -> (bool, int, float):
    "Try converting a str to int.\nReturn success, the value, and possibly a float remainder."
    try:
        f_value   = float(value)
        int_value = int(f_value)
        remainder = f_value - int_value
    except: return False, value, None
    return True, int_value, remainder


def to_float(value:str) -> (bool, float):
    "Try converting a str to float.\nReturn success, and the value."
    # TODO: check if 'inf', 'nan', ...?
    try   : return True , float(value)
    except: return False, value


def to_bool(value:str) -> (bool, bool):
    """Try converting a str to bool.
    'True' and 'False' are recognized, otherwise the value is cast to float, and then to bool.
    Return success, and the value."""
    if value == 'True' : return True, True
    if value == 'False': return True, False
    try   : return True , bool(float(value))
    except: return False, value


def to_unbounded_array(args:list, cursor:int) -> (bool, int, list):
    """Consume any number of values until either reaching the end of args,
    or until finding a value starting with '-', denoting the beginning of a new argument.
    Return success, the cursor, and the list of values.
    Currently this can't actually fail... don't use unbounded lists kids."""
    values = []
    while True:
        string_success, cursor, value = get_next_argument(args, None, cursor, suppress_error=True)
        if string_success:
            if value[0] != '-': values.append(value)
            else: # value starting with '-' means it's the next command
                # TODO: We could try parsing a number here, and only stop if that fails.
                #       numbers, and negative numbers are not valid keywords, so
                #       if it is a number, we can just add it to the array.
                cursor -= 1
                break
        else: break
    return True, cursor, values


def typify(type_or_value:object) -> (type, object):
    """Takes a type or a value.
    Returns a tuple of the type (or type of the value) and value (or None)"""
    return (type_or_value, None) if isinstance(type_or_value, type) else (type(type_or_value), type_or_value)


#######################################
#               PARSING               #
#######################################


def get_next_argument(args:list, name:str, cursor:int, suppress_error:bool=False) -> (bool, int, str):
    "Gets the next argument from the list.\nReturns success, the cursor, and the next argument"
    cursor_1 = cursor + 1
    try: return True, cursor_1, args[cursor_1]
    except IndexError:
        if not suppress_error:
            report_error(SyntaxError(f"End of arguments reached. Missing a value for argument '{name}' at position {cursor_1}"))
        return False, cursor, ''


def handle_one_argument(result:dict, state:dict, arg_type:type, arg_default:object) -> bool:
    "Parse the input args based on arg_type, and set arg_name in result to that value."
    # NOTE: 'state' and 'result' are references not values, and modified from here.
    args     = state['args']
    arg_name = state['name']
    success  = True
    if arg_type == str:
        # get the next argument, advance cursor, set success
        string_success, state['cursor'], value = get_next_argument(args, arg_name, state['cursor'])
        # TODO: How to handle strings that start with a '-'?
        #       Currently we don't do any checks, meaning is something starts with '-',
        #       it is just treated as part of the value and ignored.
        if string_success: result[arg_name] = value
        else: success = False

    elif arg_type == bool:
        # TODO: Should specifying a value also be allowed outside an array?
        #       We currently don't parse additional input outside an array.
        if state['inside_array']:
            string_success, state['cursor'], value = get_next_argument(args, arg_name, state['cursor'])
            if string_success:
                bool_success, value = to_bool(value)
                if bool_success: result[arg_name] = value
                else:
                    report_error(ValueError(f"Value of argument {state['cursor']-1} ('{arg_name}') "\
                    f"was not convertable to bool. Please use 'True', 'False', '0', or '1'. (It was '{value}')"))
                    success = False
            else: success = False
        # special case where supplying the argument means True and not supplying it means use the default (False)
        else: result[arg_name] = True

    elif arg_type == int:
        # get the next argument, cast to int, check for remainder, advance cursor, set success
        string_success, state['cursor'], value = get_next_argument(args, arg_name, state['cursor'])
        if not string_success: return False
        int_success, value, remainder = to_integer(value)
        if int_success:
            result[arg_name] = value
            if remainder:
                report_warning(f"The int argument ('{arg_name}') at position {state['cursor']-1} "\
                              f"has a non zero remained of {remainder}. Maybe change the datatype to float? "\
                              f"(The value was {value+remainder})")
        else:
            report_error(ValueError(f"Value of argument {state['cursor']-1} ('{arg_name}') "\
                                    f"was not an int. (It was '{value}')"))
            success = False

    elif arg_type == float:
        # get the next argument, cast to float, advance cursor, set success
        string_success, state['cursor'], value = get_next_argument(args, arg_name, state['cursor'])
        if not string_success: return False
        float_success, value = to_float(value)
        if float_success: result[arg_name] = value
        else:
            report_error(ValueError(f"Value of argument {state['cursor']-1} ('{arg_name}') "\
                                    f"was not a float. (It was '{value}')"))
            success = False

    elif arg_type == list or arg_type == tuple:
        if arg_default is None: # unbounded list / tuple
            if state['inside_array']:
                report_error(SyntaxError(f"Using an unbounded list or tuple inside an array is not supported."))
                return False
            array_success, state['cursor'], value = to_unbounded_array(args, state['cursor'])
            if array_success: # NOTE: currently this can't actually fail...
                result[arg_name] = arg_type(value)
            else: success = False
            
        else: # predefined list
            s = {'args': args, 'name': 'v', 'cursor': state['cursor'], 'inside_array': True}
            value = []
            # TODO: we need to handle default values here as well. if the last keywords for this array all already have values,
            #       then it's fine if they are missing.
            #       When this is fixed, also change the documentation.
            for i, x in enumerate(arg_default):
                t, d = typify(x)
                n = f'{arg_name}[{i}]'
                s['name'] = n
                r = {n:d}
                member_success = handle_one_argument(r, s, t, d)
                if member_success: value.append(r[n])
                else: # TODO: Improve error message
                    # report_error(SyntaxError(f"Array argument {state['cursor']} ('{arg_name}') was not passed correctly."))
                    return False
            state['cursor'] = s['cursor']
            result[arg_name] = arg_type(value)

    else:
        report_error(TypeError(f"Argument {state['cursor']} ('{arg_name}') is of unsupported type {arg_type}."))
        success = False
        
    return success


def check_is_set(result:dict, is_set:dict) -> bool:
    "Check if any required values (those without defaults), haven't been set yet"
    success = True
    for member, v_is_set in is_set.items():
        if v_is_set: continue
        arg_type, arg_default = typify(result[member])
        if arg_default is None: 
            if arg_type == bool: # NOTE: Special case, not setting a boolean means it's False.
                result[member] = False
                continue
            report_error(ValueError(f"Argument '{member}' has not been set, and no default value was given."))
            success = False
        elif (arg_type == list) or (arg_type == tuple): # this is a bounded list
            # generate list of names with python indexing syntax for better error reporting.
            name = [f'{member}[{i}]' for i in range(len(arg_default))]
            # create a new 'result' dict, mapping the 'idx names' to each of the values of the list.
            r = {n:x for n, x in zip(name, arg_default)}
            # since the entire list hasn't been set, each part of the list has also not been set.
            s = {n:False for n in r}
            # recurse, treating the members of the list as if they comprised a separate command.
            is_set_success = check_is_set(r, s)
            if is_set_success: # re-set result if all members of the list have a default value.
                result[member] = arg_type([r[n] for n in name])
                continue
            else: success = False
    return success


def parse_arguments(command:dict, arguments:str) -> (bool, dict, dict):
    "Finds, casts, and returns values from command, in the given comment."    
    # TODO: check that the type of all commands is supported ahead of time?
    # TODO: handle quoted arguments?
    # TODO: support command aliases?
    arguments = arguments.split()
    members   = command.keys()
    result    = command.copy()
    is_set    = {member : False for member in members}
    state     = {'args': arguments, 'name': '', 'cursor': 0, 'inside_array': False,}
    success   = True
    while state['cursor'] < len(arguments): # for arg in args:
        arg = arguments[state['cursor']]
        if arg[0] != '-':
            report_error(SyntaxError(f"Argument {state['cursor']} ('{arg}') does not start with a '-'."))
            return False, result, is_set
        arg = arg[1:] # remove '-'
        state['name'] = arg # TODO: check that len(arg) > 0?
        
        for key in members: # loop over keys of command (the things we're supposed to find)
            if key != arg: continue    
            if is_set[key]:
                report_error(SyntaxError(f"Argument {state['cursor']} ('{arg}') was given multiple times."))
                success = False
            else:
                arg_type, arg_default = typify(command[key])
                member_success = handle_one_argument(result, state, arg_type, arg_default)
                if member_success: is_set[key] = True
                else: success = False
            break # once we have found the correct struct member, stop!
        else: # TODO: improve this msg. maybe: "is not part of the command"?
            report_error(SyntaxError(f"Argument {state['cursor']} ('{arg}') is not valid."))
            success = False
        if not success: break # stop at first error
        state['cursor'] += 1
        
    if success: success = check_is_set(result, is_set)
    return success, result, is_set