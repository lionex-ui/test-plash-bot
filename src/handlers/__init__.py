from .add_user import router as add_user_router
from .auth import router as auth_router
from .check_domains import router as check_domains_router
from .delete_user import router as delete_user_router
from .edit_user import router as edit_user_router
from .main_admin import router as main_admin_router
from .panels import router as panels_router
from .todo import router as todo_router
from .create_todo import router as create_todo_router
from .get_todo import router as get_todo_router
from .get_all_todo import router as get_all_todo_router
from .update_todo import router as update_todo_router
from .delete_todo import router as delete_todo_router

__all__ = [
    "auth_router",
    "panels_router",
    "add_user_router",
    "delete_user_router",
    "edit_user_router",
    "check_domains_router",
    "main_admin_router",
    "todo_router",
    "create_todo_router",
    "get_todo_router",
    "get_all_todo_router",
    "update_todo_router",
    "delete_todo_router",
]
