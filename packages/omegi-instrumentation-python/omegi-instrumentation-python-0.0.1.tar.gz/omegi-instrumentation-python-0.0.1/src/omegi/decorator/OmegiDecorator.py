import functools
import inspect
import threading


def omegi_decorator(tracer):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            signature = inspect.signature(func)
            bound_args = signature.bind(*args, **kwargs)
            bound_args.apply_defaults()
            arguments = []
            for name, value in bound_args.arguments.items():
                param = signature.parameters[name]
                arg_type = param.annotation if param.annotation != inspect.Parameter.empty else type(value)
                arguments.append(f"{name}: {arg_type.__name__} = {value}")
            with tracer.start_as_current_span(name=f"{func.__module__}.{func.__name__}") as span:
                span.set_attribute("module", func.__module__)
                span.set_attribute("name", func.__name__)
                span.set_attribute("thread.name", threading.current_thread().name)
                span.set_attribute("thread.id", threading.current_thread().ident)
                span.set_attribute("arguments", arguments)
                return func(*args, **kwargs)
        return wrapper
    return decorator


def requests_omegi_decorator(tracer):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print("IN REQUESTS DECORATOR", flush=True)
            with tracer.start_as_current_span(name=f"{func.__module__}.{func.__name__}") as span:
                span.set_attribute("module", func.__module__)
                span.set_attribute("name", func.__name__)
                span.set_attribute("thread.name", threading.current_thread().name)
                span.set_attribute("thread.id", threading.current_thread().ident)

                response = func(*args, **kwargs)

                if hasattr(response, 'request'):
                    span.set_attribute("http.method", response.request.method)
                    span.set_attribute("http.url", response.url)
                    span.set_attribute("http.status_code", response.status_code)
                    span.set_attribute("http.headers", str(response.headers))

                return response
        return wrapper
    return decorator