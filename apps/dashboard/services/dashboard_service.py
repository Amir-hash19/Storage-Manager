from apps.dashboard.repositories.dashboard_repository import DashBoardRepository


class DashBoardUserStatisticsService:

    @classmethod
    def execute(cls):
        statistics = DashBoardRepository.get_users_statistics()

        return {
            "total_users": statistics["total"],
            "active_users": statistics["active"],
            "verified_users": statistics["verified"],
            "inactive_users": statistics["total"] - statistics["active"],
            "unverified_users": statistics["total"] - statistics["verified"],
        }





class DashBoardStorageService:

    @classmethod
    def execute(cls):
        summary = DashBoardRepository.get_storage_summary()
        top_users = DashBoardRepository.get_top_storage_users()

        total_quota = summary["quota"] or 0
        used_storage = summary["used"] or 0
        total_users = summary["users"] or 0

        return {
            "total_quota": total_quota,
            "used_storage": used_storage,
            "free_storage": total_quota - used_storage,
            "usage_percent": round(
                (used_storage / total_quota) * 100, 2
            ) if total_quota else 0,
            "average_usage_per_user": (
                used_storage // total_users
                if total_users else 0
            ),
            "top_users": list(top_users),
        }    



class DashBoardAuditService:

    @classmethod
    def execute(cls):
        return  DashBoardRepository.get_logs()   