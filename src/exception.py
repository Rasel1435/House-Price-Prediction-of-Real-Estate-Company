import sys

def error_message_detail(error, error_detail: sys):
    """
    Extracts the file name, line number, and error message 
    from the system execution info.
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    
    error_message = f"Error occurred in python script: [{file_name}] " \
                    f"at line number: [{line_number}] " \
                    f"with error message: [{str(error)}]"

    return error_message

class CustomException(Exception):
    """
    A custom exception class that inherits from the base Exception.
    It formats the error message to include specific file and line details.
    """
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message