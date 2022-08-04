import unittest
from unittest.mock import patch
from employee import Employee

class TestEmployee(unittest.TestCase):

    # run only once, at the beginning of the test
    # ideal for populate a database and then remove all when finish
    @classmethod
    def setUpClass(cls) -> None:
        print('setUpClass')

    # run only once, at the end of the test
    @classmethod
    def tearDownClass(cls) -> None:
        print('tearDownClass')

    # run before every single test
    def setUp(self) -> None:
        print('setUp')
        self.emp_1 = Employee('Joao', 'Silva', 2000)
        self.emp_2 = Employee('Neymar', 'Junior', 60000)

    # run after every test
    def tearDown(self) -> None:
        print('teaDown')

    def test_email(self):

        self.assertEqual(self.emp_1.email, 'Joao.Silva@email.com')
        self.assertEqual(self.emp_2.email, 'Neymar.Junior@email.com')

        #chaging name - email should change when name changes
        self.emp_1.first = 'Jose'
        self.emp_2.first = 'Ronaldo'

        self.assertEqual(self.emp_1.email, 'Jose.Silva@email.com')
        self.assertEqual(self.emp_2.email, 'Ronaldo.Junior@email.com')

    def test_fullname(self):

        self.assertEqual(self.emp_1.fullname, 'Joao Silva')
        self.assertEqual(self.emp_2.fullname, 'Neymar Junior')

        #chaging name
        self.emp_1.first = 'Jose'
        self.emp_2.first = 'Ronaldo'

        self.assertEqual(self.emp_1.fullname, 'Jose Silva')
        self.assertEqual(self.emp_2.fullname, 'Ronaldo Junior')

    def test_apply_raise(self):

        self.emp_1.apply_raise()
        self.emp_2.apply_raise()

        self.assertEqual(self.emp_1.pay, 2100)
        self.assertEqual(self.emp_2.pay, 63000)

    def test_month_schedule(self):
        # patch in that case is a context manager
        with patch('employee.requests.get') as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = 'Success'

            schedule = self.emp_1.monthly_schedule('May')
            mocked_get.assert_called_with('http://company.com/Silva/May')
            self.assertEqual(schedule, 'Success')

            #testing bad response
            mocked_get.return_value.ok = False

            schedule = self.emp_2.monthly_schedule('June')
            mocked_get.assert_called_with('http://company.com/Junior/June')
            self.assertEqual(schedule, 'Bad Response!')



if __name__ == '__main__':
    unittest.main()
