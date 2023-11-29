import sqlite3
import leetscore
from readConfig import readWheelDefault

reward_config = readWheelDefault()

connection = sqlite3.connect("database.db")
# allows return rows to be converted to dictionary
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
try:
    cursor.execute("CREATE TABLE leetData (username VARCHAR, easy INTEGER, medium INTEGER, hard INTEGER, used INTEGER)")
    connection.commit()
except sqlite3.OperationalError:
    pass

USER = leetscore.getUsername()


def read():
    rows = cursor.execute("SELECT username, easy, medium, hard, used FROM leetData WHERE username = ?", (USER,)).fetchall()
    if not rows:
        # fetch and update data
        fetchData = leetscore.getQuestions()  # get data from api
        cursor.execute("INSERT INTO leetData VALUES (?, ?, ?, ?, ?)",
                       (USER, fetchData['easy'], fetchData['medium'], fetchData['hard'], 0))
        connection.commit()
        return read()
    return dict(rows[0])


def update(data, used=0, rows=None):
    if not rows:
        rows = read()
    used += rows['used']
    cursor.execute(
        "UPDATE leetData SET easy = ?, medium = ?, hard = ?, used = ? WHERE username = ?",
        (data['easy'], data['medium'], data['hard'], used, USER))
    # commit the changes
    connection.commit()
    # take difference between each tier then add amount of points for each tier


def set(data, used=0):
    cursor.execute(
        "UPDATE leetData SET easy = ?, medium = ?, hard = ?, used = ? WHERE username = ?",
        (data['easy'], data['medium'], data['hard'], used, USER))
    # commit the changes
    connection.commit()


def resetUsed(used=0):
    # reset the total used to 0 or defined value
    cursor.execute(
        "UPDATE leetData SET used = ? WHERE username = ?",
        (used, USER))
    # commit the changes
    connection.commit()


def spend():
    rows = read()
    usable, _ = getUsable(rows)
    if usable >= reward_config['cost'] * 1:
        used = reward_config['cost'] * 1  # 1 equal to amount
        update(rows, used, rows)
        return True
    else:
        # Not enough
        return False


def getUsable(rows=None):
    if not rows:
        rows = read()
    total = (rows['easy'] * reward_config['easy_point']) + \
            (rows['medium'] * reward_config['medium_point']) + \
            (rows['hard'] * reward_config['hard_point'])
    usable = total - rows['used']
    return usable, rows


def refresh():
    data = leetscore.getQuestions()
    usable, rows = getUsable()
    update(data, rows=rows)
    return data, usable

resetUsed()
#data = {'easy': 2, 'medium': 2, 'hard': 4}
# data2 = {'easy': 5, 'medium': 2, 'hard': 4}
# # initialise
# cursor.execute(
#     "UPDATE leetData SET easy = ?, medium = ?, hard = ?, used = ? WHERE username = ?",
#     (data['easy'], data['medium'], data['hard'], 0, USER))
# connection.commit()
# print(f'read: ',read())
# print(f'money start: ', getUsable())
# print(f'read: ',read())
# set(dat, 0)
# print(f'read: ', read())
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
