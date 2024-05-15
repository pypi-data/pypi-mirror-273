# Introduction
A zero dependency, single file string argument parser written in python.  
You can define commands by creating simple python dictionaries, parse strings for the defined fields, and receive a structured result. The argument parser handles some basic python types, typecasting, missing values, default values, nested lists and tuples, error reporting, and any combination of the above.

# Installation
Currently the easiest way to use this module is to do a local pip install.
```console
git clone git@github.com:flpeters/argument_parsing.git
cd argument_parsing
pip install -e .
```

# Documentation

This entire module provides exactly two functions.  
A single function is provided for processing your definition of a __"command"__ as well as the string __"arguments"__ you want to parse, into structured data. 
```python
def parse_arguments(command:dict, arguments:str) -> (bool, dict, dict):
```  
A second function is provided for changing the settings of how errors and warnings are reported.
```python
def set_report_options(report_error:bool=True, report_warning:bool=True,
                       raise_error:bool=False, raise_warning:bool=False,
                       silent:bool=False) -> None:
```  

#### The __command__
is a simple dictionary. The keys are the keywords which will be parsed out from the arguments string. Each keyword maps to either a datatype, or a default value which will be used to infere the datatype.  
Example `command`:
```python
{
    'name'   : str,
    'weather': 'sunny',
    'celsius': float,
    'age'    : int,
    'thirsty': bool,
    'tired'  : bool
}
```

#### The __arguments__
are passed as a whitespacespace separated string. Keywords start with a hyphen-minus (`'-'`), and depending on the datatype of the keyword, are followed by zero, one, multiple, or optional values.  
Example `arguments`:
```python
'-name bob -age 99 -celsius 30.5 -thirsty'
```

#### The __return__ value
is a three-tuple of __"success"__, __"result"__, and __"is_set"__.
- `success` is a single `bool`, which tells you whether or not parsing was successful. If this is `False`, the other two arguments are not guaranteed to be valid. There will be an error message with details on why parsing failed.  
- `result` is a `dict` with exactly the same keys as the input `command`. The values will be set to what was parsed from the `arguments` string. In cases where `success` is `False`, this might only be partially filled out, so `success` should always be checked.
- `is_set` is a `dict`, which also contains exactly the same keys as `command`. The values are all either `True` or `False` depending on if the keyword was present in the `arguments` string. In cases where a default value is given in `command`, only if the default was overwritten will the value be `True`. This holds even for `bool` arguments.  

`return` values given the example inputs above:
```python
success = True
result  = {'name': 'bob',
           'weather': 'sunny',
           'celsius': 30.5,
           'age': 99,
           'thirsty': True,
           'tired': False}
is_set  = {'name': True,
           'weather': False,
           'celsius': True,
           'age': True,
           'thirsty': True,
           'tired': False}
```

## Supported datatypes
A __primitive type__ is a simple python datatype. Depending on which type is used when defining the keywords of a `command`, the parsing rules will change.  

---

The following __primitive types__ are supported:  
#### string
A keyword of type `str` always requires exactly one value.
```python
command   = {'weather': str}
arguments = '-weather sunny'
success, result, is_set = parse_arguments(command, arguments)
result    = {'weather': 'sunny'}
is_set    = {'weather': True}
```
As long as this value doesn't contain any whitespace, the characters it is made up of don't matter. Any punctuation or numbers will just be treated as part of the string.
```python
arguments = '-weather 1234'
...
result    = {'weather': '1234'}
is_set    = {'weather': True}
```
```python
arguments = '-weather -cloudy'
...
result    = {'weather': '-cloudy'}
is_set    = {'weather': True}
```
When a default value is set, the keyword becomes optional. Should the keyword not be part of the `arguments`, then the default value will be placed in the `results` instead.
```python
command   = {'weather': 'cloudy'}
arguments = ''
...
result    = {'weather': 'cloudy'}
is_set    = {'weather': False}
```


#### boolean
A keyword of type `bool` requires no value. If the keyword appears in the `arguments`, the result is automatically set to `True`. Setting the datatype of a keyword to `bool` in `command` is the same as specifying the default value `False`. This also means that the `result` of a `bool` keyword with a default value of `True` can never be set to `False`.

