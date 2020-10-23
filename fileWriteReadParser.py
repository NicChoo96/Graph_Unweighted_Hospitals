import json
import fastaparser
import os
import numpy as np

# https://pypi.org/project/fastaparser/

file_name = ""
genome_file_name = ""

output_directory = "output_files/"
genome_directory = "path_files/"


def get_chart_data(fname):
    json_data = get_json_data(fname)
    tc = []
    gl = []
    for i in range(0, len(json_data)):
        gl.append(json_data[i]['dna_strain_length'])
        tc.append(json_data[i]['comparison'])
    x = np.array(gl)
    y = np.array(tc)

    data = {'Strain_Length': x,
            'Comparison': y
            }
    return data


def filter_file_data(fname):
    json_data = get_json_data(fname)
    data_arr = []
    data_header = [
        "genome_length",
        "dna_strain",
        "dna_strain_length",
        "genome_file_type",
        "time_executed",
        "method",
        "comparison",
        "matches",
        "position found"
    ]
    for i in range(0, len(json_data)):
        data = {}
        for j in range(0, len(data_header)):
            data[data_header[j]] = json_data[i][data_header[j]]
        data_arr.append(data)
    return data_arr


def read_data_json_file():
    with open(output_directory + file_name) as json_file:
        data = json.load(json_file)
        print(json.dumps(data, indent=1, sort_keys=True))


def get_json_data(f_name):
    if os.path.isfile('./' + output_directory + f_name):
        with open(output_directory + f_name) as json_file:
            data = json.load(json_file)
            if len(data) > 0:
                return data['run_history']
            else:
                return []


def check_output_exist():
    return os.path.isfile('./' + output_directory + file_name)


def clear_data_file(f_name):
    if os.path.isfile('./' + output_directory + f_name):
        with open(output_directory + f_name, 'w') as outfile:
            json.dump({}, outfile)


def write_data_json_file(records):
    data = {'run_history': []}
    # Load in existing file record
    if os.path.isfile('./' + output_directory + file_name):
        with open(output_directory + file_name) as json_file:
            f_data = json.load(json_file)
            if len(f_data) != 0:
                data = f_data
    data['run_history'].append(records)

    with open(output_directory + file_name, 'w') as outfile:
        json.dump(data, outfile)


def open_genome_file():
    dna_string = ""
    with open(genome_directory + genome_file_name) as fasta_file:
        parser = fastaparser.Reader(fasta_file)
        for seq in parser:
            dna_string += seq.sequence_as_string()
    return dna_string


def get_list_output_files():
    files = []
    for file in os.listdir("output_files"):
        files.append(file)
    return files

