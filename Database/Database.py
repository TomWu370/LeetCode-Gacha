import sqlite3
from DataSource import Leetscore
from ProgramUtil.ReadConfig import readWheelDefault

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

try:
    USER = Leetscore.getUsername()
except Exception:
    USER = "Default"


def read(fetchData=None):
    rows = cursor.execute("SELECT username, easy, medium, hard, used FROM leetData WHERE username = ?", (USER,)).fetchall()
    if not rows:
        # fetch and update data
        if not fetchData:
            fetchData = Leetscore.getQuestions()  # get data from api
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


def spend(amount=1, cost=None):
    rows = read()
    if not cost:
        cost = reward_config['cost']
    usable, _ = getUsable(rows)
    if usable >= cost * amount:
        used = cost * amount  # default 1, to allow for multi spend
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


def refresh(data=None):
    if not data:
        data = Leetscore.getQuestions()
    update(data)
    usable, _ = getUsable()
    return data, usable



if __name__ == '__main__':
    # run this file to reset currency
    resetUsed()
