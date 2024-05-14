from dotenv import load_dotenv
from logger_local.Logger import Logger
from .organizations_constants import ORGANIZATIONS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT
from user_context_remote.user_context import UserContext
from database_mysql_local.generic_crud_ml import GenericCRUDML
from language_remote.lang_code import LangCode
load_dotenv()

logger = Logger(object=ORGANIZATIONS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT)
user_context = UserContext()

DEFAULT_SCHEMA_NAME = "organization"
DEFAULT_TABLE_NAME = "organization_table"
DEFAULT_VIEW_NAME = "organization_view"
DEFAULT_ID_COLUMN_NAME = "organization_id"
DEFAULT_ML_TABLE_NAME = "organization_ml_table"
DEFAULT_ML_VIEW_NAME = "organization_ml_view"
DEFAULT_ML_ID_COLUMN_NAME = "organization_ml_id"
DEFAULT_NOT_DELETED_ML_VIEW_NAME = "organization_ml_not_deleted_view"

'''
"organization_table fields":
    "number",
    "identifier",
    "is_approved",
    "is_main",
    "point",
    "location_id",
    "profile_id",
    "parent_organization_id",
    "non_members_visibility_scope_id",
    "members_visibility_scope_id",
    "Non_members_visibility_profile_id",
    "is_test_data",
    "created_timestamp",
    "created_user_id",
    "created_real_user_id",
    "created_effective_user_id",
    "created_effective_profile_id",
    "updated_timestamp",
    "updated_user_id",
    "updated_real_user_id",
    "updated_effective_user_id",
    "updated_effective_profile_id",
    "start_timestamp",
    "end_timestamp",
    "main_group_id"

organization_ml_table fields:
    "organization_ml_id",
    "organization_id",
    "lang_code",
    "is_main",
    "name",
    "is_name_approved",
    "is_description_approved",
    "description"
'''


