from typing import List, Tuple

from circles_local_database_python.generic_mapping import GenericMapping
from dotenv import load_dotenv
# TODO from group_remote.groups_remote
from group_remote.group_remote import GroupsRemote
from phone_local.phones_local import PhonesLocal

# TODO Can we avoid the src.
from src.CSVToContactPersonProfile import logger

load_dotenv()


# TODO def process_email_address( email_address: str)
#          """ Returned email_address_id, domain_name, organization_name """
#           DomainsLocal.link_contact_to_domain( contact_id, domain_name )

# TODO def process_organization( organization_name: str, email_address: str) -> str: (move to people-local-python-package
#     if organization_name == None or empty
#          organization_name = extract_organization_from_email_address( email_address)
#     normalized_organization_name = GroupsLocal.add_update_group_and_link_to_contact( organization_name, is_organization=true) # When checking if the organization exists, remove suffix such as Ltd, Inc, בעמ... when searching ignore the uppper-case lower-case

# TODO def process_department( department_name: str) -> str: (move to people-local-python-package
#     normalized_department_name = GroupsLocal.add_update_group_and_link_to_contact( department_name, is_department=true) # When searching ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_continent( continent_name: str) -> str: (move to people-local-python-package)
#     continent_id, normalized_continent_name = GroupsLocal.add_update_group_and_link_to_contact( continent_name, is_continent=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_country( country_name: str) -> str: (move to people-local-python-package)
#     country_id, normalized_country_name = GroupsLocal.add_update_group_and_link_to_contact( country_name, is_country=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_state( state_name: str) -> str: (move to people-local-python-package)
#     state_id, normalized_state_name = GroupsLocal.add_update_group_and_link_to_contact( state_name, is_state=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_county_in_state( county_in_state_name_id: id) -> str: (move to people-local-python-package)
#     country_id, normalized_county_name = GroupsLocal.add_update_group_and_link_to_contact( county_in_state_id, is_county=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_region( region_name: str) -> str: (move to people-local-python-package)
#     region_id, normalized_region_name = GroupsLocal.add_update_group_and_link_to_contact( region_name, is_region=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_neighbourhood_in_city( neighbourhood_in_city_id: str) -> str: (move to people-local-python-package)
#     neighbourhood_id, normalized_neighbourhood_name = GroupsLocal.add_update_group_and_link_to_contact( neighbourhood_in_city_id, is_neighbourhood=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_street_in_city( street_in_city_id: int) -> str: (move to people-local-python-package)
#     street_id, normalized_street_name = GroupsLocal.add_update_group_and_link_to_contact( street_in_city_id, is_street=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_building_in_street( location_id: int) -> str: (move to people-local-python-package)
#     location_id, normalized_building_address_name = GroupsLocal.add_update_group_and_link_to_contact( location_id, is_street=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_website

# TODO def process_first_name( original_first_name: str) -> str: (move to people-local-python-package)
#     normilized_first_name = the first word in original_first_name
#     GroupsLocal.add_update_group_and_link_to_contact( normilized_first_name, is_group=true, contact_id) # When checking if exists, ignore the upper-case lower-case
#     return normilized_first_name

def process_first_name(original_first_name: str) -> str:
    logger.start(object={'original_first_name': original_first_name})
    first_name = ''.join([i for i in original_first_name if not i.isdigit()])
    logger.end("success processing first name",
               object={'first_name': first_name})
    return first_name


def process_last_name(original_last_name: str) -> str:
    logger.start(object={'original_last_name': original_last_name})
    last_name = ''.join([i for i in original_last_name if not i.isdigit()])
    logger.end("success processing last name",
               object={'last_name': last_name})
    return last_name


