"""imports"""
from datetime import datetime
from typing import List

from database_mysql_local.generic_crud_ml import GenericCRUDML
from logger_local.MetaLogger import MetaLogger
from message_local.MessageImportance import MessageImportance
from message_local.MessageTemplates import MessageTemplates
from message_local.Recipient import Recipient
from messages_local.MessagesLocal import MessagesLocal

from .constants import MESSAGE_SEND_PLATFORM_INVITATION_CODE_LOGGER_OBJECT

DEFAULT_MINIMAL_DAYS = 3


class CampaignMessageSend(GenericCRUDML, metaclass=MetaLogger,
                          object=MESSAGE_SEND_PLATFORM_INVITATION_CODE_LOGGER_OBJECT):
    """Message send platform class"""

    def __init__(self) -> None:
        super().__init__(default_schema_name="message")
        self.message_template = MessageTemplates()
        self.messages_local = MessagesLocal()

    def __get_potential_recipient_list_by_campaign_id_limit(
            self, campaign_id: int, recipient_limit: int = 100) -> List[Recipient]:
        """return list of person id """

        recipient_limit_left = recipient_limit

        query_for_relevant_criteria_for_campaign = """
            SELECT criteria.min_age, criteria.max_age, 
                criteria.gender_list_id, criteria.group_list_id,
                campaign.minimal_days_between_messages_to_the_same_recipient
            FROM campaign.campaign_view AS campaign
               JOIN campaign_criteria.campaign_criteria_view AS campaign_criteria
                   ON campaign_criteria.campaign_id=campaign.campaign_id
               JOIN criteria.criteria_view AS criteria
                   ON criteria.criteria_id = campaign_criteria.criteria_id
            WHERE campaign.campaign_id = %s
        """

        self.cursor.execute(query_for_relevant_criteria_for_campaign, (campaign_id,))
        results = []
        for row in self.cursor.fetchall():
            min_age, max_age, gender_list_id, group_list_id, minimal_days = row
            minimal_days = minimal_days or DEFAULT_MINIMAL_DAYS
            # profile_id didn't receive messages from this campaign for campaign.minimal_days
            criteria_dict = {"min_age": min_age, "max_age": max_age, "gender_list_id": gender_list_id,
                             "group_list_id": group_list_id, "minimal_days": minimal_days}
            self.logger.info(object=criteria_dict)
            where = self.message_template.get_where_by_criteria_json(criteria_dict)
            where += (""" AND user.profile_id NOT IN (
                       SELECT user.profile_id FROM message.message_outbox_view 
                           WHERE campaign_id = %s AND updated_timestamp >= NOW() - INTERVAL %s DAY
                       )"""
                      )

            # Possible columns: person_id, person_is_approved, person_main_email_address, user_main_email_address,
            # username, user_id, user_is_approved, user_is_test_data, profile_preferred_lang_code, profile_gender_id,
            # user_first_name, user_last_name, user_created_timestamp, profile_id, brand_id, user_active_location_id,
            # user_active_location_country_name, subscription_id, subscription_title, user_stars, profile_stars,
            # person_birthday_date, profile_phone_full_number_normalized, role_name, group_profile_id, group_id,
            # profile_id, relationship_type_id, is_sure, group_profile_type_id, supplier_category_id,
            # consumer_category_id, participant_category_id, months, start_date_day, start_date_month, start_date_year,
            # start_circa, end_date_day, end_date_month, end_date_year, end_circa, identifier, is_test_data, rank,
            # text_block_id, is_recommended, is_request_by_the_user, is_approved_by_group_admin
            query_for_potentials_receipients = f"""
                SELECT DISTINCT user_first_name, user_id, person_id, user_main_email_address, user.profile_id, 
                   profile_phone_full_number_normalized, profile_preferred_lang_code
                 FROM user.user_general_view AS user
                    JOIN group_profile.group_profile_table AS group_profile 
                        on group_profile.profile_id = user.profile_id
                  WHERE {where} LIMIT {recipient_limit_left}
                """
            self.logger.info(object={"query_for_potentials_receipients": query_for_potentials_receipients,
                                     "campaign_id": campaign_id, "minimal_days": minimal_days})

            self.cursor.execute(query_for_potentials_receipients, (campaign_id, minimal_days))

            recieved_results = self.cursor.fetchall()
            for (first_name, user_id, person_id, user_main_email_address, profile_id,
                 profile_phone_full_number_normalized, profile_preferred_lang_code) in recieved_results:
                recipient = Recipient(user_id=user_id, person_id=person_id, email_address_str=user_main_email_address,
                                      profile_id=profile_id, telephone_number=profile_phone_full_number_normalized,
                                      preferred_lang_code_str=profile_preferred_lang_code, first_name=first_name)
                results.append(recipient)
                self.logger.info(object={"recipient": recipient})

            recipient_limit_left -= len(recieved_results)

        return results

    def __get_number_of_invitations_sent_in_the_last_24_hours(self, campaign_id: int) -> int:
        """return number of invitations"""
        self.logger.start(
            f"get number of invitations sent in the last 24_hours for campaign id={campaign_id}")
        query = """
            SELECT COUNT(*) FROM message.message_outbox_view 
            WHERE campaign_id = %s 
               AND return_code = 0   -- success
               AND updated_timestamp >= NOW() - INTERVAL 24 HOUR  -- updated in the last 24 hours
               LIMIT 1
            """

        self.cursor.execute(query, (campaign_id,))
        number_of_invitations_tuple = self.cursor.fetchone()
        number_of_invitation = number_of_invitations_tuple[0]  # can be 0

        return number_of_invitation

    def __get_number_of_invitations_to_send_by_campain_id_multiplier(
            self, campaign_id: int, additional_invitations_multiplier: float = 1.01,
            additional_invitations_amount: int = 1) -> int:
        """get number to send after multiplier"""

        invitations_sent_in_the_last_24_hours = self.__get_number_of_invitations_sent_in_the_last_24_hours(campaign_id)
        number_of_invitations_to_send = int(invitations_sent_in_the_last_24_hours * additional_invitations_multiplier +
                                            additional_invitations_amount)
        return number_of_invitations_to_send

    def send_message_by_campaign_id(
            self, *, campaign_id: int, additional_invitations_multiplier: float = 1.01,
            additional_invitations_amount: int = 1, request_datetime: datetime = None,
            requested_message_type: int = None, importance: MessageImportance = None) -> list[int]:

        recipient_limit = self.__get_number_of_invitations_to_send_by_campain_id_multiplier(
            campaign_id=campaign_id,
            additional_invitations_multiplier=additional_invitations_multiplier,
            additional_invitations_amount=additional_invitations_amount)
        recipient_list = self.__get_potential_recipient_list_by_campaign_id_limit(campaign_id, recipient_limit)
        if not recipient_list:
            return []
        self.logger.info(object={"recipient_list": recipient_list})
        # query = """
        #     SELECT campaign_table.message_template_id, message_template.message_template_ml_table.sms_body_template
        #     FROM campaign.campaign_table JOIN message_template.message_template_ml_table
        #         ON campaign_table.message_template_id = message_template_ml_table.message_template_id
        #     WHERE campaign_table.campaign_id = %s
        # """
        # self.cursor.execute(query, (campaign_id,))
        # text_template = self.cursor.fetchall()
        #  we have to call the constructor every time, as the work related to body/recipients is done there,
        #  and we have new body & recipients per campaign

        # message_dict contains a list of dicts, each with the following keys:
        # ["sms_body_template", "email_subject_template", "email_body_html_template",
        # "whatsapp_body_template", "question_id", "question_type_id", "question_title", "question_type_name"]

        message_ids = self.messages_local.send_scheduled(
            recipients=recipient_list,
            request_datetime=request_datetime,
            importance=importance,
            campaign_id=campaign_id,
            # TODO: message_template_id=message_template_id,
            requested_message_type=requested_message_type
        )

        return message_ids

    def send_to_all_campaigns(self, additional_invitations_multiplier: float = 1.01,
                              additional_invitations_amount: int = 1) -> None:
        """send to all campaigns"""

        self.cursor.execute("SELECT campaign_id FROM campaign.campaign_view WHERE NOW() >= start_timestamp "
                            "AND (end_timestamp IS NULL OR NOW() <= end_timestamp)")
        campaign_ids_list_of_tuples = self.cursor.fetchall()
        self.logger.info(object={"campaign_ids_list_of_tuples": campaign_ids_list_of_tuples})
        for campaign_id_tuple in campaign_ids_list_of_tuples:
            self.send_message_by_campaign_id(campaign_id=campaign_id_tuple[0],
                                             additional_invitations_multiplier=additional_invitations_multiplier,
                                             additional_invitations_amount=additional_invitations_amount)
