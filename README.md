# ResultWrapper


## How to install it?

You can install ResultWrapper from this Github repository with `python3 setup.py install`,
or just install it directly from pypi with `pip3 install result-wrapper`.

## What is it?

ResultWrapper is a very small utility library that provides a class containing either an Error, or a set of Results.
This can be used in APIs to quickly and easy communicate if the operation failed or not. A `ResultWrapper` instance
provides access to its underlying results if it did not fail, otherwise all access to possible results are denied.

## How to use it?

To enable the capabilities of ResultWrapper, decorate a function with the `wrap_result` decorator.
This function then returns an instance of `ResultWrapper`. To check wether a `ResultWrapper` is failed or not, use
the `.failed` property.

You can pass a tuple of exception classes that should be caught and transformed
to a failed Result in the decorator parameter `exceptions`:

```python3
from result_wrapper import wrap_result

@wrap_result(exceptions=(ValueError,))
def function1():
    raise ValueError("This exception will be caught and transformed to a failed result.")

@wrap_result(exceptions=(ValueError,))
def function2():
    raise TypeError("This exception will not be caught. The exception is thrown normally.")

assert function1().failed is True
function2() # this will throw TypeError !!!
```

Another way of returning a failed result is to use the `ResultWrapper.make_failed` function:

```python3
from result_wrapper import wrap_result, ResultWrapper

@wrap_result
def function1():
    return ResultWrapper.make_failed()

assert function1().failed is True
```

Optionally you can pass any object to the `make_failed` function to pass some error information to the caller.
In the case of a thrown exception, the error information is set to the arguments to the constructor of the exception:

```python3
from result_wrapper import wrap_result, ResultWrapper

@wrap_result
def function1():
    return ResultWrapper.make_failed({"ErrorID": 1})

@wrap_result(exceptions=(ValueError,))
def function2():
    raise ValueError({"ErrorID": 1})

assert function1().error_information.get("ErrorID") == 1
assert function2().error_information.get("ErrorID") == 1
```

To return a successful result, return an instance of `Result` or `ResultWrapper.make_succeeded`:

```python3
from result_wrapper import wrap_result, Result, ResultWrapper

@wrap_result
def function1():
    return Result(result1="value1", result2=2)

@wrap_result
def function2():
    return ResultWrapper.make_succeeded(result1="value1", result2=2)

result = function1()
assert result.result1 == "value1"
assert result.result2 == 2

result = function2()
assert result.result1 == "value1"
assert result.result2 == 2
```


