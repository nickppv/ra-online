import sqlite3


def pars_xml():
    '''парсим файл с машинами'''
    d = dict()
    with open('cars/cars.xml', encoding='UTF-8') as file:
        string = 'Hi!'
        while string != '':
            string = file.readline().strip()
            if string.startswith('<mark name='):
                name = string.lstrip('<mark name="').split('"')[0]
                d[name] = set()
            if string.startswith('<folder name="'):
                model = string.lstrip('<folder name="').split('"')[0]
                if ', ' in model:
                    model = model.split(',')[0]
                d[name].add(model)
    return d


def create_db():
    '''создаем БД и таблицы'''

    conn = sqlite3.connect('cars/cars.sqlite')
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS marks (
            mark_id INTEGER PRIMARY KEY,
            mark VARCHAR(30))'''
            )
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS models (
            model_id INTEGER PRIMARY KEY,
            model VARCHAR(50),
            mark_id INTEGER,
            FOREIGN KEY (mark_id) REFERENCES marks (mark_id))'''
            )
    cursor.close()
    conn.close()


def fill_db():
    '''заполняем БД данными из словаря'''

    data = pars_xml()
    conn = sqlite3.connect('cars/cars.sqlite')
    cursor = conn.cursor()
    for i in data:
        cursor.execute('INSERT INTO marks (mark) VALUES (?)', (i, ))
        for j in data[i]:
            cursor.execute(
                '''INSERT INTO models (model, mark_id)
                VALUES (?, (SELECT mark_id FROM marks WHERE mark = ?))''', (j, i)
                )
    cursor.execute('''SELECT mark FROM marks''')
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return result


def get_marks():
    '''выводим все марки на главную страницу'''

    conn = sqlite3.connect('cars/cars.sqlite')
    cursor = conn.cursor()
    cursor.execute('''SELECT mark FROM marks''')
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    result = [i[0] for i in result]
    return result


def get_list_cars(mark):
    conn = sqlite3.connect('cars/cars.sqlite')
    cursor = conn.cursor()
    cursor.execute('''SELECT model
                   FROM marks INNER JOIN models
                   ON marks.mark_id = models.mark_id
                   WHERE marks.mark = ?''', (mark, ))
    result = sorted(list(set(i[0] for i in cursor.fetchall())))
    result = {mark: result}
    print(result)
    cursor.close()
    conn.close()
    return result


def truncate():
    '''удаляем все записи из таблиц'''

    conn = sqlite3.connect('cars/cars.sqlite')
    cursor = conn.cursor()
    cursor.execute('TRUNCATE TABLE marks')
    cursor.execute('TRUNCATE TABLE models')
    conn.commit()
    cursor.close()
    conn.close()


create_db()
fill_db()