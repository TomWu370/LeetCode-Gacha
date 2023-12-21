import unittest

from ProgramUtil import ReadConfig


class ReadConfigTest(unittest.TestCase):

    def test_read_default(self):
        # Expected
        expected_cookie = "PlaceSessionCookieHere"
        expected_token = "PlaceCsrfTokenHere"

        # Actual
        actual_cookie, actual_token = ReadConfig.readDefault()

        # Assert
        self.assertEqual(expected_cookie, actual_cookie)
        self.assertEqual(expected_token, actual_token)


    def test_read_screen_default(self):
        # Expected
        expected_aspect = (1600, 900)
        expected_text_gap = 50
        expected_text_width = 100
        expected_text_height = 20

        # Actual
        actual_aspect, actual_text_gap, actual_text_width, actual_text_height = ReadConfig.readScreenDefault()

        # Assert
        self.assertEqual(expected_aspect, actual_aspect)
        self.assertEqual(expected_text_gap, actual_text_gap)
        self.assertEqual(expected_text_width, actual_text_width)
        self.assertEqual(expected_text_height, actual_text_height)


    def test_read_wheel_default(self):
        # Expected
        expected_easy = 100
        expected_medium = 300
        expected_hard = 1000
        expected_cost = 1000
        
        # Actual
        wheel = ReadConfig.readWheelDefault()
        actual_easy = wheel['easy_point']
        actual_medium = wheel['medium_point']
        actual_hard = wheel['hard_point']
        actual_cost = wheel['cost']

        # Assert
        self.assertEqual(expected_easy, actual_easy)
        self.assertEqual(expected_medium, actual_medium)
        self.assertEqual(expected_hard, actual_hard)
        self.assertEqual(expected_cost, actual_cost)


    def test_read_spinner_default(self):
        # Expected
        expected_max_velocity = 3.0
        expected_min_velocity = 2.0
        expected_speed_decay = 0.005
        expected_start_degree = 0.0
        expected_spin_clockwise = True
        expected_spinner_image_path = './Wheel/pointer.png'

        # Actual
        spinner = ReadConfig.readSpinnerDefault()
        actual_max_velocity = spinner[0]
        actual_min_velocity = spinner[1]
        actual_speed_decay = spinner[2]
        actual_start_degree = spinner[3]
        actual_spin_clockwise = spinner[4]
        actual_spinner_image_path = spinner[5]

        # Assert
        self.assertEqual(expected_max_velocity, actual_max_velocity)
        self.assertEqual(expected_min_velocity, actual_min_velocity)
        self.assertEqual(expected_speed_decay, actual_speed_decay)
        self.assertEqual(expected_start_degree, actual_start_degree)
        self.assertEqual(expected_spin_clockwise, actual_spin_clockwise)
        self.assertEqual(expected_spinner_image_path, actual_spinner_image_path)


    def test_read_customisation_default(self):
        # Expected
        expected_stat_background = (125,255,255)
        expected_result_text = (0,255,0)
        expected_retry_text = (125,125,0)
        expected_insufficient_text = (255,0,0)

        # Actual
        customisation = ReadConfig.readCustomisationDefault()
        actual_stat_background = customisation['stat_background']
        actual_result_text = customisation['result_text']
        actual_retry_text = customisation['retry_text']
        actual_insufficient_text = customisation['insufficient_text']

        # Assert
        self.assertEqual(expected_stat_background, actual_stat_background)
        self.assertEqual(expected_result_text, actual_result_text)
        self.assertEqual(expected_retry_text, actual_retry_text)
        self.assertEqual(expected_insufficient_text, actual_insufficient_text)



    def test_read_rates(self):
        # Expected
        expected_choices = ['choice 1', 'choice 2', 'choice 3', 'choice 4']
        expected_weights = [1, 2, 2, 4]

        # Actual
        choices, weights = ReadConfig.readRates()

        # Assert
        self.assertEqual(expected_choices, choices)
        self.assertEqual(expected_weights, weights)


if __name__ == '__main__':
    # Note that this test will only work with default configs and rates
    unittest.main()