```python
command   = {'rainy': bool}
arguments = '-rainy'
...
result    = {'rainy': True}
is_set    = {'rainy': True}
```
```python
command   = {'rainy': bool}
arguments = ''
...
result    = {'rainy': False}
is_set    = {'rainy': False}
```
```python
command   = {'rainy': True}
arguments = ''
...
result    = {'rainy': True}
is_set    = {'rainy': False}
```

#### integer
A keyword of type `int` always requires exactly one value.
```python
command   = {'meters': int}
arguments = '-meters 26'
...
result    = {'meters': 26}
is_set    = {'meters': True}
```
The value which comes after the keyword will first be cast to `float`, and then to `int`. This is partly due to how python works, but also to check for a remainder in case the provided value was actually a `float`.
This also means that a sign in front of the number will be respected.
```python
arguments = '-meters -15'
...
result    = {'meters': -15}
```
```python
arguments = '-meters +15.0'
...
result    = {'meters': 15.0}
```
```python
arguments = '-meters 15.4'
...
result    = {'meters': 15}
# This will result in a warning that the remainder of 0.4 has been cut off.
```
The default value behaviour is the same as for strings.
```python
command   = {'meters': 33}
arguments = ''
...
result    = {'meters': 33}
is_set    = {'meters': False}
```

#### float
A keyword of type `float` always requires exactly one value.
The value which comes after the keyword will simply be cast to a python `float`. What is and what isn't a valid python `float` can be suprising, so you should check the [casting rules](https://docs.python.org/3/library/functions.html#float) beforehand.
```python
command   = {'celsius': float}
arguments = '-celsius 23.6'
...
result    = {'celsius': 23.6}
is_set    = {'celsius': True}
```
```python
command   = {'celsius': float}
arguments = '-celsius -10.0'
...
result    = {'celsius': -10.0}
```
```python
command   = {'celsius': float}
arguments = '-celsius inf'
...
result    = {'celsius': inf}
```
The default value behaviour is the same as for strings.
```python
command   = {'celsius': float('nan')}
arguments = ''
...
result    = {'celsius': nan}
is_set    = {'celsius': False}
```

---

A __composite type__ is a `list` or `tuple` of one or more values of potentially multiple datatypes. Since `list` or `tuple` have the same semantics and can be used interchangeably, they will be referred to as 'array' for the purpose of this documentation.  

The following __composite types__ are supported:  

#### un-bounded array
Specifying only the type `list` or `tuple`, will result in an 'unbounded array' of that type, meaning that all values following the keyword will be added to the array, until either the end of the `arguments` string is reached, or a value starts with a hyphen-minus (`'-'`), which denotes the start of the next argument. All values of this unbounded array will be of type `str`. This kind of argument should be used with caution because, for instance, negative values will be treated as the start of a new argument due to them starting with a hyphen-minus sign.  
```python
{
    'unbounded_list' : list,
    'unbounded_tuple': tuple,
}
```  

#### fixed array
By specifying an array containing the types, default values, and ordering you want the values to have, you can define a fixed array. Their construction can get arbitrarily complex, mixing and matching any supported primitive type and fixed arrays you want. The only thing not allowed, is using an unbounded array inside a fixed array. All values will be cast to the corresponding type using all the same semantics as if they were single values (see above).  
The only exception to that is the `bool` type. Since the value can't be decided based on presence of absence, a value has to be given. The value has to be either `'True'`, `'False'`, or interpretable as a `float`, which will then be cast to a `bool`. This means that e.g. `'0.0'` will result in `False`, and `'123'` will result in `'True'` (careful, check the [casting rules](https://docs.python.org/3.3/library/stdtypes.html?highlight=frozenset#truth-value-testing) first).
```python
{
    'arg1': [int]*5,
    'arg2': (3.14, 'pi', bool),
    'arg3': (bool, str, 123)*2,
    'arg4': [[0]*3, [1]*3, [str]*3],
    'arg5': [str, int, bool, True, [1, '2', 3, bool], (2.1, float)]
}
```

# Attribution
This argument parser is largely inspired by and based upon, but in no way affiliated with, the work by [Jonathan Blow](https://www.youtube.com/@jblow888) as seen in these two videos on his youtube channel.
> [Jonathan Blow - Livestream: Metaprogramming Use Case: Command-Line Argument Parsing - Part 1](https://youtu.be/TwqXTf7VfZk)  
> [Jonathan Blow - Livestream: Metaprogramming Use Case: Command-Line Argument Parsing - Part 2](https://youtu.be/pgiVrhsGkKY)