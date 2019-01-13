# merge_grad_data
Python script to merge data from different sets of grad applicant data

This script assumes the existence of two related CSV files:
1. The "Main Data" file contains the standard application data including personal data, prior GPAs and various test score
2. The "Preference Data" file contians responses to questions about research interests and faculty mentor preferences

There may be more than one record for each student in each file.
* In "Main Data", multiple records exist for multiple test, GRE and otherwise
* In "Preference Data", multiple records exist for each of the peference questions answered by the applicant

Currently, this script assumes file names of the form: `<MAJOR> Fall 2019 <DEGREE> Main Data.csv` and 
`<MAJOR> Fall 2019 <DEGREE> Preference Data.csv`, where the user can specify the `<MAJOR>` and `<DEGREE>` 
on the command-line.
