import sqlite3

config = {'easy': 100, 'medium': 300, 'hard': 1000, 'cost':1000}
EASY, MEDIUM, HARD, USED = 0, 1, 2, 3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()
# cursor.execute("CREATE TABLE leetData (easy INTEGER, medium INTEGER, hard INTEGER, used INTEGER)")

def read():
    rows = cursor.execute("SELECT easy, medium, hard, used FROM leetData").fetchall()
    if not rows:
        # fetch and update data
        data = {'easy': 2, 'medium': 2, 'hard': 4} # get data from api
        cursor.execute("INSERT INTO leetData VALUES (?, ?, ?, ?)",
                       (data['easy'], data['medium'], data['hard'], 0))
    return rows[0]


def update(data, used=0):
    rows = read()
    used += rows[USED]
    cursor.execute(
        "UPDATE leetData SET easy = ?, medium = ?, hard = ?, used = ?",
        (data['easy'], data['medium'], data['hard'], used))
    # take difference between each tier then add amount of points for each tier


def spend():
    rows = read()
    usable = getUsable(rows)
    if usable >= config['cost'] * 1:
        used = config['cost'] * 1 # 1 equal to amount
        update(data, used)
    else:
        print('not enough')

def getUsable(rows = None):
    if not rows:
        rows = read()
    total = (rows[EASY] * config['easy']) + \
            (rows[MEDIUM] * config['medium']) + \
            (rows[HARD] * config['hard'])
    usable = total - rows[USED]
    return usable

data = {'easy': 2, 'medium': 2, 'hard': 4}
# initialise
cursor.execute(
    "UPDATE leetData SET easy = ?, medium = ?, hard = ?, used = ?",
    (data['easy'], data['medium'], data['hard'], 0))
print(f'read: ',read())
print(f'money start: ', getUsable())
update(data, 0)
spend()
print(f'money end: ', getUsable())
