import re
from dotenv import load_dotenv
from logger_local.Logger import Logger
from python_sdk_remote.utilities import remove_digits
from .people_constants import PeopleLocalConstants
from group_local.group_local_constants import GroupLocalConstants
from database_mysql_local.generic_crud import GenericCRUD
load_dotenv()


logger = Logger.create_logger(
    object=PeopleLocalConstants.PEOPLE_LOCAL_PYTHON_PACKAGE_CODE_LOGGER_OBJECT)


# TODO: When fields such as firstname, lastname, organization, job_title, group_name, city ... contains "?" then is_sure=false
# TODO Should person, profile, contact and user inherit PeopleLocal or not?
class PeopleLocal():
    def __init__(self, first_name_original: str = None, last_names_original: list = None,
                 organizations_names_original: list = None, email_addresses: list = None, urls: list = None):
        logger.start(
            object={
                'first_name_original': first_name_original, 'last_names_original': last_names_original,
                'organizations_names_original': organizations_names_original,
                'email_addresses': email_addresses, 'urls': urls}
        )
        self.first_name_original = first_name_original
        self.last_names_original = last_names_original
        self.normalized_first_name = None
        self.normalized_last_names = []
        self.organizations_names_original = organizations_names_original or []
        self.organizations_names_short = []
        self.email_addresses = email_addresses or []
        self.urls = urls or []
        self.__extract_first_name_from_email_address()
        self.__extract_organization_str_from_email_addresses_str()
        self.__extract_organization_strs_from_urls_str()
        self.__extract_organizations_names_short_from_organizations_names_original()
        self.normalize_names()
        logger.end()

    def _process_first_name_str(self, add_people_to_a_group_function, **kwargs) -> str:
        logger.start()
        if not self.normalized_first_name:
            logger.warning(log_message="normalized_first_name is None")
            return None
        try:
            logger.info("normalized_first_name", object={
                        'normalized_first_name': self.normalized_first_name})
            kwargs['groups'] = [self.normalized_first_name]
            if "?" in self.normalized_first_name:
                kwargs["mapping_data_json"] = {
                    "is_sure": False
                }
            result = add_people_to_a_group_function(**kwargs)
        except Exception as exception:
            logger.error("error processing first name", object={
                         'self.first_name_original': self.first_name_original, 'error': exception})
            raise exception

        # TODO Please use GenericCrudMl to update person.first_name_table

        # TODO Create group to all people with the same first name and add this contact/profile to the group

        logger.end("success processing first name",
                   object={'result': result})
        return result

    def _process_last_names_str(self, add_people_to_a_group_function, **kwargs) -> list:
        # TODO logger.start() should include all parameters - Please update all add_people_to_a_group_functions.
        logger.start()
        results = []
        for normalized_last_name in self.normalized_last_names:
            try:
                logger.info("normalized_last_name", object={
                            'normalized_last_name': normalized_last_name})
                kwargs['groups'] = [normalized_last_name]
                if "?" in normalized_last_name:
                    kwargs["mapping_data_json"] = {
                        "is_sure": False
                    }
                result = add_people_to_a_group_function(**kwargs)
                results.append(result)
            except Exception as exception:
                logger.error("error processing last name", object={
                            'normalized_last_name': normalized_last_name, 'error': exception})
                raise exception
        logger.end("success processing last name",
                   object={'results': results})

        # TODO Create a group to the family and add this contact/profile to the group

        return results

    def _process_organizations_str(self, add_people_to_a_group_function, **kwargs) -> list:
        logger.start()
        results = []
        for organization_name in self.organizations_names_original:
            try:
                kwargs['groups'] = [organization_name]
                # TODO: if there's "Ventures" in the organization name, shall we add
                # GroupLocalConstants.VENTURE_CAPITAL_GROUP_ID as parent_group_id
                # to all groups in self.organizations_names_original?
                if "Ventures" in organization_name:
                    kwargs['parent_group_id'] = GroupLocalConstants.VENTURE_CAPITAL_GROUP_ID
                if "?" in organization_name:
                    kwargs["mapping_data_json"] = {
                        "is_sure": False
                    }
                result = add_people_to_a_group_function(**kwargs)
                results.append(result)
            except Exception as exception:
                logger.error("error processing organization", object={
                            'organization_name': organization_name, 'error': exception})
                raise exception
        logger.end("success processing organization",
                   object={'result': result})
        return results

    # TODO: is this supposed to call methods like link_contact_to_domain in DomainLocal?
    # def _process_urls_str(self, link_people_to_domain_function, **kwargs):
    def __extract_organization_str_from_email_addresses_str(self):
        logger.start()
        if self.email_addresses == []:
            logger.warning(log_message="email address is None")
            return []
        for email_address in self.email_addresses:
            domain_part = email_address.split('@')[-1]
            organization_name_parts = domain_part.rsplit('.', 1)[0]
            organization_name = ' '.join(part for part in organization_name_parts.split('.'))
            self.organizations_names_original = self.__append_if_not_exists(
                lst=self.organizations_names_original, item=organization_name.capitalize()
            )
        logger.end(object={'organizations_names_original': self.organizations_names_original})

    #  organizations_names_short is organizations_names_original without "Ltd", "Inc" ...
    def __extract_organizations_names_short_from_organizations_names_original(self):
        logger.start()
        if self.organizations_names_original == []:
            logger.warning(log_message="organizations_names_original is None")
            return []
        organizations_names_short = []
        for organization_name in self.organizations_names_original:
            pattern = re.compile(r'\b(?:Ltd|Inc|Corporation|Corp|LLC|L.L.C.|GmbH|AG|S.A.|SARL)\b\.?', re.IGNORECASE)
            short_organization_name = re.sub(pattern, '', organization_name).strip()
            short_organization_name = re.sub(r',\s*$', '', short_organization_name).strip()
            self.organizations_names_short = self.__append_if_not_exists(
                lst=self.organizations_names_short, item=short_organization_name
            )
        logger.end(object={'organizations_names_short': organizations_names_short})

    def __extract_organization_strs_from_urls_str(self):
        logger.start(object={'urls': self.urls})
        if self.urls == []:
            logger.warning(log_message="urls are empty")
            return []
        for url in self.urls:
            if url is None:
                continue
            stripped_url = url.replace('http://', '').replace('https://', '').replace('www.', '')
            organization_name = stripped_url.split('.')[0]
            organization_name_capitalized = organization_name.capitalize()
            self.organizations_names_original = self.__append_if_not_exists(
                lst=self.organizations_names_original, item=organization_name_capitalized
            )
        logger.end(object={'organizations_names_original': self.organizations_names_original})

    def __extract_first_name_from_email_address(self):
        logger.start()
        if self.email_addresses == []:
            logger.warning(log_message="email addresses are empty")
            return []
        email_address = self.email_addresses[0]
        local_part = email_address.split('@')[0]

        for separator in ['.', '_']:
            if separator in local_part:
                first_name = local_part.split(separator)[0]
                break
        else:
            first_name = local_part

        logger.end(object={'first_name': first_name})
        self.first_name_original = first_name.capitalize()

    def normalize_names(self):
        logger.start()
        if self.first_name_original:
            self.normalized_first_name = remove_digits(self.first_name_original)
            self.normalized_first_name = self.normalized_first_name.split()[0]
        if self.last_names_original:
            for last_name in self.last_names_original:
                normalized_last_name = remove_digits(last_name)
                normalized_last_name = normalized_last_name.split()[0]
                self.normalized_last_names.append(normalized_last_name)
        logger.end()

    # TODO: Shall we move this to python-sdk-remote?
    def __append_if_not_exists(self, lst: list, item: str) -> list:
        if item not in lst:
            lst.append(item)
        return lst

    # TODO: Complete this method
    def get_people_id(self, people_entity_name: str, ids_dict: dict) -> int:
        METHOD_NAME = "get_people_id"
        logger.start(log_message=METHOD_NAME, object={'people_entity_name': people_entity_name, 'ids_dict': ids_dict})
        if people_entity_name == "person":
            if ids_dict.get("contact_id"):
                contact_id = ids_dict.get("contact_id")
                person_id = self.__get_person_id_from_contact_details(
                    people_entity_name=people_entity_name, contact_id=contact_id)
                logger.end(object={'person_id': person_id})
                return person_id
        logger.end(object={'people_id': None})
        return None

    # TODO: Complete this method
    def __get_person_id_from_contact_details(self, people_entity_name: str, contact_id: int) -> int:
        METHOD_NAME = "__get_person_id_from_contact_id"
        logger.start(log_message=METHOD_NAME, object={'people_entity_name': people_entity_name, 'contact_id': contact_id})
        crud_instance = GenericCRUD()
        person_id = None
        # Try to get person_id from contact_person_table
        person_id = crud_instance.select_one_value_by_id(
            schema_name="contact_person",
            table_name="contact_person_table",
            select_clause_value="person_id",
            column_name="contact_id",
            column_value=contact_id
        )
        if person_id is None:
            # Try to get 3 email_address_ids from contact_email_address_table
            email_address_ids = crud_instance.select_multi_value_by_id(
                schema_name="contact_email_address",
                table_name="contact_email_address_table",
                select_clause_value="email_address_id",
                column_name="contact_id",
                column_value=contact_id,
                limit=3,
                order_by="email_address_id DESC",
                skip_null_values=True
            )
            # Try to get person_id from email_address_person_table
            for email_address_id in email_address_ids:
                # TODO: insert to email_address_person_table when inserting a new contact (or/and person?)
                '''
                person_id = crud_instance.select_one_value_by_id(
                    schema_name="email_address_person",
                    table_name="email_address_person_table",
                    select_clause_value="person_id",
                    column_name="email_address_id",
                    column_value=email_address_id
                )
                '''
                if person_id is None:
                    # Try to get person_id from person_table
                    person_id = crud_instance.select_one_value_by_id(
                        schema_name="person",
                        table_name="person_table",
                        select_clause_value="person_id",
                        column_name="main_email_person",
                        column_value=email_address_id
                    )
                if person_id:
                    break
        if person_id is None:
            # Try to get 3 phone_ids from contact_phone_table
            phone_ids = crud_instance.select_multi_value_by_id(
                schema_name="contact_phone",
                table_name="contact_phone_table",
                select_clause_value="phone_id",
                column_name="contact_id",
                column_value=contact_id,
                limit=3,
                order_by="phone_id DESC",
                skip_null_values=True
            )
            # Try to get person_id from person_phone_table
            for phone_id in phone_ids:
                # TODO: insert to person_phone_table when inserting a new contact
                '''
                person_id = crud_instance.select_one_value_by_id(
                    schema_name="person_phone",
                    table_name="person_phone_table",
                    select_clause_value="person_id",
                    column_name="phone_id",
                    column_value=phone_id
                )
                if person_id:
                    break
                '''
