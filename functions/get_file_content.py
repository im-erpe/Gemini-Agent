import os
from config import CHARS_LIMIT


def get_file_content(working_directory, file_path):
        try:
            working_dir_abs = os.path.abspath(working_directory)
            target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path)) 
            
            
            if os.path.commonpath([working_dir_abs, target_file_path]) != working_dir_abs:
                return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            if not os.path.isfile(target_file_path):
                return f'Error: File not found or is not a regular file: "{file_path}"'
            
            with open(target_file_path, "r") as f:
                file_content_string = f.read(CHARS_LIMIT)
                if f.read(1):
                    file_content_string += f'[...File "{file_path}" truncated at {CHARS_LIMIT} characters]'
                
            return file_content_string
        except Exception as e:
            return f'Error: {str(e)}'