from apps.audit.models import AuditLog


from pprint import pprint
class AuditRepository:

    @staticmethod
    def create(**kwargs):
        pprint(kwargs)
        return AuditLog.objects.create(**kwargs)
        
    
    @staticmethod
    def get_by_user(user):
        return AuditLog.objects.filter(user=user)

    @staticmethod
    def get_by_action(action):
        return AuditLog.objects.filter(action=action)
    
    @staticmethod
    def get_by_user(user_id):
        return AuditLog.objects.filter(user_id=user_id)

    @staticmethod
    def get_by_request(request_id):
        return AuditLog.objects.filter(
            request_id=request_id
        )
    
    @staticmethod
    def get_failed():
        return AuditLog.objects.filter(
            status="FAILED"
        )

    @staticmethod
    def list(limit=100):
        return AuditLog.objects.all()[:limit]