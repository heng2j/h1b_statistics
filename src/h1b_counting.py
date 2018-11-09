#!/usr/bin/env python3
# h1b_counting.py
# ---------------
# Author: Zhongheng Li
# Version: 1.0
# Start Date: 11-8-18
# Last Modified Date: 11-9-18


import csv
from argparse import ArgumentParser



# TODO get 'status' , 'class' , 'state' and 'soc' column names for this file
# TODO - need to come up a better way to find the target columns
# Verify each column name and extract the key columns
def define_required_columns_dict(columns ,dict):

    """
    :param columns:
    :param dict:
    :return:
    """

    for col in columns:

        if 'STATUS' in col:

            dict['STATUS'] = col

        elif 'CLASS' in col:

            dict['CLASS'] = col

        elif 'STATE' in col:

            dict['STATE'] = col

        elif 'SOC' in col:

            dict['SOC'] = col

# Read in the file line by line as dictionary labeled type
def csvRows(filename):

    """

    :param filename:
    :return:
    """

    with open(filename, 'r', newline='') as csvFile:
        reader = csv.DictReader(csvFile, delimiter=';')
        for row in reader:
            yield row


def get_data(inputFile):
    """

    :param inputFile:
    :return:
    """

    return [line for line in csvRows(inputFile)]



# TODO check if CASE_STATUS == 'CERTIFIED' and VISA_CLASS == 'H-1B'

"""
    The columns I needs are the following
        Anything like:
            'status' , 'class' , 'state' and 'soc'
            
            To verify a state column:
                - This the len of the value has to be 2
            To verify a status column:
                - 'CERTIFIED' has to be the value in this column
            To verify a class column:
                - text like 'H-1B' has to be one of the value in this column
            To verify a soc column:
                - the value type has to be string in this column



"""


# def get_top_10_results by field name
def get_top_10_by_field(data,target_field,columns_dict,result_columns):

    """

    :param data:
    :param target_field:
    :param columns_dict:
    :param result_columns:
    :return:
    """

    total_certified_count = 0
    summarized_dict = {}
    top_10_results_dict = {}

    for record in data:
        if record[columns_dict['STATUS']] == 'CERTIFIED':# and 'H-1B' in record[columns_dict['CLASS']]:
            total_certified_count +=1
            if record[columns_dict[target_field]] in summarized_dict:
                summarized_dict[record[columns_dict[target_field]]] = summarized_dict[record[columns_dict[target_field]]] + 1
            else:
                summarized_dict[record[columns_dict[target_field]]] = 1

    # Sort occupations_dict by value first then by key
    sorted_results = sorted(summarized_dict.items(), key=lambda x: (-x[1], x[0]))

    # Extract top 10 from occupations_dict and assign percentage
    top_10_records = list(sorted_results) #[:10]

    #  Loop through the top 10 and calculate the expected values
    for record in top_10_records:
        top_10_results_dict[record[0]] = {}
        top_10_results_dict[record[0]][result_columns[0]] = record[0]
        top_10_results_dict[record[0]][result_columns[1]] = record[1]
        top_10_results_dict[record[0]][result_columns[2]] = str(round((record[1] / total_certified_count) * 100, 1)) + '%'

    return top_10_results_dict

# Export top 10 results to output folder
def export_top_10_results(data_dict,result_columns,outputFile):

    """
    :param data_dict:
    :param result_columns:
    :param outputFile:
    :return:
    """


    with open(outputFile, 'w', newline='') as textfile:
        writer = csv.DictWriter(textfile, fieldnames=result_columns, delimiter=';')

        writer.writeheader()
        for name in data_dict:
            writer.writerow(data_dict[name])


if __name__ == '__main__':

    # Set up argument parser
    parser = ArgumentParser()
    parser.add_argument("-i","--input_file", help="Input file path", required=True)
    parser.add_argument("-o1", "--outputfile_top_10_occupations", help="Output file path for top_10_occupations.txt", required=True)
    parser.add_argument("-o2", "--outputfile_top_10_states", help="Output file path for top_10_states.txt", required=True)

    args = parser.parse_args()

    # Assign input, output files adn number of lines variables from command line arguments
    inputFile = args.input_file
    outputFile_1 = args.outputfile_top_10_occupations
    outputFile_2 = args.outputfile_top_10_states


    # Set up Global Variables
    # To create a column dict for future required columns expandability.
    required_columns_dict = {}

    # The records in the file must be sorted by NUMBER_CERTIFIED_APPLICATIONS, and in case of a tie, alphabetically by TOP_OCCUPATIONS.
    top_10_occupations_columns = ['TOP_OCCUPATIONS','NUMBER_CERTIFIED_APPLICATIONS','PERCENTAGE']

    # The records in this file must be sorted by NUMBER_CERTIFIED_APPLICATIONS field, and in case of a tie, alphabetically by TOP_STATES.
    top_10_states_columns = ['TOP_STATES', 'NUMBER_CERTIFIED_APPLICATIONS','PERCENTAGE']

    # Get consolidate data
    data = get_data(inputFile)

    # Get the list of columns
    column_list = list(data[0].keys())

    # Define the required_columns for our calculation
    define_required_columns_dict(column_list, required_columns_dict)

    # Get top 10 Occupations
    top_10_occupations_dict = get_top_10_by_field(data, 'SOC', required_columns_dict, top_10_occupations_columns)

    # Export top 10 Occupations to output folder
    export_top_10_results(top_10_occupations_dict, top_10_occupations_columns,outputFile_1)

    # Get top 10 states
    top_10_states_dict = get_top_10_by_field(data, 'STATE', required_columns_dict, top_10_states_columns)

    # Export top 10 states to output folder
    export_top_10_results(top_10_states_dict, top_10_states_columns, outputFile_2)