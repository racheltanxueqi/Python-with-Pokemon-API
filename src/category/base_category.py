class BaseCategory:
    """A BaseCategory informal interface class for different type of children category.
    For now there is only search via Pokemon's name and id category.
    Searching via ability and type categories is not available"""

    def validate(self, args_list):
        """Validate the respective category"""
        pass

    def execute(self, response_data_json, read_from_file=False):
        """Execute the category's api call"""
        pass

    def set_attributes(self, data_json, read_from_file=False):
        """Set the attributes' of the category for displaying of information"""
        pass

    def format_information(self):
        """Format the category's information for display"""
        pass