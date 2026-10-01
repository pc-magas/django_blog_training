from dependency_injector import containers, providers
from .services.role_service import RoleService
from .services.policy_service import PolicyService


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    policy = providers.Singleton(PolicyService)

    role = providers.Factory(
        RoleService,
        policy_service=policy
    )

