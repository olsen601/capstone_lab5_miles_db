import mileage
import sqlite3
from unittest import TestCase

class TestMileageDB(TestCase):

    test_db_url = 'test_miles.db'

    # The name of this method is important - the test runner will look for it
    def setUp(self):
        # Overwrite the mileage
        mileage.db_url = self.test_db_url
        # drop everything from the DB to always start with an empty database
        conn = sqlite3.connect(self.test_db_url)
        conn.execute('DELETE FROM miles')
        conn.commit()
        conn.close()


    def test_add_new_vehicle(self):
        mileage.add_miles('Blue Car', 100)
        expected = { 'BLUE CAR': 100 }
        self.compare_db_to_expected(expected)

        mileage.add_miles('Green Car', 50)
        expected['GREEN CAR'] = 50
        self.compare_db_to_expected(expected)


    def test_increase_miles_for_vehicle(self):
        mileage.add_miles('Red Car', 100)
        expected = { 'RED CAR': 100 }
        self.compare_db_to_expected(expected)

        mileage.add_miles('Red Car', 50)
        expected['RED CAR'] = 100 + 50
        self.compare_db_to_expected(expected)


    def test_increase_miles_with_cap_variation(self):
        mileage.add_miles('Purple Car', 100)
        expected = { 'PURPLE CAR': 100 }
        self.compare_db_to_expected(expected)

        mileage.add_miles('pUrPlE cAr', 50)
        expected['PURPLE CAR'] = 100 + 50
        self.compare_db_to_expected(expected)

        mileage.add_miles('PurPLe CAr', 50)
        expected['PURPLE CAR'] = 100 + 50 + 50
        self.compare_db_to_expected(expected)

        mileage.add_miles('PURPLE CAR', 50)
        expected['PURPLE CAR'] = 100 + 50 + 50 + 50
        self.compare_db_to_expected(expected)


    def test_add_new_vehicle_no_vehicle(self):
        with self.assertRaises(Exception):
            mileage.addMiles(None, 100)


    def test_add_new_vehicle_invalid_new_miles(self):
        with self.assertRaises(Exception):
            mileage.addMiles('Car', -100)
        with self.assertRaises(Exception):
            mileage.addMiles('Car', 'abc')
        with self.assertRaises(Exception):
            mileage.addMiles('Car', '12.def')


    # This is not a test method, instead, it's used by the test methods
    def compare_db_to_expected(self, expected):

        conn = sqlite3.connect(self.test_db_url)
        cursor = conn.cursor()
        all_data = cursor.execute('SELECT * FROM MILES').fetchall()

        # Same rows in DB as entries in expected dictionary
        self.assertEqual(len(expected.keys()), len(all_data))

        for row in all_data:
            # Vehicle exists, and mileage is correct
            self.assertIn(row[0], expected.keys())
            self.assertEqual(expected[row[0]], row[1])

        conn.close()


class TestSearchMileageDB(TestCase):

    test_db_url = 'test_miles.db'

    # The name of this method is important - the test runner will look for it
    def setUp(self):
        # Overwrite the mileage
        mileage.db_url = self.test_db_url
        # drop everything from the DB to always start with an empty database
        conn = sqlite3.connect(self.test_db_url)
        conn.execute('DELETE FROM miles')
        conn.commit()
        cursor = conn.cursor()
        mileage.add_miles('Blue Car', 100)
        mileage.add_miles('Green Car', 200)
        mileage.add_miles('Red Car', 300)
        conn.commit()
        conn.close()


    def test_search_vehicles(self):
        bcm = mileage.search('blue car')
        expected = { 'BLUE CAR': bcm[0] }

        gcm = mileage.search('green car')
        expected['GREEN CAR'] = gcm[0]

        rcm = mileage.search('red car')
        expected['RED CAR'] = rcm[0]
        self.compare_db_to_expected(expected)


    def test_invalid_search_vehicle(self):
        wcm = mileage.search('white car')
        self.assertIsNone(wcm)


    # This is not a test method, instead, it's used by the test methods
    def compare_db_to_expected(self, expected):

        conn = sqlite3.connect(self.test_db_url)
        cursor = conn.cursor()
        all_data = cursor.execute('SELECT * FROM MILES').fetchall()

        # Same rows in DB as entries in expected dictionary
        self.assertEqual(len(expected.keys()), len(all_data))

        for row in all_data:
            # Vehicle exists, and mileage is correct
            self.assertIn(row[0], expected.keys())
            self.assertEqual(expected[row[0]], row[1])

        conn.close()