def process_phone(original_phone_number: str) -> dict:
    logger.start(object={'original_phone_number': original_phone_number})
    phone_local_instance = PhonesLocal()
    generic_mapping_instance = GenericMapping(
        default_schema_name='location_profile')
    profile_id = logger.user_context.get_effective_profile_id()
    location_id = generic_mapping_instance.select_one_tuple_by_id(view_table_name='location_profile_view',
                                                                  select_clause_value='location_id',
                                                                  id_column_name='profile_id',
                                                                  id_column_value=profile_id)[0]
    if location_id is None:
        logger.error(
            f"profile {profile_id} location is not set phone number will cannot normalized")
        return None
    generic_mapping_instance.set_schema(schema_name='location')
    country_id = \
    generic_mapping_instance.select_one_tuple_by_id(view_table_name='location_view', select_clause_value='country_id',
                                                    id_column_name='location_id', id_column_value=location_id)[0]
    country_iso_code = \
    generic_mapping_instance.select_one_tuple_by_id(view_table_name='country_ml_view', select_clause_value='iso',
                                                    id_column_name='country_id', id_column_value=country_id)[0]
    normalized_phone_number = phone_local_instance.normalize_phone_number(
        original_number=original_phone_number, region=country_iso_code)
    phone_data = {
        'number_original': original_phone_number,
        'international_code': normalized_phone_number['international_code'],
        'full_number_normalized': normalized_phone_number['full_number_normalized'],
        'local_number_normalized': int(str(normalized_phone_number['full_number_normalized'])
                                       .replace(str(normalized_phone_number['international_code']), '')),
        'created_user_id': logger.user_context.get_effective_user_id(),
    }
    generic_mapping_instance.set_schema(schema_name='phone')
    phone_id = generic_mapping_instance.insert(
        table_name='phone_table', data_json=phone_data)

    generic_mapping_instance.set_schema(schema_name='phone_profile')
    # link phone to profile
    phone_profile_id = generic_mapping_instance.insert_mapping(
        entity_name1='phone', entity_name2='profile', entity_id1=phone_id, entity_id2=profile_id)
    result = {
        'phone_profile_id': phone_profile_id,
        'phone_id': phone_id,
        'normalized_phone_number': normalized_phone_number,
        'original_phone_number': original_phone_number
    }
    logger.end("success processing phone number", object=result)
    return result


def process_job_title(contact_id: int, job_title: str) -> List[Tuple[int, str]]:
    """
    Process the job title for a contact by checking if related groups exist and linking them.

    Args:
    - contact_id (int): The ID of the contact.
    - job_title (str): The job title associated with the contact.

    Returns:
    - List[Tuple[int, str]]: A list of tuples containing linked group IDs and titles.
    """
    if job_title is None:
        return []
    # Creating an instance of GenericMapping
    generec_mapping = GenericMapping(
        default_entity_name1='contact', default_entity_name2='group', default_schema_name='contact_group')

    # Retrieving all group names
    groups_names = get_all_groups_names()

    # Initializing lists to store groups to link and groups that are successfully linked
    groups_to_link = []
    groups_linked = []

    # Iterating through group names to find matching groups based on job_title
    for group in groups_names:
        if group is None:
            continue
        if job_title in group:
            groups_to_link.append(group)

    # If no matching groups found based on job_title
    if len(groups_to_link) == 0:
        # Creating a new group with the job_title
        title = job_title
        # TODO Why do we need the 1st parameter?
        group_id = GroupsRemote.create_group(GroupsRemote(), title=title,
                                             titleLangCode=logger.user_context.get_effective_profile_preferred_lang_code(),
                                             isInterest=True)
        # Inserting mapping between contact and the newly created group
        GenericMapping.insert_mapping(GenericMapping(), 'contact', 'group', contact_id, group_id)
        groups_linked.append((group_id, title))
    else:
        # Linking contact with existing groups found based on job_title
        for group in groups_to_link:
            group_id = GroupsRemote.get_group_by_group_name(
                GroupsRemote(), groupName=group).json()['data'][0]['id']
            generec_mapping.insert_mapping(
                'contact', 'group', contact_id, group_id)
            groups_linked.append((group_id, group))

    # Logging the success of processing job title and returning linked group IDs and titles
    logger.end("success processing job title", object={
        #TODO Please add a suffix to all relevant variables i.e. groups_linked
        'groups_linked': groups_linked})
    return groups_linked


def get_all_groups_names():
    group_remote = GroupsRemote()
    groups = group_remote.get_all_groups().json()
    groups_names = []
    for group in groups['data']:
        groups_names.append(group['title'])
    return groups_names
