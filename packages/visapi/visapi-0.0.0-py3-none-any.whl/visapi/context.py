from contextvars import ContextVar

not_bound = object()

application = ContextVar("application", default=not_bound)
