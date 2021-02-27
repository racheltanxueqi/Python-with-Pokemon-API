from .base_category import BaseCategory
from functools import reduce
import requests
from config import config
from terminaltables import DoubleTable

class Pokemon(BaseCategory):
    """A Pokemon class that implements BaseCategory class for Pokemon category"""
    def __init__(self, search_value):
        self.base_url = config.BASE_URL
        self.category_name = "pokemon"
        self.search_value = search_value
        self.id = None
        self.name = None
        self.types_arr = None
        self.location_area_encounters = None
        self.stats_arr = None


    def validate(self, args_list):
        """Validate the respective category"""
        if len(args_list) > 2:
            raise Exception("Error: Too many arguments")
        if not args_list[1].isalnum():
            raise Exception("Error: Search value must be a valid name or id")
        
        return True

    def execute(self, response_data_json, read_from_file=False):
        """Execute the pokemon's api call"""
        self.set_attributes(response_data_json, read_from_file=read_from_file)

        new_payload = {
            "name": self.name,
            "id": self.id,
            "types": self.types_arr,
            "location_area_encounters": self.location_area_encounters,
            "stats": self.stats_arr
        }
        return new_payload

    def set_attributes(self, data_json, read_from_file=False):
        """Set the attributes' of the pokemon category for displaying of information.
        Atributes consist of id, name, types, locations, methods and stats."""
        self.id = data_json["id"]
        self.name = data_json["name"]

        if read_from_file:
            print(data_json)
            self.types_arr = data_json["types"]
            self.stats_arr = data_json["stats"]
            self.location_area_encounters = data_json["location_area_encounters"]
        else:
            # strip and parse types information
            types_arr = []
            for types_element in data_json["types"]:
                types_arr.append(types_element["type"]["name"])
            self.types_arr = types_arr

            # strip  and parse stats information
            stats_arr = []
            for stats_element in data_json["stats"]:
                stats_arr.append({
                    "stat_name": stats_element["stat"]["name"], 
                    "base_stat": stats_element["base_stat"]
                })
            self.stats_arr = stats_arr

            # strip  and parse encounter locations and methods information
            location_api = data_json["location_area_encounters"]
            location_response = requests.get(location_api)
            location_res_status_code = location_response.status_code
            if (location_res_status_code == 200):
                location_area_encounters = location_response.json()
                self.parse_location_and_method(location_area_encounters)
            else: 
                if location_res_status_code == 404:
                    raise Exception("No Result Found")
    
    
    def parse_location_and_method(self, location_area_encounters):
        """Process the fetch data information on location and method for pokemon category"""
        location_area_encounters_arr = []
        for location_element in location_area_encounters:
            is_kanto_location = location_element["location_area"]["name"].find("kanto")
            if is_kanto_location != -1:
                location_area_encounters_dict = {}
                encounter_location = location_element["location_area"]["name"]
                methods_set = set()
                for version_details_arr in location_element["version_details"]:
                    encounter_details_arr = version_details_arr["encounter_details"]
                    for encounter_details_element in encounter_details_arr:
                        name = encounter_details_element["method"]["name"]
                        methods_set = methods_set.union({name})
                    location_area_encounters_dict["encounter_location"] = encounter_location
                    location_area_encounters_dict["encounter_method"] = list(methods_set)
                location_area_encounters_arr.append(location_area_encounters_dict)
        self.location_area_encounters = location_area_encounters_arr
    
    def format_information(self):
        """Format the pokemon's information for display"""
        # Format display of types
        type_tag = DoubleTable([self.types_arr])

        # Format display of encounter details
        if(len(self.location_area_encounters) > 0):
            encounter_details_data = [["Location", "Methods"]]
            for location_area_encounter in self.location_area_encounters:
                encounter_details_data.append([location_area_encounter["encounter_location"], ",".join(location_area_encounter["encounter_method"])])
            encounter_details_table = DoubleTable(encounter_details_data)  
            encounter_details = encounter_details_table.table
        else:
            encounter_details = "-"

        # Format display of stats
        stats_data = [["Stats Name", "Base Stats"]]
        for stat in self.stats_arr:
            stats_data.append([stat["stat_name"], stat["base_stat"]])
        stats_table = DoubleTable(stats_data)

        # Format final resulting table
        final_data = [
            ["ID", self.id],
            ["Name", self.name],
            ["Types", type_tag.table],
            ["Encounter\nDetails", encounter_details],
            ["Stats", stats_table.table]
        ]
        final_table = DoubleTable(final_data)
        final_table.inner_row_border = True
        final_table.title = "Pokemon Information"
        final_table.justify_columns[1] = "center"

        return final_table.table
