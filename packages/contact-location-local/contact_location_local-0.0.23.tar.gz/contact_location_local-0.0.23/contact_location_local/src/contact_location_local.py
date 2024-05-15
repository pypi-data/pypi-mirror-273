import phonenumbers
import pycountry
from database_mysql_local.generic_mapping import GenericMapping
from database_mysql_local.point import Point
from group_local.group_local import GroupLocal
from language_remote.lang_code import LangCode
from location_local.city import City
from location_local.country import Country
from location_local.county import County
from location_local.location_local_constants import LocationLocalConstants
from location_local.locations_local_crud import LocationsLocal
from location_local.neighborhood import Neighborhood
from location_local.region import Region
from location_local.state import State
from logger_local.LoggerLocal import Logger
from user_context_remote.user_context import UserContext

from .contact_location_local_constants import CONTACT_LOCATION_PYTHON_PACKAGE_CODE_LOGGER_OBJECT

DEFAULT_SCHEMA_NAME = "contact_location"
DEFAULT_ENTITY_NAME1 = "contact"
DEFAULT_ENTITY_NAME2 = "location"
DEFAULT_ID_COLUMN_NAME = "contact_location_id"
DEFAULT_TABLE_NAME = "contact_location_table"
DEFAULT_VIEW_TABLE_NAME = "contact_location_view"
# TODO Move those to group_category.py in group-local-python-package, we'll generate this file using sql2code
# TODO develop file group_category.py in group-local-python-package
STATE_THEY_LIVE_IN_GROUP_CATEGORY = 501
CITY_THEY_LIVE_IN_GROUP_CATEGORY = 201
DEFAULT_COORDINATE = Point(0, 0)
logger = Logger.create_logger(
    object=CONTACT_LOCATION_PYTHON_PACKAGE_CODE_LOGGER_OBJECT)

user_context = UserContext.login_using_user_identification_and_password()


