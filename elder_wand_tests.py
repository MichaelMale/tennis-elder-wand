import unittest
import pandas as pd
from collections import deque
from tennis_data import get_tennis_data, find_transfers


class TestTennisData(unittest.TestCase):

    def test_get_tennis_data(self):
        """Test get_tennis_data function"""
        data = get_tennis_data(2016, 'wta')
        self.assertIsInstance(data, pd.DataFrame)
        self.assertNotEqual(data.shape[0], 0)  # Check if data frame is not empty
        self.assertEqual(data.columns.tolist(),
                         ['tourney_name', 'tourney_date', 'winner_name', 'loser_name', 'score', 'round', 'match_num'])

    def test_get_tennis_data_invalid_year(self):
        """Test get_tennis_data function with invalid year"""
        with self.assertRaises(ValueError):
            get_tennis_data(1900, 'atp')

    def test_get_tennis_data_invalid_tour(self):
        """Test get_tennis_data function with invalid tour"""
        with self.assertRaises(ValueError):
            get_tennis_data(2016, 'invalid')

    def test_find_transfers(self):
        """Test find_transfers function"""
        data = get_tennis_data(2016, 'wta')
        initial_holder = data.iloc[0]['winner_name']
        elder_wand = deque()
        elder_wand.append(data.iloc[0].tolist())  # add the first match data

        find_transfers(data, initial_holder, elder_wand)

        self.assertNotEqual(len(elder_wand), 0)  # Check if elder_wand is not empty
        self.assertEqual(elder_wand[0][2], initial_holder)  # Check if the initial holder is correct


if __name__ == '__main__':
    unittest.main()
