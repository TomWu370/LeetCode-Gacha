import sqlite3

config = {'easy': 100, 'medium': 300, 'hard': 1000, 'cost':1000}
EASY, MEDIUM, HARD, USED = 0, 1, 2, 3

connection = sqlite3.connect("database.db")
# allows return rows to be converted to dictionary
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
try:
    cursor.execute("CREATE TABLE leetData (easy INTEGER, medium INTEGER, hard INTEGER, used INTEGER)")
except sqlite3.OperationalError:
    pass

def read():
    rows = cursor.execute("SELECT easy, medium, hard, used FROM leetData").fetchall()
    if not rows:
        # fetch and update data
        data = {'easy': 2, 'medium': 2, 'hard': 4} # get data from api
        cursor.execute("INSERT INTO leetData VALUES (?, ?, ?, ?)",
                       (data['easy'], data['medium'], data['hard'], 0))
    return dict(rows[0])


def update(data, used=0):
    rows = read()
    used += rows['used']
    cursor.execute(
        "UPDATE leetData SET easy = ?, medium = ?, hard = ?, used = ?",
        (data['easy'], data['medium'], data['hard'], used))
    # take difference between each tier then add amount of points for each tier


def spend():
    rows = read()
    usable = getUsable(rows)
    if usable >= config['cost'] * 1:
        used = config['cost'] * 1 # 1 equal to amount
        update(rows, used)
    else:
        print('not enough')

def getUsable(rows = None):
    if not rows:
        rows = read()
    total = (rows['easy'] * config['easy']) + \
            (rows['medium'] * config['medium']) + \
            (rows['hard'] * config['hard'])
    usable = total - rows['used']
    return usable

# data = {'easy': 2, 'medium': 2, 'hard': 4}
# data2 = {'easy': 5, 'medium': 2, 'hard': 4}
# # initialise
# cursor.execute(
#     "UPDATE leetData SET easy = ?, medium = ?, hard = ?, used = ?",
#     (data['easy'], data['medium'], data['hard'], 0))
# print(f'read: ',read())
# print(f'money start: ', getUsable())
# update(data, 0)
# spend()
# print(f'spend 1: ', getUsable())
# spend()
# print(f'spend 2: ', getUsable())
# spend()
# print(f'spend 3: ', getUsable())
# spend()
# print(f'spend 4: ', getUsable())
# spend()
# print(f'spend 5: ', getUsable())
# update(data2)
# print(f'update 1: ', getUsable())
# spend()
# print(f'spend 6: ', getUsable())
# print(f'money end: ', getUsable())

# test cases
# new to leetcode, database should be 0,0,0,0
# experienced, but no spending 3,4,5,0
# experienced, 2,3,4,1000
# buying when have enough
# buying when not enough
# when buying always update
# when pressing update button, update
# on startup update