import os, re
import datetime
from datetime import date

# the directory where the csv file is located
# csv should contain the prescription data *prior to* the scan, and [Self] prescriptions
os.chdir("/Users/junheelee/Documents/2016(LJH)/2017Trivia/(done)ECT_EEG_PANSS_med/medication_data/")

# output csv file
import csv
with open('output.csv', 'w', newline='', encoding = 'utf-8') as fcsv:
    fieldnames = ['patient', 'olzdose']
    writer = csv.DictWriter(fcsv, fieldnames = fieldnames)
    
    writer.writeheader()
    
    fp = open("supreme_processed_05Sep.csv")
    # initialising patiend id, which is data[1]
    patient = '19461476'
    # initialising olzdose & totaldays
    olzdose = 0.0
    temp_olzdose = 0.0
    totaldays = 0.0
    dates = []
    prescription_date = date(2000,1,1)
    print(prescription_date)
    # [1:] for skipping the top row, if it has headers
    for line in fp.readlines()[1:]:
        data = line.split(',')
        print(data)
        # chemical name and dosage in mg
        # chemical names in the original dataset here = 
        #  ['Amisulpride', 'Aripiprazole', 'Blonanserin', 'Haloperidol', 'Olanzapine', 'Paliperidone', 'Quetiapine', 'Risperidon', Risperidon Disp, 'Risperidone', Risperidone Disp, 'Ziprasidone', 'Zyprexa' zydis*, Zyprexa Zydis*]
        # olanzapine equivalent doses were referenced from S Leucht et al., Schizophr Bull 2015;41(6):1397-1402
        drugs = {'Amisulpride':38.3, 'Aripiprazole':1.4, 'Blonanserin':1.6, 'Chlorpromazine':38.9, 'Clozapine':30.6, 'Haloperidol':0.7, 'Olanzapine':1.0, 'Paliperidone':0.6, 'Quetiapine':32.3, 'Risperidone':0.4, 'Ziprasidone':7.9}
        names = data[4]
        # the first element on the list is the chemical name
        chemical = names.split(' ')
        if patient == data[0]:
            if chemical[0] in drugs:
                # \s: a space between chemical names and dosage, \d: dosage, .{0,4}: whatever numbers or characters till 'mg'
                m1 = re.search('(\s)(\d+.{0,4})(mg)', data[4])
                # taking numbers only and then converting into float
                dosage = float(m1.group(2))
                # totaltabs is the total number of prescribed tablets
                totaltabs = float(data[5])
                # the total dosage = totaltabs multiplied by dosage per tab
                totaldose = dosage * totaltabs
                # olzdose is olanzapine equivalent dosage of 'totaldose'
                olzdose = totaldose / drugs[chemical[0]]
                # if it is the same patient, sum up the olzdose till the next patient comes up
                temp_olzdose = temp_olzdose + olzdose
                # dates is a list of all the prescription dates in this patient
                # append the prescription date to the list 'dates'
                m2 = re.search('(\d+)(\-)(\d+)(\-)(\d+)', data[3])
                prescription_date = date(int(m2.group(1)), int(m2.group(3)), int(m2.group(5)))
                dates.append(prescription_date)
                print(patient, 'totaldose', totaldose)
                print(patient, 'prescription_date', prescription_date)
                print(patient, 'temp_olzdose', temp_olzdose)
                print(patient, 'avg_olzdose', avg_olzdose)
            else:
                print('not antipsychotics')
        else:
            # if it is the next patient, calculate the average olzdose
            totaldays = (max(dates)-min(dates)).days
            avg_olzdose = temp_olzdose / totaldays
            print('******************next patient*********************')
            # then write the patient ID and summed olzdose to the csv file
            writer.writerow({'patient': patient, 'olzdose': avg_olzdose})
            # and then initialise parameters for the next patient
            avg_olzdose = 0.0
            totaldays = 0.0
            temp_olzdose = 0.0
            dates = []
            # after initialising, process the first row of the next patient
            if chemical[0] in drugs:
                # \s: a space between chemical names and dosage, \d: dosage, .{0,4}: whatever numbers or characters till 'mg'
                m1 = re.search('(\s)(\d+.{0,4})(mg)', data[4])
                # taking numbers only and then converting into float
                dosage = float(m1.group(2))
                # totaltabs is the total number of prescribed tablets
                totaltabs = float(data[5])
                # the total dosage = totaltabs multiplied by dosage per tab
                totaldose = dosage * totaltabs
                # olzdose is olanzapine equivalent dosage of 'totaldose'
                olzdose = totaldose / drugs[chemical[0]]
                # if it is the same patient, sum up the olzdose till the next patient comes up
                temp_olzdose = temp_olzdose + olzdose
                # dates is a list of all the prescription dates in this patient
                # append the prescription date to the list 'dates'
                m2 = re.search('(\d+)(\-)(\d+)(\-)(\d+)', data[3])
                prescription_date = date(int(m2.group(1)), int(m2.group(3)), int(m2.group(5)))
                dates.append(prescription_date)
                print(patient, 'totaldose', totaldose)
                print(patient, 'prescription_date', prescription_date)
                print(patient, 'temp_olzdose', temp_olzdose)
                print(patient, 'avg_olzdose', avg_olzdose)
            else:
                print('not antipsychotics')
        patient = data[0]
    # write the avg_olzdose of the last patient to the csv file
    avg_olzdose = temp_olzdose / totaldays
    writer.writerow({'patient': patient, 'olzdose': avg_olzdose})
    fp.close()
