import csv
import argparse
import pdb

# This script will take two files with graduate student application information and merge
# the tables into a single table

parser = argparse.ArgumentParser()

parser.add_argument('-d', '--degree', help="MS vs PhD", default="PhD")
parser.add_argument('-m', '--major',  help="EMA vs NEEP", default="NEEP")

args = parser.parse_args()

# this should be run once per degree type: MS vs PhD
degree_type = args.degree
base_file_name = args.major + " Fall 2019"

# the original files are assumed to have the following names:
# * "NEEP Fall 2019 MS Main Data.csv" + "NEEP Fall 2019 MS Preference Data.csv" '
#          -> "NEEP Fall 2019 MS Combined Data.csv"
# * "NEEP Fall 2019 PhD Main Data.csv" + "NEEP Fall 2019 PhD Preference Data.csv" '
#          -> "NEEP Fall 2019 PhD Combined Data.csv"

common_key = 'ApplicationSID'

all_student_data = {}
data_keys = []

# base file name
primary_data_file = base_file_name + " " + degree_type + " Main Data.csv"
preference_data_file = base_file_name + " " + degree_type + " Preference Data.csv"
combined_data_file = base_file_name + " " + degree_type + " Combined Data.csv"

test_score_fields = { 'GRE' : ['Verbal Score',
                               'Verbal Percent',
                               'Quantitative Score',
	                       'Quantitative Percent',
	                       'Analytical Score',
	                       'Analytical Percent'],
                      'AdvGRE' : ['GRE Subject Type',
                                  'Subject Score',
                                  'Subject Percent'],
                      'TOEFL' : ['TOEFL Type',
                                 'Total Score',
	                         'Reading Score',
	                         'Listening Score',
	                         'Speaking Score',
	                         'Writing Score'],
                      'IELTS' : ['Total Score',
	                         'Reading Score',
	                         'Listening Score',
	                         'Speaking Score',
	                         'Writing Score'],
                    }



# Open file with primary data per student
with open(primary_data_file) as primary_data_csv:
    primary_data_reader = csv.reader(primary_data_csv)
    first_row = True
    for primary_data in primary_data_reader:
        # capture header from first row
        if first_row:
            data_keys = [item.strip() for item in primary_data]
            # fix duplicate GPA headers
            for idx, key in enumerate(data_keys):
                if key in data_keys[:idx]:
                    data_keys[idx] = "MS " + key
            first_row = False
        else:
            # create a dictionary by zipping together the keys
            this_student_data = dict(zip(data_keys,primary_data))
            # combine multiple exams
            student_id = this_student_data[common_key]
            test_type = this_student_data['Test Type']
            if student_id in all_student_data:
                all_student_data[student_id]['Test Type'] += "-" + test_type
                for field in test_score_fields[test_type]:
                    all_student_data[student_id][field] = this_student_data[field]
            else:
                all_student_data[student_id] = this_student_data

# get final set of headers
final_keys = data_keys

with open(preference_data_file) as preference_data_csv:
    preference_data_reader = csv.reader(preference_data_csv)
    first_row = True
    for preference_data in preference_data_reader:
        if first_row:
            data_keys = [item.strip() for item in preference_data]
            first_row = False
        else:
            this_pref_data = dict(zip(data_keys,preference_data))
            if this_pref_data[common_key] not in all_student_data:
                raise ValueError("Found preference data for a student with no main data: " + this_pref_data['Last Name'])
            this_student_data = all_student_data[this_pref_data[common_key]]
            this_student_data[this_pref_data['Question']] = this_pref_data['Response']
            if (this_pref_data['Question'] not in final_keys):
                final_keys.append(this_pref_data['Question'])

with open(combined_data_file,mode='w') as combined_data_csv:
    combined_data_writer = csv.writer(combined_data_csv)
    combined_data_writer.writerow(final_keys)
    for student_data in all_student_data.values():
        combined_data_writer.writerow(student_data.values())

