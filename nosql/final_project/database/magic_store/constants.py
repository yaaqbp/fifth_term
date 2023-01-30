class MESSAGES:
    OK_CODE = 100
    INCORRECT_NAMESPACE_CODE = 202
    INCORRECT_KEY_CODE = 203
    INCORRECT_GUARD_CODE = 205
    INCORRECT_TYPE_CODE = 207
    INCORRECT_USERNAME_CODE = 209
    INCORRECT_USERTYPE_CODE = 211
    INCORRECT_PASSWORD_CODE = 213
    INCORRECT_PERMISSION_CODE = 215
    INCORRECT_TAG_CODE = 217

    OK = {"code": OK_CODE, "description": "OK"}
    INCORRECT_NAMESPACE = {"code": INCORRECT_NAMESPACE_CODE, "description": "Incorrect_(nonexisting)_namespace"}
    INCORRECT_KEY = {"code": INCORRECT_KEY_CODE, "description": "Incorrect_key"}
    INCORRECT_GUARD = {"code": INCORRECT_GUARD_CODE, "description": "Incorrect_guard"}
    INCORRECT_TYPE = {"code": INCORRECT_TYPE_CODE, "description": "Incorrect_type"}
    INCORRECT_USERNAME = {"code": INCORRECT_USERNAME_CODE, "description": "Incorrect_username"}
    INCORRECT_USERTYPE = {"code": INCORRECT_USERTYPE_CODE, "description": "Incorrect_usertype"}
    INCORRECT_PASSWORD = {"code": INCORRECT_PASSWORD_CODE, "description": "Incorrect_password"}
    INCORRECT_PERMISSION = {"code": INCORRECT_PERMISSION_CODE, "description": "Incorrect_permission"}
    INCORRECT_TAG = {"code": INCORRECT_TAG_CODE, "description": "Incorrect_tag"}
    @classmethod
    def ok(cls, value, guard=None):
        result = cls.OK.copy()
        result["value"] = value
        if guard is not None:
            result["guard"] = guard
        return result

class EVENTS:
    TYPES = [
        'put',
        'get',
        'searchByTag'
        'delete',
        'login',
        'addTag',
        'removeTag',
        'createNamespace',
        'createUser',
        'load', 
        'save', 
        'saveEvents',
        'init', 
        ]

class USERS:
    PERMISSIONS = {
        'admin': EVENTS.TYPES,
        'superuser':EVENTS.TYPES[:8],
        'user':EVENTS.TYPES[:3],
        'guest':[]
    }

