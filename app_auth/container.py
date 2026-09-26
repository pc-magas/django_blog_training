from dependency_injector import containers, providers
import app_auth.services.policy_service as policy_service

class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    policy = providers.Singleton(policy_service.PolicyService)

    role_service = providers.Singleton(
        policy_service.RoleService,
        policy_service
    )

