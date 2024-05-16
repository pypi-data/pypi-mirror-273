# TODO Please make sure every src file will have a test file i.e. CompoundMessage

import json
import random
from collections import defaultdict
from functools import lru_cache

from database_mysql_local.generic_crud import GenericCRUD
from language_remote.lang_code import LangCode
from logger_local.MetaLogger import MetaLogger
from profile_local.profiles_local import ProfilesLocal
from user_context_remote.user_context import UserContext
from variable_local.template import ReplaceFieldsWithValues
from queue_local.database_queue import DatabaseQueue

from .MessageChannels import MessageChannel
from .MessageConstants import object_message
from .MessageTemplates import MessageTemplates
from .Recipient import Recipient

JSON_VERSION = "240416"  # TODO: make it generic


class CompoundMessage(GenericCRUD, metaclass=MetaLogger, object=object_message):
    def __init__(self, *, campaign_id: int = None, message_template_id: int = None, body: str = None,
                 subject: str = None,
                 recipients: list[Recipient] = None, message_id: int = None, is_test_data: bool = False, ui_schema=None,
                 schema=None, field_id=None, form_id: int = None, is_debug: bool = False,
                 is_require_moderator: bool = True):
        """Initializes the CompoundMessage instance and sets the compound message in the instance and in the database"""
        super().__init__(default_schema_name="message", default_table_name="message_table",
                         default_view_table_name="message_view", default_column_name="message_id",
                         is_test_data=is_test_data)

        self.campaign_id = campaign_id
        self.message_template_id = message_template_id
        self.__body = body
        self.__subject = subject
        self.recipients = recipients
        self.message_id = message_id
        self.form_id = form_id
        self.is_debug = is_debug
        self.__compound_message = {}
        self.ui_schema = ui_schema
        self.schema = schema
        self.field_id = field_id
        self.is_require_moderator = is_require_moderator

        self.profile_local = ProfilesLocal()
        self.message_template = MessageTemplates()
        self.user_context = UserContext()
        self.queue = None

        self.set_compound_message_after_text_template()

    def get_queue(self):
        if not self.queue:
            self.queue = DatabaseQueue(schema_name="message", table_name="message_table",
                                       view_name="message_view", queue_item_id_column_name="message_id",
                                       is_test_data=self.is_test_data)
        return self.queue

    @lru_cache
    def _get_message_template_ids_with_weights_by_campaign_id(self, campaign_id: int) -> list[dict]:
        """Returns a list of possible template ids from the campaign"""
        message_template_ids_with_weights = self.select_multi_dict_by_where(
            schema_name="campaign_message_template", view_table_name="campaign_message_template_view",
            select_clause_value="message_template_id, percent",
            where="campaign_id=%s AND message_template_id IS NOT NULL", params=(campaign_id,))
        return message_template_ids_with_weights

    def _get_random_weighted_message_template_id(self, campaign_id: int) -> int:
        # percent = 0.7 -> This Message Template should be sent in 70% of the cases.
        # percent = None -> equal distribution
        message_template_ids_with_weights = self._get_message_template_ids_with_weights_by_campaign_id(campaign_id)
        weights = [row["percent"] or 1 / len(message_template_ids_with_weights)
                   for row in message_template_ids_with_weights]
        message_templates = [row["message_template_id"] for row in message_template_ids_with_weights]
        random_message_template_id = random.choices(message_templates, weights=weights, k=1)[0]
        self.logger.info("Choosed random message_template_id", object={
            "random_message_template_id": random_message_template_id, "campaign_id": campaign_id,
            "message_template_ids_with_weights": message_template_ids_with_weights})
        return random_message_template_id

    def set_compound_message_after_text_template(
            self, campaign_id: int = None, message_template_id: int = None, body: str = None, subject: str = None,
            recipients: list[Recipient] = None, message_id: int = None, form_id: int = None,
            is_debug: bool = False, is_require_moderator: bool = True) -> None:
        """ Sets the compound message in the instance and in the database using the following structure:"""

        # Allow overiding instance vars
        campaign_id = campaign_id or self.campaign_id
        message_template_id = message_template_id or self.message_template_id
        body = body or self.__body
        subject = subject or self.__subject
        recipients = recipients or self.recipients or []
        message_id = message_id or self.message_id
        form_id = form_id or self.form_id
        is_debug = is_debug or self.is_debug
        is_require_moderator = is_require_moderator or self.is_require_moderator

        compound_message = {"json_version": JSON_VERSION, "data": {}}
        if message_id:
            self.message_id = message_id
            # get compound message from the db:
            compound_message_json = self.select_one_value_by_column_and_value(
                select_clause_value="compound_message_json", column_value=message_id)
            if compound_message_json is None:
                raise Exception(f"No compound_message_json found for message_id={message_id}")
            self.__compound_message = json.loads(compound_message_json)
            return

        if body:  # TODO constract textblocks_and_attributes if body is given
            textblocks_and_attributes = [{"message_template_id": message_template_id, "default_body_template": body,
                                          "default_subject_template": subject, "form_id": form_id}]

        elif form_id:  # If body is not given, get it from the database
            textblocks_and_attributes = self.message_template.get_textblocks_and_attributes_by_form_id(form_id)
        else:
            textblocks_and_attributes = None
            if campaign_id and not message_template_id:
                message_template_id = self._get_random_weighted_message_template_id(campaign_id=campaign_id)
            if message_template_id:
                textblocks_and_attributes = self.message_template.get_textblocks_and_attributes_by_message_template_id(
                    message_template_id)
        if not textblocks_and_attributes:
            raise Exception(f"No text blocks found for message_template_id={message_template_id} ("
                            f"campaign_id={campaign_id}) or form_id={form_id}")

        grouped_textblocks_and_attributes = self._get_grouped_textblocks_and_attributes(textblocks_and_attributes)
        for channel in MessageChannel:
            compound_message_json = self.create_compound_message_json(
                grouped_textblocks_and_attributes=grouped_textblocks_and_attributes, channel=channel,
                form_id=form_id, recipients=recipients, is_debug=is_debug)
            if compound_message_json:
                compound_message["data"][channel.name] = compound_message_json

        if compound_message["data"]:
            self.message_id = self.get_queue().push(data_dict={
                "compound_message_json": json.dumps(compound_message), "compound_message_json_version": JSON_VERSION,
                "is_require_moderator": is_require_moderator})

        self.__compound_message = compound_message
        self.logger.debug(object=locals())

    def get_profiles_blocks(self, text_block: dict, recipients: list[Recipient], message_template_id: int,
                            content_per_language: dict, possible_answers_per_question_id: dict) -> list[dict]:
        """Each profile block contains the following keys:
subject_locale [Optional] possible values he-il, en-us, en-gb https://www.science.co.il/language/Locale-codes.php
subject_text (aliases title/headline/question_title) [Optional]
body_locale
body_text / question_title
question_id
variable_id
default_possible_answer_id
is_visible
possible answers
    possible_answer_locale
    possible_answer_text
"""
        criteria_dict = self.message_template.get_critiria_dict(message_template_id=message_template_id)
        if criteria_dict:
            potentials_recipients = self.message_template.get_potentials_recipients(criteria_dict, recipients)
        else:
            potentials_recipients = [recipient.to_json() for recipient in recipients]

        profiles_blocks = []
        for recipient in recipients:
            profile_id = recipient.get_profile_id()
            if any(recipient.get_profile_id() == potential_recipient["profile_id"]
                   for potential_recipient in potentials_recipients):
                question_id = text_block.get("question_id")
                profile_block = {
                    "profile_id": profile_id,
                    "preferred_language": self.profile_local.get_preferred_lang_code_by_profile_id(profile_id).value,
                    "subject_per_language": {
                        lang: self._process_text_block(content, recipient)
                        for lang, content in content_per_language[question_id]["subject_per_language"].items()},
                    "body_per_language": None if question_id else {
                        lang: self._process_text_block(content, recipient)
                        for lang, content in content_per_language[question_id]["body_per_language"].items()},
                    "question_per_language": None if not question_id else {
                        lang: self._process_text_block(content, recipient) for lang, content in
                        content_per_language[question_id]["question_per_language"].items()},
                    "question_id": question_id,
                    "variable_id": text_block.get("variable_id"),
                    "default_question_possible_answer_id": text_block.get("default_question_possible_answer_id"),
                    "is_visible": text_block.get("message_template_text_block_is_visible"),
                    "is_required": text_block.get("is_required") or False,
                    "possible_answers": possible_answers_per_question_id[question_id]
                }
                if profile_block not in profiles_blocks and (profile_block["subject_per_language"] or
                                                             profile_block["body_per_language"] or
                                                             profile_block["question_per_language"]):
                    profiles_blocks.append(profile_block)
        return profiles_blocks

    @staticmethod
    def _get_grouped_textblocks_and_attributes(textblocks_and_attributes: list[dict]) \
            -> dict[int, dict[int, list[dict]]]:
        # Group the fetched data by page and message_template_id
        grouped_textblocks_and_attributes = {}
        for row in textblocks_and_attributes:
            if not row:
                continue
            page_number = row.get("form_page", row.get("message_template_text_block_seq", 1))
            message_template_id = row["message_template_id"]
            if page_number not in grouped_textblocks_and_attributes:
                grouped_textblocks_and_attributes[page_number] = {}
            if message_template_id not in grouped_textblocks_and_attributes[page_number]:
                grouped_textblocks_and_attributes[page_number][message_template_id] = []
            grouped_textblocks_and_attributes[page_number][message_template_id].append(row)
        return grouped_textblocks_and_attributes

    def create_compound_message_json(self, *, grouped_textblocks_and_attributes: dict, channel: MessageChannel,
                                     form_id: int = None, recipients: list[Recipient], is_debug: bool) -> dict or None:
        """Specs: https://docs.google.com/document/d/1UvdU9WrK7RwMNnLLBwdye9HbUzgMGEG8wsIMxxYrxa4/edit?usp=sharing
Returns dict with the following structure:
form_id = 2 [if form_id]
form_name [if form_id and debug=true]
Page[]
    page_number
    message_seq_in_page [If debug=true] - Sorted by message_seq_in_page
    Message Templates - Not need hierarchy in the JSON. Container of message_template_text_blocks
        index_number - i.e. child number (default 1)
        index_name - i.e. Home/Work (default "")
        message_template_id (i.e. 3000)
        message_template_name [If debug=true]
        MessageTemplateTextBlocks (message, question) - Not need hierarchy in the JSON
            message_template_text_block_seq [If debug=true] - Sorted by message_template_text_block_seq
            message_template_text_block_id
            message_template_text_block_name [If debug=true]
            subject_templates [If debug=true] Based on channel
            body_templates - message_template_text_block_ml.default_subject_template [If debug=true] Based on Channel
            question_templates
            question_schema
            question_uischema
            Profiles[] - Generated by message-local-python-package based on message_template_text_block_ml.default_subject_template in the relevant language/channel - Index is profile_id
                profile_id
                preferred_language
                subject_per_language = {"en": "..."}
                body_per_language = {"en": "..."} or null
                question_per_language = {"en": "..."} or null
                question_id
                variable_id
                default_question_possible_answer_id
                is_visible
                possible answers
                    possible_answer_locale
                    possible_answer_text
"""

        compound_message_json = {"Page": []}
        if form_id:
            compound_message_json["form_id"] = form_id

        # if is_debug:  TODO
        #     if form_id:
        #         compound_message_json["form_name"] = textblocks_and_attributes[0]["form_name"]

        # Iterate through the fetched data and structure it into the JSON
        for page_number, message_templates in grouped_textblocks_and_attributes.items():
            page = {
                "page_number": page_number,
                "MessageTemplates": []
            }

            for message_template_id, text_blocks in message_templates.items():
                if not text_blocks:
                    continue
                message_template_data = {
                    "message_template_id": message_template_id,
                    "MessageTemplateTextBlocks": []
                }
                if form_id:
                    message_template_data["index_number"] = list(
                        range(text_blocks[0].get("min_message_template", 0), text_blocks[0].get("max_message_template", 0) + 1)),
                    message_template_data["index_name"] = None  # will be filled by the frontend

                if is_debug:
                    message_template_data["message_template_name"] = text_blocks[0].get("message_template_name")
                    message_template_data["message_seq_in_page"] = text_blocks[0].get("form_message_seq_in_page", 1)

                # Group possible answers by question_id
                possible_answers_per_question_id = defaultdict(list)
                for text_block in text_blocks:
                    if text_block.get("possible_answer"):
                        # TODO: multiple languages
                        lang_code = text_block["question_ml_lang_code"] or LangCode.ENGLISH.value
                        possible_answers_per_question_id[text_block["question_id"]].append(
                            {lang_code: text_block["possible_answer"]})

                # Group questions by language:
                content_per_language = defaultdict(lambda: {"body_per_language": {},
                                                            "subject_per_language": {},
                                                            "question_per_language": {}})

                body_key = (channel.name.lower() + "_body") if channel != MessageChannel.EMAIL else "email_body_html"
                if f"{body_key}_template" not in text_blocks[0]:
                    return  # no special template for this channel
                field_to_lang_field = {
                    f"{body_key}_template": ("body_per_language", "message_template_text_block_ml_lang_code"),
                    f"{channel.name}_subject_template": (
                        "subject_per_language", "message_template_text_block_ml_lang_code"),
                    "question_title": ("question_per_language", "question_ml_lang_code")}

                text_blocks_by_question_id = defaultdict(list)
                for text_block in text_blocks:
                    text_blocks_by_question_id[text_block.get("question_id")].append(text_block)

                for question_id, _text_blocks in text_blocks_by_question_id.items():
                    for text_block in text_blocks:
                        for field, (lang_field, lang_code_field) in field_to_lang_field.items():
                            lang_code = text_block.get(lang_code_field) or LangCode.ENGLISH.value
                            # Note: question_id can be None
                            if text_block.get(field) and text_block.get("question_id") == question_id:
                                content_per_language[question_id][lang_field][lang_code] = text_block[field]

                # remove duplicated text_blocks
                unique_text_blocks = []
                for text_block in text_blocks:
                    columns_to_ignore = ["possible_answer"]
                    for field, (lang_field, lang_code_field) in field_to_lang_field.items():
                        columns_to_ignore.extend([field, lang_code_field])
                    unique_text_block = {k: v for k, v in text_block.items() if k not in columns_to_ignore}
                    if unique_text_block not in unique_text_blocks:
                        unique_text_blocks.append(unique_text_block)

                for text_block in unique_text_blocks:
                    text_block_data = {
                        "message_template_text_block_id": text_block.get("message_template_text_block_id"),
                        "question_schema": text_block.get("question_type_schema_attributes") or text_block.get(
                            "schema_attribute"),
                        "question_uischema": text_block.get("question_type_uischema_attributes") or text_block.get(
                            "uischema_attribute"),
                        "Profiles": self.get_profiles_blocks(text_block=text_block, recipients=recipients,
                                                             message_template_id=message_template_id,
                                                             content_per_language=content_per_language,
                                                             possible_answers_per_question_id=possible_answers_per_question_id)
                    }
                    if not text_block_data["Profiles"]:
                        continue  # There's no one to send to

                    # if channel == MessageChannel.FORM_REACTJS:
                    #     text_block_data["question_schema"] = text_block["question_type_schema_attributes"] or text_block["schema_attribute"]
                    #     text_block_data["question_uischema"] = text_block["question_type_uischema_attributes"] or text_block["uischema_attribute"]

                    if is_debug:
                        text_block_data["message_template_text_block_seq"] = text_block.get(
                            "message_template_text_block_seq", 1)
                        text_block_data["message_template_text_block_name"] = text_block.get(
                            "message_template_text_block_name")
                        text_block_data["subject_templates"] = content_per_language[text_block.get("question_id")][
                            "subject_per_language"]
                        text_block_data["body_templates"] = content_per_language[text_block.get("question_id")][
                            "body_per_language"]
                        text_block_data["question_templates"] = content_per_language[text_block.get("question_id")][
                            "question_per_language"]

                    if text_block_data not in message_template_data["MessageTemplateTextBlocks"]:
                        message_template_data["MessageTemplateTextBlocks"].append(text_block_data)

                if message_template_data["MessageTemplateTextBlocks"] and message_template_data not in page[
                    "MessageTemplates"]:
                    page["MessageTemplates"].append(message_template_data)

            if page["MessageTemplates"] and page not in compound_message_json["Page"]:
                compound_message_json["Page"].append(page)

        if not compound_message_json["Page"]:
            return None
        return compound_message_json

    def _process_text_block(self, text_block_body: str, recipient: Recipient) -> str:
        template = ReplaceFieldsWithValues(message=text_block_body,
                                           lang_code=recipient.get_preferred_lang_code(),
                                           variables=recipient.get_profile_variables())
        processed_text_block = template.get_variable_values_and_chosen_option(
            profile_id=recipient.get_profile_id(),
            # TODO: use name in the right language from person.person_ml_table
            kwargs={"to.first_name": recipient.get_first_name(),
                    "from.first_name": self.user_context.get_real_first_name(),
                    "message_id": self.message_id
                    })
        return processed_text_block

    def get_compound_message_dict(self, channel: MessageChannel = None) -> dict:
        if channel is None:
            return self.__compound_message["data"]
        else:
            compound_message_dict = {channel.name: self.__compound_message["data"].get(channel.name, {})}
            if channel != MessageChannel.DEFAULT:
                compound_message_dict["DEFAULT"] = self.__compound_message["data"].get("DEFAULT", {})
            return compound_message_dict

    def get_compound_message_str(self, channel: MessageChannel = None) -> str:
        return json.dumps(self.get_compound_message_dict(channel=channel))

    def get_profile_blocks(self, profile_id: int, channel: MessageChannel) -> list[dict]:
        compound_message_dict = self.get_compound_message_dict(channel=channel)
        if "Page" not in compound_message_dict[channel.name]:
            channel = MessageChannel.DEFAULT

        profile_blocks = []
        for page in compound_message_dict[channel.name].get("Page", {}):
            for message_template in page.get("MessageTemplates", {}):
                for text_block in message_template.get("MessageTemplateTextBlocks", {}):
                    for profile_block in text_block.get("Profiles", {}):
                        if profile_block["profile_id"] == profile_id and profile_block not in profile_blocks:
                            profile_blocks.append(profile_block)
        return profile_blocks

    def get_message_fields(self) -> dict:
        # Used by dialog workflow
        if self.recipients:
            recipients_mapping = {recipient.get_profile_id(): recipient.to_json() for recipient in self.recipients}
        else:
            recipients_mapping = {}
        return {
            "campaign_id": self.campaign_id,
            "body": self.__body,
            "subject": self.__subject,
            "message_id": self.message_id,
            "ui_schema": self.ui_schema,
            "schema": self.schema,
            "field_id": self.field_id,
            "recipients": recipients_mapping,
            "json_version": JSON_VERSION,
        }
