from logger_local.LoggerComponentEnum import LoggerComponentEnum


class ProfileUserConstants:
    USER_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 199
    USER_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = "user_local/src/profile_user.py"

    OBJECT_TO_INSERT_CODE = {
        'component_id': USER_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
        'component_name': USER_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
        'developer_email': 'tal.g@circ.zone'
    }

    OBJECT_TO_INSERT_TEST = {
        'component_id': USER_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
        'component_name': USER_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
        'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
        'developer_email': 'tal.g@circ.zone'
    }

    PROFILE_USER_SCHEMA_NAME = "profile_user"
    PROFILE_USER_TABLE_NAME = "profile_user_table"
    PROFILE_USER_VIEW_NAME = "profile_user_view"

    PROFILE_USER_ID_COLUMN_NAME = "id"
    PROFILE_ID_COLUMN_NAME = "profile_id"
    USER_ID_COLUMN_NAME = "user_id"
    IS_MAIN_COLUMN_NAME = "is_main"

    PROFILE_ID_COLUMN_INDEX = 0
    USER_ID_COLUMN_INDEX = 1
    IS_MAIN_COLUMN_INDEX = 2
