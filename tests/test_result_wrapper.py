import pytest

from src.result_wrapper import Result, ResultWrapper, wrap_result
from src.exceptions import ResultNotAccessibleException


@wrap_result(exceptions=(ValueError,))
def dummy_func1(do_raise=False):
    if do_raise:
        raise ValueError("Raised")
    return Result()


@wrap_result(exceptions=(ValueError, TypeError))
def dummy_func2(do_raise=False):
    if do_raise:
        raise TypeError("Raised")
    return Result(val="test")


@wrap_result(exceptions=(ValueError,))
def dummy_func3(do_raise=False):
    if do_raise:
        raise TypeError("Raised")


@wrap_result(exceptions=(ValueError,))
def dummy_func4(do_raise=False):
    if do_raise:
        raise ValueError(Result(ErrorID=1))


def test_results_wrapper():
    assert ResultWrapper.make_failed().failed is True
    assert ResultWrapper.make_succeeded().failed is False

    assert ResultWrapper.make_succeeded(result="value").result == "value"
    with pytest.raises(ResultNotAccessibleException):
        getattr(ResultWrapper.make_failed(), "result")

    with pytest.raises(ResultNotAccessibleException):
        getattr(ResultWrapper(True, None, result="value"), "result")


def test_wraps_results_decorator():
    assert dummy_func1(do_raise=True).failed is True
    assert dummy_func1(do_raise=False).failed is False
    with pytest.raises(AttributeError):
        getattr(dummy_func1(do_raise=False), "val")

    assert dummy_func2(do_raise=True).failed is True
    assert dummy_func2(do_raise=False).failed is False
    assert dummy_func2(do_raise=False).val == "test"
    with pytest.raises(ResultNotAccessibleException):
        getattr(dummy_func2(do_raise=True), "val")

    with pytest.raises(TypeError):
        dummy_func3(do_raise=True)


def test_wraps_result_error_information():
    result_wrapper = dummy_func1(do_raise=True)
    assert result_wrapper.failed is True
    assert result_wrapper.error_information == ("Raised", )

    result_wrapper = dummy_func4(do_raise=True)
    assert result_wrapper.failed is True
    assert result_wrapper.error_information[0].result.get("ErrorID") == 1


def test_wrap_results_return_none():
    assert dummy_func4(do_raise=False).failed is False

