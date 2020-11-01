import os
import json

def write_data_json_file(output_directory, file_name, writePath):
    # Load in existing file record
    if os.path.isfile('./' + output_directory + file_name):
        with open(output_directory + file_name) as json_file:
            f_data = json.load(json_file)
            if len(f_data) != 0:
                data = f_data
    data = writePath

    with open(output_directory + file_name, 'w') as outfile:
        json.dump(data, outfile)