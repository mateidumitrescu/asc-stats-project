import unittest
import csv

from app.utilities.utils import (calculate_states_mean,
                                calculate_state_mean,
                                calculate_best5,
                                calculate_worst5,
                                calculate_global_mean,
                                calculate_diff_from_mean,
                                calculate_state_diff_from_mean,
                                calculate_mean_by_category,
                                calculate_state_mean_by_category)


class TestWebserver(unittest.TestCase):
    def setUp(self):
        # getting the data from the csv file
        self.data = []
        with open(file='unittests_data.csv', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.data.append(row)
        
        # dictionary storing each function to be tested
        self.functions = {
            'states_mean': calculate_states_mean,
            'state_mean': calculate_state_mean,
            'best5': calculate_best5,
            'worst5': calculate_worst5,
            'global_mean': calculate_global_mean,
            'diff_from_mean': calculate_diff_from_mean,
            'state_diff_from_mean': calculate_state_diff_from_mean,
            'mean_by_category': calculate_mean_by_category,
            'state_mean_by_category': calculate_state_mean_by_category
        }
    
    def tearDown(self):
        return super().tearDown()
    
    def test_states_mean(self):
        data_received = {
            "question": "Percent of adults aged 18 years and older who have an overweight classification"
        }
        result = self.functions['states_mean'](self.data, data_received)
        self.assertEqual(result, {})
    
    def test_state_mean(self):
        data_received = {
            "question": "Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)", "state": "Tennessee"
        }
        result = self.functions['state_mean'](self.data, data_received)
        self.assertEqual(result, {'Tennessee': 39.0})
    
    def test_best5(self):
        data_received = {
            "question": "Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)"
        }
        result = self.functions['best5'](self.data, data_received)
        self.assertEqual(result, {'West Virginia': 31.1, 'Tennessee': 39.0})
    
    def test_worst5(self):
        data_received = {
            "question": "Percent of adults who engage in no leisure-time physical activity"
        }
        result = self.functions['worst5'](self.data, data_received)
        self.assertEqual(result, {'Wisconsin': 24.0, 'Kansas': 28.7, 'Nebraska': 31.5, 'Ohio': 31.6, 'Maryland': 38.4})
     
    def test_global_mean(self):
        data_received = {
            "question": "Percent of adults who report consuming vegetables less than one time daily"
        }
        result = self.functions['global_mean'](self.data, data_received)
        self.assertEqual(result, {'global_mean': 35.4})
    
    def test_diff_from_mean(self):
        data_received = {
            "question": "Percent of adults aged 18 years and older who have obesity", "state": "Washington"
        }
        result = self.functions['diff_from_mean'](self.data, data_received)
        self.assertEqual(result, {'New Mexico': 6.033333333333328, 'Ohio': 4.333333333333329, 'Tennessee': -10.366666666666674})
        
    def test_state_diff_from_mean(self):
        data_received = {
            "question": "Percent of adults who report consuming vegetables less than one time daily", "state": "Rhode Island"
        }
        result = self.functions['state_diff_from_mean'](self.data, data_received)
        self.assertEqual(result, {'Rhode Island': 35.4})
    
    def test_mean_by_category(self):
        data_received = {
            "question": "Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)"
        }
        result = self.functions['mean_by_category'](self.data, data_received)
        self.assertEqual(result, {})
    
    def test_state_mean_by_category(self):
        data_received = {
            "question": "Percent of adults aged 18 years and older who have obesity", "state": "Wisconsin"
        }
        result = self.functions['state_mean_by_category'](self.data, data_received)
        self.assertEqual(result, {'Wisconsin': 0})


from app import webserver
# shutting down the webserver because it is created in app.__init__.py
webserver.tasks_runner.shutdown_event.set()