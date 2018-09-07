# antipsychotics equivalent dose calculator
extracting data from EMR(electronic medical record) and then processing them into antipsychotics equivalent doses such as chlorpromazeine or olanzqpine equivalent dose

# Med_Dose.py
a python3 script which reads a csv file containing the patient id, brand/chemical name of antipsychotics, prescribed days, and prescribed dose, and converts the total dose into an averaged olanzapine equivalent dose
the output is a csv format, and prints the patient id and averaged olanzapine equivalent dose

# Med_Dose_v2.py
a few debugging:
1) fixed a bug where each row was counted was 1 day resulting in exagerrated prescription days count -- now uses the datetime module to calculate the prescription days count
2) fixed a bug where the first row of each patient was omitted from calculating the antipsychotics dose
3) fixed a bug where the calculation result of the last patient was omitted from the csv file
