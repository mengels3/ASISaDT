import csv
import datetime
import statistics
import re
import string

import pandas as pd
import matplotlib.pyplot as plt

from collections import Counter
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer

answer_mapping = {
    'XAI01': {
        'A1': 'not at all',
        'A2': 'I have heard of it,\n but I have never dealt with it',
        'A3': 'I have read articles about it\n from time to time',
        'A4': 'I regularly deal with the topic',
        'A5': 'I am an expert'
    },
    'XAI02': {
        'A1': 'not at all',
        'A2': 'I have heard of it,\n but I have never dealt with it',
        'A3': 'I have read articles about it\n from time to time',
        'A4': 'I follow the topic closely'
    },
    'XAI03': {
        'A1': 'Completely and without questioning it',
        'A2': 'Basically yes, but I would like\n to understand the background better',
        'A3': 'Most of the time,\n but I do not understand the background',
        'A4': 'Rather rarely,\n only if it is understandable',
        'A5': 'Actually never'
    },
    'XAI04': {
        'A1': 'Yes, in any case',
        'A2': 'Yes, in parts',
        'A3': 'No, constant',
        'A4': 'No, it would go down'
    },
    'AIpT01': {
        'A1': 'No',
        'A2': 'Yes',
        'A3': 'Yes, and I have already dealt with this topic'
    },
    'AIpT02': {
        'A1': 'No, never',
        'A2': 'Rather not',
        'A3': 'No opinion',
        'A4': 'Rather yes',
        'A5': 'Yes, absolutly'
    },
    'EnvSus01': {
        'A1': 'Not important',
        'A2': 'Rather not important',
        'A3': 'Rather important',
        'A4': 'Very important'
    },
    'EnvSus02': {
        'A1': '5x per Week or more',
        'A2': '2-4x per Week',
        'A3': '1x per Week',
        'A4': 'Few times per month',
        'A5': 'Few times per week',
        'A6': 'Never'
    },
    'EnvSus03': {
        'A1': 'Not important',
        'A2': 'Rather not important',
        'A3': 'I do not care',
        'A4': 'Rather important',
        'A5': 'Very important'
    },
    'EnvSus04': {
        'A1': 'Not important',
        'A2': 'Rather not important',
        'A3': 'I do not care',
        'A4': 'Rather important',
        'A5': 'Very important'
    },
    'O01': {
        'A1': 'Bad',
        'A2': 'Rather bad',
        'A3': 'Rather good',
        'A4': 'Good',
        'A5': 'Very good'
    },
    'O02': {
        'A1': 'No',
        'A2': 'Yes, in parts',
        'A3': 'Yes, absolutly',
    },
    'O03': {
        'A1': 'Not important',
        'A2': 'Rather not important',
        'A3': 'Rather important',
        'A4': 'Very important',
    }
}

lemmatizer = WordNetLemmatizer()

def remove_noise(tweet_tokens):

    stop_words = stopwords.words('german')
    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(str(token.lower()))
    print(cleaned_tokens)
    return list(cleaned_tokens)


