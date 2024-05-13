import time
import unittest
from ownotp.otp import generate_otp


class TestOTP(unittest.TestCase):
    def test_generate_otp(self):
        otp_one = generate_otp('your_own_secret')
        time.sleep(15)
        otp_two = generate_otp('your_own_secret')
        self.assertEqual(otp_one, otp_two)

    def test_generate_otp_digit(self):
        otp = generate_otp('your_own_secret')
        self.assertEqual(otp.isdigit(), True)

    def test_generate_otp_not_digit(self):
        otp = generate_otp('your_own_secret', only_digits=False, interval=10)
        self.assertEqual(otp.isdigit(), False)


if __name__ == '__main__':
    unittest.main()
