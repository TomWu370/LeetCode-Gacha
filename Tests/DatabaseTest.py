import os
import unittest

from Database import Database


class DatabaseTest(unittest.TestCase):

    def test_read(self):
        # Read data from database, if not exist, then fetch and insert data
        Username = 'Tom'
        Data = {'easy': 10, 'medium': 5, 'hard': 3}
        Database.USER = Username
        Database.set(Data, 0)
        readData = Database.read(Data)
        expectedData = {'username': Username, 'easy': Data['easy'], 'medium': Data['medium'], 'hard': Data['hard'],
                        'used': 0}
        self.assertEqual(readData, expectedData)

    def test_update(self):
        # Update data, then change used twice
        Username = 'Tom'
        Data = {'easy': 100, 'medium': 50, 'hard': 10}
        Database.USER = Username
        used = 100
        Database.update(Data, used)
        Database.update(Data, used)
        readData = Database.read(Data)
        expectedData = {'username': Username, 'easy': 100, 'medium': 50, 'hard': 10, 'used': 300}
        self.assertEqual(readData, expectedData)

    def test_set(self):
        # Override records for user with given data values
        Username = 'Tom'
        Data = {'easy': 95, 'medium': 45, 'hard': 5}
        Database.USER = Username
        used = 75
        Database.set(Data, used)
        readData = Database.read(Data)
        expectedData = {'username': Username, 'easy': 95, 'medium': 45, 'hard': 5, 'used': 75}
        self.assertEqual(readData, expectedData)

    def test_resetUsed(self):
        # Set used field to 0 by default or a set value
        Username = 'Tom'
        Database.USER = Username
        Database.resetUsed()
        updatedUsed = Database.read()['used']
        self.assertEqual(updatedUsed, 0)

    def test_spend_sufficient(self):
        # Spend currency, if sufficient, then update used field
        Username = 'Tom'
        Database.USER = Username
        cost = 100
        used = 0
        Data = {'easy': 95, 'medium': 45, 'hard': 5}
        Database.set(Data, used)  # given sufficient currency
        result = Database.spend(1, cost)
        self.assertEqual(result, True)
        self.assertEqual(Database.read()['used'], cost)  # since no currency is spent, spending once = the cost

    def test_spend_insufficient(self):
        # Spend currency, if insufficient, then don't update used field
        Username = 'Tom'
        Database.USER = Username
        cost = 10000
        used = 0
        Data = {'easy': 1, 'medium': 1, 'hard': 1}
        Database.set(Data, used)  # given insufficient currency
        result = Database.spend(1, cost)
        self.assertEqual(result, False)
        self.assertEqual(Database.read()['used'], 0)

    def test_getUsable(self):
        # Get usable currency from database, with some config multipliers
        Username = 'Tom'
        Data = {'easy': 95, 'medium': 45, 'hard': 5}
        used = 0
        Database.USER = Username
        Database.set(Data, used)
        reward_config = Database.reward_config
        expectedUsable = Data['easy'] * reward_config['easy_point']
        expectedUsable += Data['medium'] * reward_config['medium_point']
        expectedUsable += Data['hard'] * reward_config['hard_point']
        usable, _ = Database.getUsable()
        self.assertEqual(expectedUsable, usable)

    def test_refresh(self):
        # Update database with data fetched from leetcode
        Username = 'Tom'
        Database.USER = Username
        Data = {'easy': 50, 'medium': 50, 'hard': 50}
        used = 0
        Database.USER = Username
        Database.set(Data, used)
        readData = Database.read(Data)
        # Check before refresh
        self.assertEqual(readData, {'username': Username, 'easy': 50, 'medium': 50, 'hard': 50, 'used': 0})
        newData = {'easy': 55, 'medium': 50, 'hard': 50}  # User completes 5 more easy leetcode questions
        newReadData, _ = Database.refresh(newData)
        # Check after refresh
        self.assertEqual(newReadData, {'easy': 55, 'medium': 50, 'hard': 50})


if __name__ == '__main__':
    # remove database.db to have fresh test
    try:
        os.remove('database.db')
    except OSError:
        pass

    # run test
    unittest.main()
