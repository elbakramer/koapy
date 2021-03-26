import sys
import inspect
import textwrap

def function_to_script(func):
    function_sig = inspect.signature(func)
    assert all(p.default != p.empty for p in function_sig.parameters), 'Function should not require parameters'

    function_name = func.__name__
    function_impl = inspect.getsource(func)
    function_impl = textwrap.dedent(function_impl)

    script = textwrap.dedent("""
    %s

    if __name__ == '__main__':
        %s()
    """) % (function_impl, function_name)

    return script

def function_to_subprocess_args(func):
    script = function_to_script(func)
    args = [sys.executable, '-c', script]
    return args
