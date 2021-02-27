class Validator:
    """A Validator class to handle validation of the command line inputs"""
    def __init__(self, category_dict):
        self.category_dict = category_dict
    
    def validate(self, args_list):
        """A validate function that ensure there is no empty command line,
        and passes the category's own validation"""

        if len(args_list) == 0:
            raise Exception("Error: Empty query, enter correct command line: <example>")

        category_args = args_list[0]
        if category_args not in self.category_dict.keys():
            raise Exception("Error: wrong flag. Use <command> to view the correct flag to use.")

        category = self.category_dict[category_args](args_list)
        validate_result = category.validate(args_list)
        return validate_result

