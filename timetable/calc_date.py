import pandas as pd
from datetime import timedelta, datetime


def calc_date(lessons, semester_begin, semester_end):
    begin = datetime.strptime(semester_begin, "%m/%d/%Y")
    end = datetime.strptime(semester_end, "%m/%d/%Y")

    day_number = (end-begin).days
    lessons_new = []

    for i in range(day_number):
        num = ((i + begin.weekday() + 1)//7 + 1) % 2
        for j, row in lessons.iterrows():
            if (num == 1 and row['odd']) or (num == 0 and row['even']):
                row_new = row
                day = begin + timedelta(days=i)
                if row['weekday'] == day.weekday():

                    hours_start, minutes_start = row['start'].split(':')
                    hours_end, minutes_end = row['end'].split(':')

                    date_start = day + timedelta(hours=int(hours_start), minutes=int(minutes_start))
                    date_end = day + timedelta(hours=int(hours_end), minutes=int(minutes_end))

                    date_start_ = datetime.strftime(date_start, "%Y-%m-%dT%H:%M:%SZ")
                    date_end_ = datetime.strftime(date_end, "%Y-%m-%dT%H:%M:%SZ")

                    row_new['start'] = date_start_
                    row_new['end'] = date_end_

                    lessons_new.append(row_new)

    lessons_new = pd.DataFrame(lessons_new)
    lessons_new.pop('odd')
    lessons_new.pop('even')
    lessons_new.pop('weekday')
    lessons_new.pop('num')

    return lessons_new
