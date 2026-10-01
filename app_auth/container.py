from dependency_injector import containers, providers

from app_auth.services.save.user import UserService
from app_auth.services.group_service import GroupService
from app_auth.services.policy_service import PolicyService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    policy_service = providers.Singleton(PolicyService)

    group_service = providers.Singleton(
        GroupService,
        policy_service=policy_service
    )

    user_service = providers.Singleton(
        UserService,
        group_service=group_service
    )
