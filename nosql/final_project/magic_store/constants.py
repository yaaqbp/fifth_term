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

    OK = {"code": OK_CODE, "description": "OK"}
    INCORRECT_NAMESPACE = {"code": INCORRECT_NAMESPACE_CODE, "description": "Incorrect_(nonexisting)_namespace"}
    INCORRECT_KEY = {"code": INCORRECT_KEY_CODE, "description": "Incorrect_key"}
    INCORRECT_GUARD = {"code": INCORRECT_GUARD_CODE, "description": "Incorrect_guard"}
    INCORRECT_TYPE = {"code": INCORRECT_TYPE_CODE, "description": "Incorrect_type"}
    INCORRECT_USERNAME = {"code": INCORRECT_USERNAME_CODE, "description": "Incorrect_username"}
    INCORRECT_USERTYPE = {"code": INCORRECT_USERTYPE_CODE, "description": "Incorrect_usertype"}
    INCORRECT_PASSWORD = {"code": INCORRECT_PASSWORD_CODE, "description": "Incorrect_password"}
    INCORRECT_PERMISSION = {"code": INCORRECT_PERMISSION_CODE, "description": "Incorrect_permission"}
    @classmethod
    def ok(cls, value, guard):
        result = cls.OK.copy()
        result["value"] = value
        result["guard"] = guard
        return result

class EVENTS:
    TYPES = [
        'put',
        'get',
        'createNamespace',
        'createUser',
        'init', 
        'load', 
        'save', 
        'saveEvents',
        'delete',
        'login'
        ]

class USERS:
    PERMISSIONS = {
        'admin': EVENTS.TYPES,
        'superuser':[
            'put',
            'get',
            'delete',
            'createNamespace',
        ],
        'user':[
            'put',
            'get'
        ],
        'guest':[]
    }