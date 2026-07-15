from contextvars import ContextVar




_audit_context = ContextVar("audit_context", default={})



class AuditContext:

    @staticmethod
    def set(data: dict):
        _audit_context.set(data)

    @staticmethod
    def get():
        return _audit_context.get()

    @staticmethod
    def clear():
        _audit_context.set({})