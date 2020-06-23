import csv
import datetime
import pandas as pd

survey_results = list()
# with open("survey_results.csv", "rU") as f:
#     # csv_reader = csv.reader(f, delimiter=";", quotechar="\"")
#     # with open("test.csv", 'rU') as csvIN:
#     outCSV = (line for line in csv.reader(f, dialect='excel'))


#     for row in outCSV:
#         print(row)
#         survey_results.append(row)

survey_results = pd.read_excel("survey_results.xlsx").values.tolist()

survey_results = survey_results[1:-1]
work_len = 0
submit_count = len(survey_results)
for res in survey_results:
        work_len += (res[6] - res[5]).total_seconds()

avg_work_len = (work_len / submit_count)

print("avg. work len: %s min" %str(datetime.timedelta(seconds=avg_work_len)))
