import unittest

from app import app
from tasks.routes import *
from tasks.exceptions import *


class TaskTest(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client(self)

    def test_url_fetch_status_code(self):
        """Yandex url should return ok status."""
        with app.app_context():
            try:
                fetch_address_info('mkad')
            except RemoteResponseException:
                self.fail('Yandex url call invalid response')

    def test_valid_location_not_empty_result(self):
        """Valid location fetch should not return an empty result."""
        samples = ['mkad', 'moscow', 'lagos']
        with app.app_context():
            try:
                for sample in samples:
                    members = get_address_members(sample)
                    self.assertTrue(len(members) > 0)
            except Exception:
                self.fail('Empty result detected for valid locations')

    def test_empty_results_fetch(self):
        """Detect empty result when fetched."""
        wrong_samples = ['kskjldnjhkdbhfbkj', 'jlhkhghjugjhv978', 'khdgfhbhjadf']
        with app.app_context():
            for sample in wrong_samples:
                with self.assertRaises(NoLocationFoundException, msg=f'Exception not raised for empty result'):
                    get_address_members(sample)

    def test_empty_address_input(self):
        """Check empty address inputted."""
        with app.app_context():
            with self.assertRaises(EmptyAddressException):
                fetch_address_info('')
            with self.assertRaises(EmptyAddressException):
                fetch_address_info(None)

    def test_address_is_not_coordinate(self):
        """Inputted address should not be coordinates."""
        wrong_samples = [
            '134.854,-25.828', 'E134.854, S25.828', '134.854E, 25.828S',
            '134°51\'15.88", -25°49\'41.1"',
            '25°49\'41.1"S,134°51\'15.88"E',
            '2549.67,S, 13451.26,E'
        ]
        with app.app_context():
            for sample in wrong_samples:
                with self.assertRaises(InvalidAddressFormatException, msg=f'Exception not raised for "{sample}"'):
                    validate_address_is_not_coordinates(sample)


if __name__ == '__main__':
    unittest.main()
