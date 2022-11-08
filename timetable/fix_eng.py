import pandas as pd

def multiple_places_to_single(df_):
    for (weekday, group, subject, start), sub_df in df.groupby(['weekday', 'group', 'subject', 'start']):
        if len(sub_df) > 1: # если кол-во пар в одном месте в одно время больше одной
            teachers = sub_df['teacher'].values # список всех преподавателей
            places = sub_df['place'].values # список всех мест
            new_df = sub_df.iloc[0].copy()
            new_df['teacher'] = ', '.join(teachers) # собираем все преподавателей в один список
            new_df['place'] = ', '.join(places) # собираем все места в один список

            indexes = sub_df.index
            df.drop(indexes, axis=0, inplace=True) # убираем старые ряды
            df.loc[len(df)] = new_df # добавляем в исходную таблицу обновленный ряд
    return df
