from Database import Database


Username = 'Tom'
Data = {'easy':10, 'medium':5, 'hard':3}
Database.USER = Username
readData = Database.read(Data)
print(readData)


used = 100
Database.update()
# set, resetUsed, spend, getUsable, refresh