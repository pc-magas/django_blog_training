def permission_codename(permission)->str:
    """
        Supports both:
            "create_article"
        and:
            (
                "create_article",
                "Can create article",
            )
    """

    if isinstance(permission, str):
        return permission

    if isinstance(permission, (tuple, list)) and permission:
        return permission[0]

    raise RuntimeError(f"Invalid permission definition: {permission!r}")


def permission_description(permission)->str:
    if isinstance(permission, (tuple, list)) and len(permission) > 1:
        return permission[1]

    return ""
