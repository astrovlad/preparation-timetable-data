import pandas as pd
import requests

import authorization


def fix_eng(lessons):
    url_group = authorization.get_url() + "/timetable/group/?limit=1000&offset=0"
    r = requests.get(url_group, headers=authorization.headers)
    groups = r.json()['items']
    groups = pd.DataFrame(groups)
    print(groups)

    new_lessons = []

    n_lessons = []
    for i, row in lessons.iterrows():
        row['place'] = [int(row['place'])] if not pd.isna(row["place"]) else []
        if not isinstance(row["teacher"], list):
            row['teacher'] = []
            print("yes")
        n_lessons.append(row)

    lessons = pd.DataFrame(n_lessons)
    lessons.to_excel("test.xlsx", "List")

    for i, group in groups.iterrows():
        for j in range(7):
            table = []

            for k, row in lessons.iterrows():
                if row['group'] == group[0] and row['weekday'] == j:
                    table.append(row)
            table = pd.DataFrame(table)


            row1 = pd.DataFrame()
            ar = []
            boo = False


            for k, row in table.iterrows():
                if "странный язык" in row['subject']:
                    row1 = row
                    boo = True
                    ar.append(k)
                    break

            for k, row in table.iterrows():
                if row['teacher'] != []:
                    if "странный язык" in row['subject'] and row['teacher'][0] != row1['teacher'][0]:
                        ar.append(k)
                        row1['teacher'].append(row['teacher'][0])
                        row1['place'].append(row['place'][0])

            table.drop(labels=ar, axis=0, inplace=True)
            if boo:
                new_lessons.append(row1)

            for k, row in table.iterrows():
                new_lessons.append(row)


    new_lessons = pd.DataFrame(new_lessons)
    return new_lessons