def main():

    survey_results = list()
    # with open("survey_results.csv", "rU") as f:
    #     # csv_reader = csv.reader(f, delimiter=";", quotechar="\"")
    #     # with open("test.csv", 'rU') as csvIN:
    #     outCSV = (line for line in csv.reader(f, dialect='excel'))


    #     for row in outCSV:
    #         print(row)
    #         survey_results.append(row)

    survey_results = pd.read_excel("survey_results.xlsx")
    titles = survey_results.keys()
    survey_results = survey_results.values.tolist()

    survey_results = survey_results[1:-1]
    work_lens = list()

    for res in survey_results:
        try:            
            res[9] = "A" + str(int(res[9]))
        except:
            pass
        for x in res:
            if type(x) == str():
                x = x.replace('\n', ' ').replace('\r', ' ')

    results_dict = dict()
    for t in titles:
        results_dict[t] = list()

    cat_1 = 0
    cat_2 = 0
    cat_3 = 0
    rest = 0

    clustered_results = dict()
    cl_groups = [0, 1, 2, 3]

    for t in titles:
        if t not in clustered_results.keys():
            clustered_results[t] = dict()
        for k in cl_groups:
            if k not in clustered_results[t].keys():
                clustered_results[t][k] = list()

    for res in survey_results:
        if str(res[1]) != "NaT":
            if (res[7] == 'A1' or res[7] == 'A2') and (res[8] == 'A1' or res[8] == 'A2'):
                cat_1 += 1
                group = 1
            elif (res[7] == 'A3' or res[7] == 'A4') and (res[8] == 'A2' or res[8] =='A1'):
                cat_2 += 1
                group = 2
            elif (res[7] == 'A5' or res[7] == 'A4') and (res[8] == 'A4' or res[8] == 'A3'):
                cat_3 += 1
                group = 3
            else:
                rest += 1
                group = 0

            for index, x in enumerate(res):
                clustered_results[list(results_dict.keys())[index]][group].append(x)

            for index, x in enumerate(res):
                results_dict[list(results_dict.keys())[index]].append(x)



    for t in results_dict:
        # if t not in ['id', 'datestamp', 'startdate', 'startlanguage', 'lastpage', 'seed', 'enddate', 'submitdate', 'AIpT03', 'EnvSus05', 'O04']:
        if t in ['XAI01', 'XAI02']:
            count = dict(Counter(results_dict[t]))
            print("Frage %s :" %t, dict(Counter(count)))
            plt.title(t)
            plt.xlabel('Answer', fontsize=20)
            plt.ylabel('Count', fontsize=20)
            keys = sorted(list(count.keys()))
            values = list()
            names = list()
            for k in keys:
                values.append(count[k])
                try:
                    names.append(answer_mapping[t][k])
                except KeyError:
                    names.append(k)
            plt.yscale('linear')
            plt.bar(range(len(count)), values, align='center')
            plt.xticks(range(len(count)), names)
            plt.show()

    for t in clustered_results:
        if t not in ['id', 'datestamp', 'startdate', 'startlanguage', 'lastpage', 'seed', 'enddate', 'submitdate', 'XAI01', 'XAI02', 'AIpT03', 'EnvSus05', 'O04']:
            value_list = list()
            for cl_key in clustered_results[t]:
                print("Cluster: ", cl_key)
                print(cl_key, t)
                count = dict(Counter(clustered_results[t][cl_key]))
                print("Frage %s :" %t, dict(Counter(count)))
                keys = sorted(answer_mapping[t].keys())
                values = list()
                names = list()
                for k in keys:
                    if k in count.keys():
                        values.append(count[k])
                    else:
                        values.append(0)
                    try:
                        names.append(answer_mapping[t][k])
                    except:
                        names.append(k)
                value_list.append(values)
                print(values, names)
            
            data = pd.DataFrame({"Cluster 0": value_list[0], "Cluster 1": value_list[1], "Cluster 2": value_list[2], "Cluster 3": value_list[3]}, index=names)
            ax = data.plot.bar(rot=0)

            plt.show()

    wc_results = {'XAI04' : list(), 'EnvSus05': list(), 'O04': list()}

    for res in survey_results:

        if str(res[1]) != 'NaT':

            res[12]
            res[17]
            res[21]
            if str(res[13]) != 'nan':
                wc_results['XAI04'].extend(remove_noise(word_tokenize(res[13])))
            if str(res[18]) != 'nan':
                wc_results['EnvSus05'].extend(remove_noise(word_tokenize(res[18])))
            if str(res[22]) != 'nan':
                wc_results['O04'].extend(remove_noise(word_tokenize(res[22])))

            if res[6] != res[5]:
                work_lens.append((res[6] - res[5]).total_seconds())


    wc_results['XAI04'] = Counter(wc_results['XAI04'])
    wordcloud = WordCloud()
    wordcloud.generate_from_frequencies(frequencies=wc_results['XAI04'])
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    wc_results['EnvSus05'] = Counter(wc_results['EnvSus05'])

    wordcloud = WordCloud()
    wordcloud.generate_from_frequencies(frequencies=wc_results['EnvSus05'])
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")

    wc_results['O04'] = Counter(wc_results['O04'])
    wordcloud = WordCloud()
    wordcloud.generate_from_frequencies(frequencies=wc_results['O04'])
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")

    plt.show()


    avg_work_len = int((sum(work_lens) / len(results_dict['id'])))
    median_work_len = int(statistics.median(work_lens))

    print("participants: ", len(results_dict['id']))
    print("avgerage working time: %s min" %str(datetime.timedelta(seconds=avg_work_len)))
    print("median working time: %s min" %str(datetime.timedelta(seconds=median_work_len)))
    print("group 1: ", cat_1)
    print("group 2: ", cat_2)
    print("group 3: ", cat_3)
    print("rest: ", rest)



if __name__ == '__main__':
    main()