class ContactLocationLocal(GenericMapping):
    def __init__(self, default_schema_name: str = DEFAULT_SCHEMA_NAME, default_entity_name1: str = DEFAULT_ENTITY_NAME1,
                 default_entity_name2: str = DEFAULT_ENTITY_NAME2, default_id_column_name: str = DEFAULT_ID_COLUMN_NAME,
                 default_table_name: str = DEFAULT_TABLE_NAME, default_view_table_name: str = DEFAULT_VIEW_TABLE_NAME,
                 lang_code: LangCode = None, is_test_data: bool = False) -> None:

        GenericMapping.__init__(
            self, default_schema_name=default_schema_name, default_entity_name1=default_entity_name1,
            default_entity_name2=default_entity_name2, default_id_column_name=default_id_column_name,
            default_table_name=default_table_name, default_view_table_name=default_view_table_name,
            is_test_data=is_test_data)
        self.locations_local = LocationsLocal()
        self.country = Country()
        self.county = County()
        self.state = State()
        self.city = City()
        self.region = Region()
        self.neighborhood = Neighborhood()
        self.group_local = GroupLocal(is_test_data=is_test_data)

        # TODO: is self.lang_code still needed?
        self.lang_code = lang_code or user_context.get_effective_profile_preferred_lang_code()
        self.is_test_data = is_test_data
        self.profile_id = user_context.get_effective_profile_id()

    def insert_contact_and_link_to_location(self, location_dict: dict, contact_id: int) -> dict:
        """
        Process city information create city group if not exist and add city to city group
        and linking the contact to the city
        :param location_dict: location information: dict
        keys:
        - coordinate : Point
        - city : dict
        - state : dict
        - country : dict
        - region : dict
        - neighborhood : dict
        :param contact_id: contact id

        """
        logger.start("process_location", object={
            'location_dict': location_dict, 'contact_id': contact_id})
        if not location_dict or not contact_id:
            # TODO: Check if you can raise an exception here and then run google-contact-local tests
            # TODO: and contact-csv-import tests
            logger.warning("location_dict or contact_id is None",
                           object={"location_dict": location_dict, "contact_id": contact_id})
            return None
        city_name = location_dict.get('city')
        state_name = location_dict.get('state')
        county_name = location_dict.get('county')
        country_name = location_dict.get('country')
        region_name = location_dict.get('region')
        neighborhood_name = location_dict.get('neighborhood')
        coordinate = location_dict.get('coordinate')

        # insert to database temporary ignore duplicate entry exception
        try:
            country_id, country_data = self.__process_country(country_name=country_name, coordinate=coordinate)

            state_id = self.__process_state(state_name=state_name)

            city_id = self.__process_city(
                city_name=city_name, state_id=state_id, coordinate=coordinate)

            county_id = self.__process_county(
                county_name=county_name, state_id=state_id, coordinate=coordinate)

            region_id = self.__process_region(
                region_name=region_name, country_id=country_id, coordinate=coordinate)

            neighborhood_id = self.__process_neighborhood(
                neighborhood_name=neighborhood_name, city_id=city_id, coordinate=coordinate)

            location_info = {
                'coordinate': coordinate or DEFAULT_COORDINATE,
                'city_id': city_id,
                'state_id': state_id,
                'county_id': county_id,
                'country_id': country_id,
                'region_id': region_id,
                'neighborhood_id': neighborhood_id,
                'address_local_language': location_dict.get('address_local_language'),
                # TODO: Shall we translate the address to Enlgish and add to address_english?
                'postal_code': location_dict.get('postal_code'),
                'visibility_id': 1,
                'is_approved': False,
            }

            if country_data:
                location_info['plus_code'] = country_data.get("plus_code")
            else:
                location_info['plus_code'] = LocationLocalConstants.DEFAULT_PLUS_CODE

            '''
            # old code
            location_id = self.locations_local.insert(data=location_info,
                                                      lang_code=self.lang_code,
                                                      is_test_data=self.is_test_data)
            '''
            # We don't need to call self.locations_local.insert here
            # because we already processed the location information
            # If we use self.locations_local.insert we lose information
            # and the ids fields in location_table new rows are missing
            location_id = self.insert(
                schema_name="location",
                table_name="location_table",
                data_dict=location_info)

            contact_location_id = self.insert_mapping(schema_name='contact_location',
                                                      entity_name1=self.default_entity_name1,
                                                      entity_name2=self.default_entity_name2,
                                                      entity_id1=contact_id,
                                                      entity_id2=location_id,
                                                      data_dict={'contact_id': contact_id, 'location_id': location_id})
            location_result = {
                'location_id': location_id,
                'contact_location_id': contact_location_id,
            }
            logger.end(log_message="location successfully processed",
                       object={"location_result": location_result})
            return location_result
        except Exception as e:
            logger.exception("error in process_location" + str(e))
            raise e

    # TODO Should this method be here or in location package?
    def get_country_information(self, country_name: str) -> dict:
        """
        Get country information by country name
        :param country_name: The country name
        :return: country information: dict
        example:
        {
            "alpha_2(iso2)": "IL",  :str
            "name": "Israel", :str
            "alpha_3(iso3)": "ISR", :str
            "flag": "🇮🇱", :str
            "numeric": 376, :str
            "plus_code": 972 :int
        }
        """
        try:
            if not self.__validate_method_arguments(country_name):
                logger.warning("country_name is None", object={"country_name": country_name})
                return None
            if country_name is None:
                raise ValueError("country_name is None")
            country = pycountry.countries.get(
                name=country_name).__dict__.get('_fields')
            if country:
                country_alpha_2 = country.get('alpha_2')
                country_code = phonenumbers.COUNTRY_CODE_TO_REGION_CODE.keys()
                for code in country_code:
                    if country_alpha_2 in phonenumbers.COUNTRY_CODE_TO_REGION_CODE[code]:
                        country['plus_code'] = code
                        break
                return country
        except Exception as exception:
            logger.exception("error in get_country_information" + str(exception))
            logger.exception(str(exception))
            raise exception
        return {}

    def __process_country(self, country_name: str, coordinate: Point) -> (int, dict):
        """
        Process country information
        :param country_name: country name
        :param coordinate: coordinate
        :return: country_id: int, country_data: dict
        """
        if not self.__validate_method_arguments(country_name, coordinate):
            logger.warning("country_name or coordinate is None",
                           object={"country_name": country_name, "coordinate": coordinate})
            return None, None
        country_id = self.country.get_country_id_by_country_name(country_name=country_name)
        if country_id is None:
            # Sometimes we get the country name as ISO, for example from GoogleContactsCSV
            country_id = self.country.select_one_value_by_id(
                view_table_name="country_ml_view",
                select_clause_value='country_id',
                column_name="iso", column_value=country_name)
        if country_id is None:
            # I commented this since I don't think we want to add new countries to the database
            # by this method
            # TODO: Shall we delete the following comment?
            '''
            country_information = self.get_country_information(
                country_name=country_name)
            country_data = {
                'coordinate': coordinate,
                'iso': country_information.get("alpha_2"),
                'name': country_name,
                'iso3': country_information.get("alpha_3"),
                'numcode': country_information.get("numeric"),
                'phonecode': country_information.get("plus_code"),
            }
            country_lang_code = LangCode.detect_lang_code(text=country_name)
            if country_lang_code != LangCode.ENGLISH and country_lang_code != LangCode.HEBREW:
                logger.info("country_lang_code is not english or hebrew", object={"country_lang_code": country_lang_code})
                country_lang_code = LangCode.ENGLISH
                logger.info("country_lang_code is set to english", object={"country_lang_code": country_lang_code})
            country_id = self.country.insert(country=country_name, lang_code=country_lang_code,
                new_country_data=country_data, coordinate=coordinate)
            '''
            return None
        else:
            country_data_temp = self.country.select_one_dict_by_id(
                view_table_name="country_ml_view",
                # TODO: change coordiante to coordinate in country_ml_view and here
                select_clause_value="coordiante, iso, name, iso3, numcode, phonecode",
                id_column_name="country_id", id_column_value=country_id)
        # TODO: when we change coordiante to coordinate we won't need country_data_temp, we can use country_data directly
        country_data = {
            'coordinate': country_data_temp.get('coordiante') or coordinate,
            'iso': country_data_temp.get('iso'),  # TODO iso / alpha_2 ?
            'name': country_data_temp.get('name'),  # or country_name?
            'iso3': country_data_temp.get('iso3'),  # iso3 / alpha_3?
            'numcode': country_data_temp.get('numcode'),  # numcode / numeric?
            'plus_code': country_data_temp.get('phonecode'),  # TODO plus_code / phonecode ?
        }
        return country_id, country_data

    def __process_state(self, state_name: str) -> int:
        """
        Process state information
        :param state_name: state name
        :return: state_id: int
        """
        # We don't throw an exception because a location can have None state
        if not self.__validate_method_arguments(state_name):
            logger.warning("state_name is None",
                           object={"state_name": state_name})
            return None
        state_lang_code = LangCode.detect_lang_code(text=state_name)
        if state_lang_code != LangCode.ENGLISH and state_lang_code != LangCode.HEBREW:
            logger.info("state_lang_code is not english or hebrew", object={"state_lang_code": state_lang_code})
            state_lang_code = LangCode.ENGLISH
            logger.info("state_lang_code is set to english", object={"state_lang_code": state_lang_code})
        state_id = self.state.get_state_id_by_state_name(
            state_name=state_name, lang_code=state_lang_code)
        if state_id is None:
            group_id = self.get_or_create_group_id(
                group_name=state_name, group_category_id=STATE_THEY_LIVE_IN_GROUP_CATEGORY,
                profile_id=self.profile_id, type_of_group="is_state")
            state_id = self.state.insert(
                coordinate=DEFAULT_COORDINATE,
                state=state_name,
                lang_code=state_lang_code,
                group_id=group_id)
        return state_id

    def __process_city(self, city_name: str, state_id: int, coordinate: Point) -> int:
        """
        Process city information
        :param city_name: city name
        :param coordinate: coordinate
        :return: city_id: int
        """
        # We don't throw an exception because a location can have None city
        if not self.__validate_method_arguments(city_name):
            logger.warning("city_name is None",
                           object={"city_name": city_name})
            return None
        city_lang_code = LangCode.detect_lang_code(text=city_name)
        if city_lang_code != LangCode.ENGLISH and city_lang_code != LangCode.HEBREW:
            logger.info("city_lang_code is not english or hebrew", object={"city_lang_code": city_lang_code})
            city_lang_code = LangCode.ENGLISH
            logger.info("city_lang_code is set to english", object={"city_lang_code": city_lang_code})
        city_id = self.city.get_city_id_by_city_name(city_name=city_name, lang_code=city_lang_code)
        if city_id is None:
            group_id = self.get_or_create_group_id(
                group_name=city_name, group_category_id=CITY_THEY_LIVE_IN_GROUP_CATEGORY,
                profile_id=self.profile_id, type_of_group="is_city")
            city_id = self.city.insert(city=city_name, state_id=state_id,
                                       lang_code=city_lang_code,
                                       coordinate=coordinate, group_id=group_id)
        return city_id

    def __process_county(self, county_name: str, state_id: int, coordinate: Point) -> int:
        """
        Process county information
        :param county_name: county name
        :param state_id: state id
        :param coordinate: coordinate
        :return: county_id: int
        """
        # We don't throw an exception because a location can have None county
        if not self.__validate_method_arguments(county_name, state_id):
            logger.warning("county_name or state_id is None",
                           object={"county_name": county_name, "state_id": state_id})
            return None
        county_lang_code = LangCode.detect_lang_code(text=county_name)
        if county_lang_code != LangCode.ENGLISH and county_lang_code != LangCode.HEBREW:
            logger.info("county_lang_code is not english or hebrew", object={"county_lang_code": county_lang_code})
            county_lang_code = LangCode.ENGLISH
            logger.info("county_lang_code is set to english", object={"county_lang_code": county_lang_code})
        county_id = self.county.get_county_id_by_county_name_state_id(county_name=county_name, state_id=state_id,
                                                                      lang_code=county_lang_code)
        if county_id is None:
            group_id = self.get_or_create_group_id(
                group_name=county_name, profile_id=self.profile_id, type_of_group="is_county")

            county_id = self.county.insert(county=county_name, lang_code=self.lang_code,
                                           coordinate=coordinate, group_id=group_id, state_id=state_id)
        return county_id

    def __process_region(self, region_name: str, country_id: int, coordinate: Point) -> int:
        """
        Process region information
        :param region_name: region name
        :param country_id: country id
        :param coordinate: coordinate
        :return: region_id: int
        """
        if not self.__validate_method_arguments(region_name, country_id):
            logger.warning("region_name or country_id is None",
                           object={"region_name": region_name, "country_id": country_id})
            return None
        region_lang_code = LangCode.detect_lang_code(text=region_name)
        if region_lang_code != LangCode.ENGLISH and region_lang_code != LangCode.HEBREW:
            logger.info("region_lang_code is not english or hebrew", object={"region_lang_code": region_lang_code})
            region_lang_code = LangCode.ENGLISH
            logger.info("region_lang_code is set to english", object={"region_lang_code": region_lang_code})
        region_id = self.region.get_region_id_by_region_name(
            region_name=region_name, country_id=country_id, lang_code=region_lang_code)
        if region_id is None:
            group_id = self.get_or_create_group_id(group_name=region_name, profile_id=self.profile_id,
                                                   type_of_group="is_region")

            region_id = Region().insert(region=region_name,
                                        lang_code=region_lang_code,
                                        coordinate=coordinate,
                                        country_id=country_id,
                                        group_id=group_id)
        return region_id

    def __process_neighborhood(self, neighborhood_name: str, city_id: int, coordinate: Point) -> int:
        """
        Process neighborhood information
        :param neighborhood_name: neighborhood name
        :param city_id: city id
        :param coordinate: coordinate
        :return: neighborhood_id: int
        """
        if not self.__validate_method_arguments(neighborhood_name, city_id):
            logger.warning("neighborhood_name or city_id is None",
                           object={"neighborhood_name": neighborhood_name, "city_id": city_id, "coordinate": coordinate})
            return None
        neighborhood_lang_code = LangCode.detect_lang_code(text=neighborhood_name)
        if neighborhood_lang_code != LangCode.ENGLISH and neighborhood_lang_code != LangCode.HEBREW:
            logger.info("neighborhood_lang_code is not english or hebrew, so set to english",
                        object={"neighborhood_lang_code": neighborhood_lang_code})
            neighborhood_lang_code = LangCode.ENGLISH
        neighborhood_id = self.neighborhood.get_neighborhood_id_by_neighborhood_name(
            neighborhood_name=neighborhood_name, city_id=city_id, lang_code=neighborhood_lang_code)
        if neighborhood_id is None:
            group_id = self.get_or_create_group_id(group_name=neighborhood_name, profile_id=self.profile_id,
                                                   type_of_group="is_neighborhood")

            neighborhood_id = Neighborhood().insert(neighborhood=neighborhood_name,
                                                    lang_code=neighborhood_lang_code,
                                                    coordinate=coordinate,
                                                    city_id=city_id,
                                                    group_id=group_id)
        return neighborhood_id

    # Refactored repeated database processing code into a helper function
    def get_or_create_group_id(self, *, group_name: str, profile_id: int, group_category_id: int = None,
                               type_of_group: str = None) -> int:
        if not self.__validate_method_arguments(group_name, profile_id):
            logger.warning("group_name, is_test_data or profile_id is None",
                           object={"group_name": group_name, "profile_id": profile_id})
            return None        
        # TODO Can we use a function in group-local repo? -We should take into account the end_timestamp, visibility, is_approved if the UserContext.effective user is not the owner
        group_id = self.group_local.select_one_value_by_id(
            select_clause_value='group_id',
            id_column_name="title", id_column_value=group_name)
        if not group_id:
            group_dict = {
                # 'is_neighborhood': True,
                # 'group_category_id': None,  # TODO: add group category for neighborhood
                'name': group_name,
                'title': group_name,
                'profile_id': profile_id,
                "is_main_title": 1,
                "is_approved": None,
                type_of_group: True,
            }
            data_dict_compare = {
                'name': group_name,
            }
            if group_category_id:
                group_dict['group_category_id'] = group_category_id
            group_lang_code = LangCode.detect_lang_code(text=group_name)
            if group_lang_code != LangCode.ENGLISH and group_lang_code != LangCode.HEBREW:
                group_lang_code = LangCode.ENGLISH
            upsert_group_result = self.group_local.upsert_group(
                group_dict=group_dict,
                data_dict_compare=data_dict_compare,
                lang_code=group_lang_code)
            group_id = upsert_group_result.get('group_id')
        return group_id

    def __validate_method_arguments(*args):
        """
        Validate method arguments to ensure they are not None or ''
        :param args: Variable number of arguments to validate
        :return: True if all arguments are not None or '', False otherwise
        """
        for arg in args:
            if arg is None or arg == '':
                return False
        return True
