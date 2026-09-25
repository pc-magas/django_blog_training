from .groups import AUTHOR, EDITOR


POLICY = {
    AUTHOR: {
        "is_staff":True,
        "permissions":{
            "add_article",
            "change_article",
            "delete_article",
            "view_article"
        }
    },
    EDITOR: {
        "is_staff":True,
        "permissions":{
            "change_article",
            "view_article",
            "add_user",
            "change_user"
            "delete_user"
        },
        "manage_groups":{
            AUTHOR
        }
    },
}
