
import re
import html
import validators
from typing import Callable, Any, List, Dict, Union


EASY_PASSWORD_PATTERN = r'^[a-zA-Z0-9]{6,}$'
EASY_PASSWORD_MESSAGE = "Password must be at least 6 characters long and can contain letters and numbers."


MEDIUM_PASSWORD_PATTERN = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$'
MEDIUM_PASSWORD_MESSAGE = "Password must be at least 8 characters long, with at least one lowercase letter, one uppercase letter, and one number."

HARD_PASSWORD_PATTERN = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,}$'
HARD_PASSWORD_MESSAGE = "Password must be at least 12 characters long, including one lowercase, one uppercase, one number, and one special character."



def sanitize_input(input_data):
	try:
		return html.escape(input_data)
	except AttributeError:
		pass



def validate_form(userData, sanitize=True):
    # sanitize input data
    clean_user_data = {}
    if sanitize:
        for k in userData:
            clean_user_data[k] = sanitize_input(userData[k])
    else:
        clean_user_data = userData

    # validate user data (order-agnostic)
    validation_rules = {
        "username": "[a-zA-Z]+[_.]+[a-zA-Z0-9]+",
        "email": "[a-zA-Z0-9_-]+[@](aol|gmail|yahoo|outlook)+(.com)+",
        "password": "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    }

    messages = {
        "username": "Invalid username should be like this abc_123 or abc.abc",
        "email": "This email address is not valid",
        "password": "The password length must be at least 8 uppercase, lowercase letters, numbers, symbols like @aA123#*"
    }

    result = {}
    for field_name, pattern in validation_rules.items():
        if field_name in clean_user_data and not re.match(pattern, clean_user_data[field_name]):
            result[field_name] = messages[field_name]

    if result:
        return {"error": result}
    else:
        return {"good": clean_user_data}




def custom_validate(data, pattrens, messages, sanitize = True):
	clean_user_data = {}
	if sanitize:
		# sanitize input data
		for k in data:
			clean_user_data[k] = sanitize_input(data[k])
	else:
		clean_user_data = data

	result = {}

	for i, key in enumerate(clean_user_data):
		if not re.match(pattrens[i], clean_user_data[key]):
			result[key] = messages[i]

	if len(result) > 0:
		return {"error": result}
	else:
		return {"good": clean_user_data}






def validate_data_with_callbacks(
    data: dict,
    callbacks: List[Callable[[Any], bool]],
    messages: List[str],
    sanitize: bool = True
) -> Dict[str, Union[dict, Any]]:
    """
    Validates the given data using the provided callbacks and messages.

    Args:
        data: The data to validate.
        callbacks: A list of callback functions or lists containing a function and arguments.
        messages: A list of error messages corresponding to the callbacks or lists.
        sanitize: Whether to sanitize the input data before validation.

    Returns:
        A dictionary with either a "good": validated data key, an "error": error message key,
        or "errors": a dictionary of error messages for multiple errors.
    """

    clean_user_data = {}
    if sanitize:
        for k in data:
            clean_user_data[k] = sanitize_input(data[k])
    else:
        clean_user_data = data

    all_results = {}  # Use a more descriptive name

    # Loop through all callbacks
    for i, (func, data_key, msg) in enumerate(zip(callbacks, clean_user_data, messages)):
        try:
            if not isinstance(func, dict):  # Handle single-function callbacks
                value = clean_user_data[data_key]
                result = func(value)
                if not result:
                    all_results[data_key] = msg

            else:
                result = func['func'](data[data_key])
                if not result:
                    all_results[data_key] = msg
                    
                    
                clean_user_data[data_key] = data[data_key]
            

        except (TypeError, ValueError) as e:
            all_results[data_key] = f"Validation error: {e}"  # Provide more informative error message
            
	

    if not all_results:
        return {"good": clean_user_data}
    elif len(all_results) == 1:
        return {"error": list(all_results.values())[0]}
    else:
        return {"errors": all_results}


# -----------------------------
