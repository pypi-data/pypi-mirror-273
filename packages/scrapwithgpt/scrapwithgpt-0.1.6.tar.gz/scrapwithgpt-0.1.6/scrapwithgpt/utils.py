

from .config import WARNING_UNKNOWN


from typing import  Callable, Any
import datetime
import inspect
import re


def get_module_name(func: Callable[..., Any]) -> str:
    """
    Given a function, returns the name of the module in which it is defined.
    """
    module = inspect.getmodule(func)
    if module is None:
        return ''
    else:
        return module.__name__.split('.')[-1]

def log_issue(exception: Exception, func: Callable[..., Any], additional_info: str = "") -> None:
    """
    Logs an issue. Can be called anywhere and will display an error message showing the module, the function, the exception and if specified, the additional info.

    Args:
        exception (Exception): The exception that was raised.
        func (Callable[..., Any]): The function in which the exception occurred.
        additional_info (str): Any additional information to log. Default is an empty string.

    Returns:
        None
    """
    now = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
    if hasattr(func, '__name__'):
        function_name = func.__name__
        module_name = get_module_name(func)
    else:
        function_name = func if isinstance(func, str) else WARNING_UNKNOWN
        print(f"🟡 What is this function? {func} * {type(func)}")
        try:
            module_name = get_module_name(func)
        except:
            module_name = "Couldn't get the module name"
    additional = f"""
    ****************************************
    Additional Info: 
    {additional_info}
    ****************************************""" if additional_info else ""
    print(f"""
    ----------------------------------------------------------------
    🚨 ERROR 🚨
    Occurred: {now}
    Module: {module_name} | Function: {function_name}
    Exception: {exception}{additional}
    ----------------------------------------------------------------
    """)

def remove_excess(text: str) -> str:
    """
    Replaces all occurrences of double newlines ('\n\n') and double spaces with single newline and space, respectively.
    """
    double_jump = '\n\n'
    double_space = '  '
    while double_jump in text:
        text = text.replace(double_jump, '\n')
    while double_space in text:
        text = text.replace(double_space, ' ')
    return text

def remove_non_printable(text :str) -> str:
    """
    Strong cleaner which removes non-ASCII characters from the input text.
    """
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text) # removes non printable char
    y = text.split()
    z = [el for el in y if all(ord(e) < 128 for e in el)]
    return ' '.join(z)

def get_now(exact: bool = False) -> str:
    """
    Small function to get the timestamp in string format.
    By default we return the following format: "10_Jan_2023" but if exact is True, we will return 10_Jan_2023_@15h23s33
    """
    now = datetime.datetime.now()
    return datetime.datetime.strftime(now, "%d_%b_%Y@%Hh%Ms%S") if exact else datetime.datetime.strftime(now, "%d_%b_%Y")


def is_valid_email(email):
    '''
    Not the best but a first regex protection.
    '''
    return bool(re.search(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))

# *************************************************************
if __name__ == "__main__":
    pass