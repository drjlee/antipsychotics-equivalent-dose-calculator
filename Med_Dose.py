
# coding: utf-8
import os, re

# the directory where the csv file is located
os.chdir("/Users/junheelee/Documents/2016(LJH)/2017Trivia/FEP_CHR_followup_data/")

# output csv file
import csv
with open('output.csv', 'w', newline='', encoding = 'utf-8') as fcsv:
    fieldnames = ['patient', 'olzdose']
    writer = csv.DictWriter(fcsv, fieldnames = fieldnames)
    
    writer.writeheader()
    
    # the requested data should be converted to csv format, and the data should exclude the prescriptions on the day the scan was done, and in case of SNUH, should include 'self medications'
    fp = open("SZ_prescription_23Oct.csv")
    # initialising patiend id, which is data[1]
    patient = '27709908'
    # initialising olzdose & totaldays
    olzdose = 0.0
    temp_olzdose = 0.0
    totaldays = 0.0
    # [1:] for skipping the top row, if it has headers
    for line in fp.readlines()[1:]:
        data = line.split(',')    
        # chemical name and dosage in mg
        # chemical names in the original dataset here = 
        #  ['Amisulpride', 'Aripiprazole', 'Blonanserin', 'Haloperidol', 'Olanzapine', 'Paliperidone', 'Quetiapine', 'Risperidon', Risperidon Disp, 'Risperidone', Risperidone Disp, 'Ziprasidone', 'Zyprexa' zydis*, Zyprexa Zydis*]
        # olanzapine equivalent doses were referenced from S Leucht et al., Schizophr Bull 2015;41(6):1397-1402
        drugs = {'Amisulpride':38.3, 'Aripiprazole':1.4, 'Blonanserin':1.6, 'Haloperidol':0.7, 'Olanzapine':1.0, 'Paliperidone':0.6, 'Quetiapine':32.3, 'Risperidon':0.4, 'Risperidone':0.4, 'Ziprasidone':7.9, 'Zyprexa':1.0}
        names = data[5]
        # the first element on the list is the chemical name
        chemical = names.split(' ')
        if patient == data[1]:
            if chemical[0] in drugs:
                # \s: a space between chemical names and dosage, \d: dosage, .{0,4}: whatever numbers or characters till 'mg'
                m = re.search('(\s)(\d+.{0,4})(mg)', data[5])
                # taking numbers only and then converting into float
                dosage = float(m.group(2))
                # totaltabs is the total number of prescribed tablets
                totaltabs = float(data[9])
                # the total dosage = totaltabs multiplied by dosage per tab
                totaldose = dosage * totaltabs
                # olzdose is olanzapine equivalent dosage of 'totaldose'
                # if it is the same patient, sum up the olzdose till the next patient comes up
                olzdose = totaldose / drugs[chemical[0]]
                # olzdose should be divided by total days prescribed per patient
                prescribed_days = float(data[8])
                totaldays = totaldays + prescribed_days
                temp_olzdose = temp_olzdose + olzdose
                avg_olzdose = temp_olzdose / totaldays
                print(patient, 'totaldose', totaldose)
                print(patient, 'prescribed_days', prescribed_days)
                print(patient, 'totaldays', totaldays)
                print(patient, 'temp_olzdose', temp_olzdose)
                print(patient, 'avg_olzdose', avg_olzdose)
        else:
            # if it is the next patient, write the patient ID and summed olzdose to the csv file
            writer.writerow({'patient': patient, 'olzdose': avg_olzdose})
            # and then initialise parameters for the next patient
            avg_olzdose = 0.0
            totaldays = 0.0
            temp_olzdose = 0.0
        patient = data[1]
    fp.close()

