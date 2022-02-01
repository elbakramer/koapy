from functools import update_wrapper


def update_wrapper_with_click_params(wrapper, wrapped, *args, **kwargs):
    click_params_wrapper = getattr(wrapper, "__click_params__", [])
    click_params_wrapped = getattr(wrapped, "__click_params__", [])
    click_params = click_params_wrapped + click_params_wrapper
    wrapper.__click_params__ = click_params
    wrapped.__click_params__ = click_params
    updated_wrapper = update_wrapper(wrapper, wrapped, *args, **kwargs)
    return updated_wrapper
