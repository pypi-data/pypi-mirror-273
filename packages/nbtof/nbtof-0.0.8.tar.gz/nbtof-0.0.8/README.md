# nbtof <!-- omit in toc -->

---

| English | [日本語](https://github.com/Nodaka/nbtof/blob/main/i18n/README-JA.md) |

---

This module is used to convert Jupyter Notebook to the python function with the same process.  


- [Introduction](#introduction)
- [Installation](#installation)
- [Documentation](#documentation)
  - [Marks list](#marks-list)
  - [Details about marks](#details-about-marks)
    - [#@param](#param)
    - [#@default](#default)
    - [#@args](#args)
    - [#@kwargs](#kwargs)
    - [#@return](#return)
    - [#@ignore](#ignore)
    - [#@help](#help)
    - [#@advance](#advance)
    - [#@r\_advance](#r_advance)



## Introduction

Only by writing the `#@~` marks in Jupyter Notebook file, you can easily convert Jupyter Notebook file to the python source file with the function which perform the same process as the Jupyter Notebook file. For example, in the case that you want to convert `sample.ipynb` to function,

  
**sample.ipynb**

```python
#@param
a = 1
b = 1
```
```python
c = a + b
```
```python
#@return
c
```
  
you can get `sample.py` by executing the next code.

```python
import nbtof

nbtof.nbtof_generate(
    notebook_name='sample.ipynb',
    func_py_name='sample.py',
    )
```

**sample.py**

```python
def sample(a, b):
    c = a + b
    return c
```


## Installation
The latest nbtof can be installed from PyPI:  

```
$ pip install nbtof
```


## Documentation

### Marks list

| Mark | Description |
| ---- | ---- |
| `#@param` | Variable names in the cell become function's argument names. The values assigned at the Jupyter Notebook is ignored. |
| `#@default` | Variable names in the cell become function's argument names. The values assigned at the Jupyter Notebook get default values. |
| `#@args` | Variable names in the cell become function's variable length argument *args names. The values assigned at the notebook is ignored. |
| `#@kwargs` | Variable names in the cell become function's variable length argument **kwargs names. The values assigned at the notebook is ignored. |
| `#@return` | The line after this mark become function's return value |
| `#@ignore` | Anything in the cell is ignored. |
| `#@help` | What you write in the cell becomes function's docstring. Please write it in quotation marks. |
| `#@advance` | What you write in the cell is written before the function declaration as it is. (e.g., imports) |
| `#@r_advance` | The comment line with `#` in the cell is written with the `#` removed before the function declaration. Please use to avoid the error in Jupyter Notebook (e.g., relative imports) | 

### Details about marks

#### #@param

The Jupyter Notebook

**sample_param.ipynb**
```python
#@param
a = 0
```
```python
print("Hello World !")
```

is converted into


```python

def sample_param(a):
    print('Hello world !')

```

#### #@default

The Jupyter Notebook

**sample_default.ipynb**
```python
#@default
a = 0
```
```python
print("Hello World !")
```

is converted into


```python

def sample_default(a=0):
    print('Hello world !')

```

#### #@args

**sample_args.ipynb**
```python
#@args
a = 0
```
```python
print("Hello World !")
```

is converted into


```python

def sample_args(*a):
    print('Hello world !')

```


#### #@kwargs

**sample_kwargs.ipynb**
```python
#@kwargs
a = 0
```
```python
print("Hello World !")
```

is converted into


```python
def sample_kwargs(**a):
    print('Hello world !')
```


#### #@return

**sample_return.ipynb**
```python
#@return
a = 0
```
```python
if a == 0:
#@return
    True
else:
#@return
    False
```

is converted into


```python

def sample_return(a):
    if a == 0:
        return True
    else:
        return False
```



#### #@ignore

**sample_ignore.ipynb**
```python
#@ignore
1 + 1
```
```python
print('Hello world !')
```

is converted into


```python
def sample_ignore():
    print('Hello world !')
```

#### #@help
**sample_help.ipynb**
```python
#@help
"""
This function outputs "Hello world !" sentence.

Parameters
----------

Returns
-------

"""
```
```python
print('Hello world !')
```

is converted into


```python
def sample_help():
    """
    This function outputs "Hello world !" sentence.
    
    Parameters
    ----------
    
    Returns
    -------
    
    """
    print('Hello world !')
```

#### #@advance

**sample_advance.ipynb**
```python
#@advance
import os
import sys
```
```python
#@advance
def func():
    print(os.getcwd())
    print(sys.prefix)
    print("Hello world !")
```
```python
func()
```

is converted into


```python
import os
import sys

def func():
    print(os.getcwd())
    print(sys.prefix)
    print('Hello world !')

def sample_advance():
    func()
```

#### #@r_advance

**sample_r_advance.ipynb**
```python
#@r_advance
#from . import foo
#from . import bar
```
```python
print("Hello world !")
```

is converted into


```python
from . import foo
from . import bar

def sample_r_advance():
    print('Hello world !')
```
