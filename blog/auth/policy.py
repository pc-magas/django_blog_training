from .groups import AUTHOR, EDITOR
from .permissions import (
    CREATE_ARTICLE,
    UPDATE_ARTICLE,
    DELETE_ARTICLE,
)

GROUP_PERMISSIONS = {
    AUTHOR: {
        CREATE_ARTICLE,
    },
    EDITOR: {
        CREATE_ARTICLE,
        UPDATE_ARTICLE,
    },
}