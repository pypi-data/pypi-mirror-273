# pyVRL

Exposes Vector VRL to Python for fast, simple & unified transforms
## Installation

`pip install pyVRL`


## Use

Create an instance of pyvrl.Transform using the VRL program as the sole argument

Apply the program to data with the object's `remap` function

```
>>> from pyvrl import Transform
>>> data: dict = {"x": "foo"}
>>> vrl_program = '''
... .y = "bar"
... .x = upcase!(.x)
... .z = uuid_v7()
... .
... '''
>>> transform = Transform(vrl_program)
>>> output = transform.remap(data)
>>> print(output)
{'x': 'FOO', 'y': 'bar', 'z': '018f79d0-812b-7f90-bc74-85042e23db44'}
```
