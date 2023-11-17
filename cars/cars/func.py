import sqlite3


def pars_xml():
    '''парсим файл с машинами'''
    d = dict()
    with open('../cars.xml', encoding='UTF-8') as file:
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
    print(data)
    conn = sqlite3.connect('cars/cars.sqlite')
    cursor = conn.cursor()
    for i in data:
        print('Печатаем i:', i)
        cursor.execute('INSERT INTO marks (mark) VALUES (?)', (i, ))
        for j in data[i]:
            print('Печатаем j:', j)
            cursor.execute(
                '''INSERT INTO models (model, mark_id)
                VALUES (?, (SELECT mark_id FROM marks WHERE mark = ?))''', (j, i)
                )
    conn.commit()
    cursor.close()
    conn.close()


create_db()
fill_db()