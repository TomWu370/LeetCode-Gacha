import unittest

from DataSource import Leetscore


class LeetscoreTest(unittest.TestCase):
    # due to cookies and other differences, Unit test can't test for specific values

    def test_get_username(self):
        username = Leetscore.getUsername()

        # Assert true when returned username is a string and not error
        self.assertEqual(str, type(username))

    def test_get_questions(self):
        questions = Leetscore.getQuestions()

        # Assert true when returned dictionary contains 3 keys and not error
        self.assertEqual(3, len(questions))


if __name__ == '__main__':
    unittest.main()
