import json
import os
import time
import math
from datetime import date
import requests
from config import config

class Evaluator():
    """An Evaluator class to evaluate the category's search value and
    to api call or fetch data from cache to display the information"""

    def evaluate(self, category):
        """A function that contains the logic to check: 
        If the stored information is over a week old, the data should be retrieved again from the API. 
        If not, the data should be retrieved from the storage text file"""

        url = category.base_url + category.category_name + "/" + category.search_value
        file_path = config.STORAGE_FILE_PATH
        present_date = date.today().strftime("%d-%m-%Y")

        if self.is_file_empty(file_path):
            storage_data_json = {}
            storage_data_json[category.category_name] = {}
            self.fetch_and_update_resource(url, file_path, storage_data_json, category, present_date)
        else:
            with open(file_path) as database_file:
                database_file_data = json.load(database_file)

            category_dict = database_file_data[category.category_name]

            if category.search_value in category_dict:
                # Retrieve last stored date based on the searched value (name or id)
                last_stored_date = category_dict[category.search_value]["last_stored_date"]

                # Calculate how old the stored information is
                days = self.calulate_days_between(last_stored_date, present_date)
                
                if days > 7:
                    self.fetch_and_update_resource(url, file_path, database_file_data, category, present_date)
                else:
                    new_payload = category.execute(category_dict[category.search_value]["data"], read_from_file=True)
            else:                   
                # Has not fetch data based on searched value before, fetch data and store here
                self.fetch_and_update_resource(url, file_path, database_file_data, category, present_date)

    
    def is_file_empty(self, file_path):   
        """ Check if file is empty by confirming if its size is 0 bytes"""
        # Check if file exist and it is empty
        return os.path.exists(file_path) and os.stat(file_path).st_size == 0
    
    def calulate_days_between(self, last_stored_date, present_date):
        """Calculate the number of days between 2 dates"""
        last_stored_date_arr = last_stored_date.split("-")
        start_date = date(int(last_stored_date_arr[2]), int(last_stored_date_arr[1].lstrip("0")), int(last_stored_date_arr[0].lstrip("0")))
        present_date_arr = present_date.split("-")
        end_date = date(int(present_date_arr[2]), int(present_date_arr[1].lstrip("0")), int(present_date_arr[0].lstrip("0")))
        return abs(start_date-end_date).days 
       
    def fetch_and_update_resource(self, url, file_path, data_json, category, present_date):
        """A function to make an api call and store or make an update to storage"""

        # Make api call
        response = requests.get(url)
        status_code = response.status_code

        if (status_code == 200):
            # Successful response
            response_data_json = response.json()
            new_payload = category.execute(response_data_json, read_from_file=False)

            response_data_name = response_data_json["name"]
            response_data_id = response_data_json["id"]

            category_dict = data_json[category.category_name]
            category_dict[response_data_name] = {
                "last_stored_date": present_date,
                "data": new_payload
            }
            category_dict[response_data_id] = category_dict[response_data_name]

            # Store the information locally
            self.store_data(data_json, file_path)
        else: 
            raise Exception("Bad Response: "+ str(status_code))

    def store_data(self, data, file_path):
        """Write data to storage text file"""
        with open(file_path, 'w') as database_file:
            database_file.write(json.dumps(data))
        database_file.close()