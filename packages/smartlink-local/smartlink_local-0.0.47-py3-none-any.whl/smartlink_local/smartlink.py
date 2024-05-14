import json

# from database_mysql_local.generic_crud import GenericCRUD
from database_infrastructure_local.number_generator import NumberGenerator
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.MetaLogger import MetaLogger
from message_local.Recipient import Recipient
from queue_worker_local.queue_worker import QueueWorker
from user_context_remote.user_context import UserContext
# from entity_type_local.entity_enum import EntityTypeId

SMARTLINK_COMPONENT_ID = 258
SMARTLINK_COMPONENT_NAME = "smartlink"
DEVELOPER_EMAIL = "akiva.s@circ.zone"
logger_object = {
    'component_id': SMARTLINK_COMPONENT_ID,
    'component_name': SMARTLINK_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}

SESSION_LENGTH = 32
# If adding more actions, make sure to update action_to_parameters and requirements.txt
VERIFY_EMAIL_ADDRESS_ACTION_ID = 17


class SmartlinkLocal(QueueWorker, metaclass=MetaLogger, object=logger_object):
    def __init__(self, is_test_data: bool = False):
        # QueueWorker is a subclass of GenericCRUD.
        QueueWorker.__init__(self, schema_name="smartlink", table_name="smartlink_table",
                             queue_item_id_column_name="smartlink_id", view_name="smartlink_view",
                             action_boolean_column="is_smartlink_action", is_test_data=is_test_data)

        self.user = UserContext()

    # We use primitive types for parameters and return value because we want to be able to call this function from srvls
    def insert(self, smartlink_type_id: int, campaign_id: int,
               from_recipient: dict = None, to_recipient: dict = None) -> dict:
        """Returns the inserted row as a dict"""
        # TODO should have an expiration parameter with a default of 7 days in case of email invitation,
        #  a few hours for sending pin code
        # TODO add support of multiple criteria per campaign
        session = self._generate_session()
        smartlink_data = super().select_one_dict_by_column_and_value(view_table_name="smartlink_type_view",
                                                       column_name="smartlink_type_id",
                                                       column_value=smartlink_type_id)

        # TODO: add updated_real_user_id, updated_effective_profile_id, updated_user_id, updated_effective_user_id)
        smartlink_details = {
            "campaign_id": campaign_id,
            "action_id": smartlink_data["action_id"],
            "dialog_workflow_script_id": smartlink_data["dialog_workflow_script_id"],
            "smartlink_type_id": smartlink_type_id,
            "created_real_user_id": self.user.get_real_user_id(),
            "created_effective_user_id": self.user.get_effective_user_id(),
            "created_effective_profile_id": self.user.get_effective_profile_id(),
            # TODO: get to_group_id and effective user id
        }
        if from_recipient:
            from_recipient_object = Recipient.from_json(from_recipient)
            smartlink_details["from_email_address_old"] = from_recipient_object.get_email_address()
            # smartlink_details["from_phone_id"] = from_recipient_object.get_normizalied_phone()
            # contact_id, user_id, person_id, profile_id
            # TODO: those are foreign keys, so we have to insert them first to the relevant tables
            # smartlink_details.update({"from_" + key: value for key, value in from_recipient.items() if key.endswith("_id")})

        if to_recipient:
            to_recipient_object = Recipient.from_json(to_recipient)
            smartlink_details["to_email_address_old"] = to_recipient_object.get_email_address()
            # smartlink_details["to_phone_id"] = to_recipient_object.get_normizalied_phone()
            smartlink_details["lang_code"] = to_recipient_object.get_preferred_lang_code_str()
            # smartlink_details.update({"to_" + key: value for key, value in to_recipient.items() if key.endswith("_id")})

        smartlink_id = super().insert(schema_name="smartlink", data_dict=smartlink_details)

        smartlink_details["smartlink_id"] = smartlink_id
        smartlink_details["session"] = session  # we can't add it before the insert because it's not in the table

        return smartlink_details

    # REST API GET request with GET parameter id=GsMgEP7rQJWRZUNWV4ES which executes a function based on action_id
    # from action_table with all fields that are not null in starlink_table (similar to queue worker but sync)
    # and get back from the action json with return-code, redirection url, stdout, stderr...
    # call api_management.incoming_api() which will call api_call.insert()

    def execute(self, identifier: str) -> dict:
        session = self._generate_session()
        smartlink_details = self.select_one_dict_by_column_and_value(column_name="identifier",
                                                       column_value=identifier)
        if not smartlink_details:
            self.logger.error(message=f"identifier {identifier} not found",
                              object={"session": session})
            return {}

        action_to_parameters = {
            VERIFY_EMAIL_ADDRESS_ACTION_ID: {
                "function_parameters_json": {"email_address": smartlink_details["to_email_address_old"]},
                "class_parameters_json": {}},
            # If adding more actions, make sure to update requirements.txt
            # ...
        }
        if smartlink_details["action_id"] not in action_to_parameters:
            self.logger.error(message=f"action_id {smartlink_details['action_id']} not found",
                              object={"session": session})
            return {}
        execution_details = {
            "action_id": smartlink_details["action_id"],
            "smartlink_id": identifier,
            "function_parameters_json": json.dumps(
                action_to_parameters[smartlink_details["action_id"]]["function_parameters_json"]),
            "class_parameters_json": json.dumps(
                action_to_parameters[smartlink_details["action_id"]]["class_parameters_json"]),
            "session": session,
            "component_id": SMARTLINK_COMPONENT_ID,
            # "user_jwt": self.user.get_user_jwt(),
        }
        # TODO: save redirection url (how?)
        # AWS Lambda environment is read-only, so we can't install packages.
        super().execute(execution_details=execution_details, install_packages=False)

        smartlink_details["session"] = session

        return smartlink_details

    # 2. REST API POST gets json with all the details of a specific identifier for Dialog Workflow Remote
    def get_smartlink_by_identifier(self, identifier: str) -> dict:
        session = self._generate_session()

        smartlink_details = super().select_one_dict_by_column_and_value(column_name="identifier",
                                                          column_value=identifier)
        if not smartlink_details:
            self.logger.error(message=f"smartlink_id {identifier} not found",
                              object={"session": session})
            return {}
        smartlink_details["session"] = session

        return smartlink_details

    def get_smartlink_by_id(self, smartlink_id: int) -> dict:
        session = self._generate_session()

        smartlink_details = super().select_one_dict_by_column_and_value(column_name="smartlink_id",
                                                          column_value=smartlink_id)
        if not smartlink_details:
            self.logger.error(message=f"smartlink_id {smartlink_id} not found",
                              object={"session": session})
            return {}

        smartlink_details["session"] = session

        return smartlink_details

    @staticmethod
    def _generate_session() -> str:
        return NumberGenerator.get_random_identifier(schema_name="logger", view_name="logger_view",
                                                     identifier_column_name="session", length=SESSION_LENGTH)

    def insert_smartlink_type(self, **kwargs) -> int:
        return super().insert(table_name="smartlink_type_table", data_dict=kwargs)

    def get_test_smartlink_type_id(self) -> int:
        return super().get_test_entity_id(entity_name="smartlink_type",
                                          view_name="smartlink_type_view",
                                          insert_function=self.insert_smartlink_type,
                                          insert_kwargs={"name": "Test Smartlink Type",
                                                         "action_id": VERIFY_EMAIL_ADDRESS_ACTION_ID})
