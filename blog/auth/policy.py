from .groups import AUTHOR, EDITOR


GROUP_PERMISSIONS = {
    AUTHOR: {
        ("add_article"),
        ("update_article")
    },
    EDITOR: {
        ("update_article"),
    },
}
