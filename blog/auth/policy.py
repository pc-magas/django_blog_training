from .groups import AUTHOR, EDITOR


GROUP_PERMISSIONS = {
    AUTHOR: {
        "add_article",
        "change_article",
        "delete_article",
        "view_article"
    },
    EDITOR: {
        "change_article",
        "view_article",
        "add_user"
    },
}