class OrganizationsLocal(GenericCRUDML):
    def __init__(self, default_schema_name=DEFAULT_SCHEMA_NAME, default_table_name=DEFAULT_TABLE_NAME,
                 default_id_column_name=DEFAULT_ID_COLUMN_NAME, is_test_data=False):
        GenericCRUDML.__init__(self, default_schema_name=default_schema_name,
                               default_table_name=default_table_name,
                               default_id_column_name=default_id_column_name,
                               is_test_data=is_test_data)
        self.default_view_table_name = DEFAULT_VIEW_NAME

    def insert_organization(self, organization_dict: dict) -> tuple[int, int]:
        logger.start(object={'data': str(organization_dict)})
        organization_data_dict = {
            "name": organization_dict.get('name'),
            "is_approved": organization_dict.get('is_approved'),
            "is_main": organization_dict.get('is_main'),
            "point": organization_dict.get('point'),
            "location_id": organization_dict.get('location_id'),
            "profile_id": organization_dict.get('profile_id'),
            "parent_organization_id": organization_dict.get('parent_organization_id'),
            "non_members_visibility_scope_id": organization_dict.get('non_members_visibility_scope_id'),
            "members_visibility_scope_id": organization_dict.get('members_visibility_scope_id'),
            "Non_members_visibility_profile_id": organization_dict.get('Non_members_visibility_profile_id'),
            "main_group_id": organization_dict.get('main_group_id')
        }
        organization_id = GenericCRUDML.insert(self, data_dict=organization_data_dict)

        organization_ml_data_dict = {
            "organization_id": organization_id,
            "lang_code": organization_dict.get('lang_code'),
            "is_main": organization_dict.get('is_main'),
            "title": organization_dict.get('title'),
            "is_name_approved": organization_dict.get('is_name_approved'),
            "is_description_approved": organization_dict.get('is_description_approved'),
            "description": organization_dict.get('description')
        }
        organization_ml_id = GenericCRUDML.insert(self, table_name="organization_ml_table",
                                                  data_dict=organization_ml_data_dict)

        logger.end(object={'organization_id': organization_id,
                   'organization_ml_id': organization_ml_id})
        return organization_id, organization_ml_id

    def upsert_organization(self, organization_dict: dict, order_by: str = "") -> dict:
        logger.start(object={'data': str(organization_dict)})
        lang_code = LangCode.detect_lang_code(organization_dict.get('title'))
        organization_data_dict = {
            "name": organization_dict.get('name'),
            "is_approved": organization_dict.get('is_approved'),
            "is_main": organization_dict.get('is_main'),
            "point": organization_dict.get('point'),
            "location_id": organization_dict.get('location_id'),
            "profile_id": organization_dict.get('profile_id'),
            "parent_organization_id": organization_dict.get('parent_organization_id'),
            "non_members_visibility_scope_id": organization_dict.get('non_members_visibility_scope_id'),
            "members_visibility_scope_id": organization_dict.get('members_visibility_scope_id'),
            "Non_members_visibility_profile_id": organization_dict.get('Non_members_visibility_profile_id'),
            "main_group_id": organization_dict.get('main_group_id')
        }

        organization_ml_data_dict = {
            "is_main": organization_dict.get('is_main'),
            "title": organization_dict.get('title'),
            "is_name_approved": organization_dict.get('is_name_approved'),
            "is_description_approved": organization_dict.get('is_description_approved'),
            "description": organization_dict.get('description')
        }
        if "(" and ")" in organization_dict.get('title'):
            organization_id, organzation_ml_ids_list = GenericCRUDML.upsert_value_with_abbreviations(
                self, data_ml_dict=organization_ml_data_dict,
                lang_code=lang_code,
                data_dict=organization_data_dict,
                schema_name=DEFAULT_SCHEMA_NAME,
                table_name=DEFAULT_TABLE_NAME,
                ml_table_name=DEFAULT_ML_TABLE_NAME,
                order_by=order_by
            )
        else:
            organization_id, organzation_ml_id = GenericCRUDML.upsert_value(
                self, data_ml_dict=organization_ml_data_dict,
                lang_code=lang_code,
                data_dict=organization_data_dict,
                schema_name=DEFAULT_SCHEMA_NAME,
                table_name=DEFAULT_TABLE_NAME,
                ml_table_name=DEFAULT_ML_TABLE_NAME,
                order_by=order_by
            )
            organzation_ml_ids_list = [organzation_ml_id]

        upsert_information = {
            "organization_id": organization_id,
            "organization_ml_ids_list": organzation_ml_ids_list
        }
        logger.end(object={'organization_id': organization_id,
                   'organzation_ml_ids_list': organzation_ml_ids_list})
        return upsert_information

    def update_organization(self, organization_id: int, organization_ml_id: int, organization_dict: dict) -> None:
        logger.start(object={'organization_id': organization_id, 'data': str(organization_dict)})
        organization_data_dict = {
            "name": organization_dict.get('name'),
            "is_approved": organization_dict.get('is_approved'),
            "is_main": organization_dict.get('is_main'),
            "point": organization_dict.get('point'),
            "location_id": organization_dict.get('location_id'),
            "profile_id": organization_dict.get('profile_id'),
            "parent_organization_id": organization_dict.get('parent_organization_id'),
            "non_members_visibility_scope_id": organization_dict.get('non_members_visibility_scope_id'),
            "members_visibility_scope_id": organization_dict.get('members_visibility_scope_id'),
            "Non_members_visibility_profile_id": organization_dict.get('Non_members_visibility_profile_id'),
            "main_group_id": organization_dict.get('main_group_id')
        }
        GenericCRUDML.update_by_id(self, id_column_value=organization_id,
                                   data_dict=organization_data_dict)

        organization_ml_data_dict = {
            "organization_id": organization_id,
            "lang_code": organization_dict.get('lang_code'),
            "is_main": organization_dict.get('is_main'),
            "title": organization_dict.get('title'),
            "is_name_approved": organization_dict.get('is_name_approved'),
            "is_description_approved": organization_dict.get('is_description_approved'),
            "description": organization_dict.get('description')
        }
        GenericCRUDML.update_by_id(self, table_name="organization_ml_table",
                                   id_column_value=organization_ml_id, data_dict=organization_ml_data_dict,
                                   id_column_name="organization_ml_id")
        logger.end()

    def get_organization_dict_by_organization_id(self, organization_id: int, organization_ml_id: int = None,
                                                 view_table_name: str = None) -> dict:
        logger.start(object={'organization_id': organization_id})
        view_table_name = view_table_name or self.default_view_table_name
        organization_ml_dict = {}
        if organization_ml_id:
            organization_ml_dict = self.select_one_dict_by_id(view_table_name="organization_ml_view",
                                                              id_column_value=organization_ml_id,
                                                              id_column_name="organization_ml_id")
        organization_dict = self.select_one_dict_by_id(view_table_name=view_table_name, id_column_value=organization_id,
                                                       id_column_name="organization_id")
        logger.end(object={'organization_ml_dict': str(organization_ml_dict)})
        return {**organization_dict, **organization_ml_dict}

    def get_organizations_names_list_by_organizations_ids(self, organizations_ids_list: list[int],
                                                          lang_codes_list: list[LangCode] = None,
                                                          view_table_name: str = None) -> list[str]:
        logger.start(object={'organizations_ids_list': organizations_ids_list})
        if lang_codes_list is None:
            lang_codes_list = [LangCode.ENGLISH]
        view_table_name = view_table_name or DEFAULT_ML_VIEW_NAME
        organizations_names_list = []
        for organization_id in organizations_ids_list:
            organization_name_dicts = self.select_multi_dict_by_id(
                view_table_name=view_table_name,
                select_clause_value="title, lang_code",
                id_column_name="organization_id",
                id_column_value=organization_id
            )
            # filter by lang_codes_list
            for lang_code in lang_codes_list:
                for organization_name_dict in organization_name_dicts:
                    if organization_name_dict.get('lang_code') == lang_code.value:
                        organization_name = organization_name_dict.get('title')
                        organizations_names_list.append(organization_name)
        logger.end(object={'organizations_names_list': str(organizations_names_list)})
        return organizations_names_list

    def delete_by_organization_id(self, organization_id: int, organization_ml_id: int = None) -> None:
        logger.start(object={'organization_id': organization_id})
        # Delete from organization_table
        self.delete_by_id(table_name="organization_table",
                          id_column_name="organization_id", id_column_value=organization_id)
        # Delete from organization_ml_table
        if organization_ml_id:
            self.delete_by_id(table_name="organization_ml_table", id_column_name="organization_ml_id",
                              id_column_value=organization_ml_id)
        logger.end()

    def get_test_organization_id(self) -> int:
        return self.get_test_entity_id(
            entity_name="organization",
            insert_function=self.insert_organization
        )
