import sys
from pokemon_frontend.validator import Validator
from category.base_category import BaseCategory
from category.pokemon import Pokemon
from pokemon_query_processor.evaluator import Evaluator
from pokemon_query_processor.result_projector import ResultProjector

if __name__ == "__main__":
    """This is main where it first interact with user's inputs"""
    # A category dictionary to allow for future extension of other search modes via types, ability 
    category_dict = {
        "-p" : Pokemon
    }

    # Get an array of the command line arguments 
    args_list = sys.argv[1:]

    # Validate the command line arguments
    category_validator = Validator(category_dict)
    try:
        validator_result = category_validator.validate(args_list)
        category_args = args_list[0]
        search_value = args_list[1]
        category = category_dict[category_args](search_value)

        # Evaluate the command lind arguments
        evaluator = Evaluator()
        evaluator.evaluate(category)

        # Format and display the result
        result_projector = ResultProjector()
        result = result_projector.format_result(category)
        print(result)

    except Exception as e:
        print(str(e))

    
