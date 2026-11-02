from app_auth.auth.groups import ADMIN

POLICY = {
    # Admin is the system's Admin having all available capabilities and permissions a user can have
    ADMIN: {
        "is_admin":True,
        "permissions":{
            "*",
        },
        "manage_roles":{
            "*"
        }
    },
}
