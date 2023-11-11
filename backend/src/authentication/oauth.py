from fastapi.security import OAuth2PasswordBearer

OAuthSchema = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    scopes={
        # Admin Scopes
        "admin": "All permissions",
        # Premium Scopes
        "premium:user:read": "Read permission for Premium User",
        "premium:user:update": "Update permission for Premium User",
        "premium:user:delete": "Delete permission for Premium User",
        "premium:user:create": "Create permission for Premium User",
        # Free User scopes
        "free_user:user:read": "Read permission for Free User",
        "free_user:user:update": "Update permission for Free User",
        "free_user:user:delete": "Delete permission for Free User",
        "free_user:user:create": "Create permission for Free User",
        # Premium User Chat Scopes
        "premium:chat:read": "Read permission for Premium User Chat",
        "premium:chat:update": "Update permission for Premium User Chat",
        "premium:chat:delete": "Delete permission for Premium User Chat",
        "premium:chat:create": "Create permission for Premium User Chat",
        # Free User Chat Scopes
        "free_user:chat:read": "Read permission for Free User Chat",
        "free_user:chat:update": "Update permission for Free User Chat",
        "free_user:chat:delete": "Delete permission for Free User Chat",
        "free_user:chat:create": "Create permission for Free User Chat",
    },
)
