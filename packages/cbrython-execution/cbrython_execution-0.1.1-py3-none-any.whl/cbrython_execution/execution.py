"""Module for helping with javascript/brython interaction and model execution."""
from traceback import format_tb

try:
    from browser import window
    from browser.aio import Future
    from browser.aio import run
    from javascript import JSObject
    from javascript import this
    from javascript import import_modules

    def asyncexe(func):
        async def wrapper(*args, **kwargs):
            # pylint: disable=no-member,broad-exception-caught
            try:
                return await func(*args, **kwargs)
            except Exception as exception:
                if isinstance(exception, JSObject):
                    window.console.err(
                        "raised JSObject in async:",
                        type(exception).__name__,
                        exception,
                    )
                else:
                    print(
                        "raised exception in async:",
                        type(exception).__name__,
                        exception,
                    )
                print("\n".join(format_tb(exception.__traceback__)))
                raise

        return run(wrapper())

    def jsf(func):
        def wrapper(*args, **kwargs):
            return func(this(), *args, **kwargs)

        return wrapper

    def load_module(path):
        future = Future()
        import_modules([path], future.set_result)
        return future

    def futurize(promise):
        future = Future()
        promise.then(
            lambda result: future.set_result(result),
            lambda exception: future.set_exception(exception),
        )
        return future

except ModuleNotFoundError:
    from asyncio import run

    def asyncexe(func):
        async def wrapper(*args, **kwargs):
            # pylint: disable=no-member,broad-exception-caught
            try:
                return await func(*args, **kwargs)
            except Exception as exception:
                print("raised exception in async:", type(exception).__name__, exception)
                print("\n".join(format_tb(exception.__traceback__)))
                raise exception

        return run(wrapper())

    def futurize(task):
        return task
