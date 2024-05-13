import hashlib
import time


def generate_otp(secret_key, interval=120, length=6, only_digits=True):
    """
    Generate a time-based OTP using SHA-256 hashing algorithm.

    Args:
    secret_key (str): Secret key used for hashing.
    interval (int): Time interval in seconds for OTP validity. Default is 120 seconds (2 minutes).
    length (int): Length of OTP. Default is 6 (6 digits). Maximum 8 digits. Minimum 4 digits.
    only_digits (bool): If True, only digits are used for OTP. Default is True.

    Returns:
    str: Generated OTP.
    """
    # Validating the length. Maximum 8 is allowed. 6 will assign if count gave more than 8.
    length = length if 9 > length > 3 else 6

    # Getting current time based on interval. This will use for generate one OTP based on secret at particular interval.
    current_time = int(time.time() / interval)

    # Generating hash
    otp_hash = hashlib.sha256((str(current_time) + secret_key).encode()).hexdigest()

    # Getting only digits from hash
    otp_numeric = ''.join(char for char in otp_hash if char.isdigit())

    # Digit or mixed OTP based on only_digits
    otp = otp_numeric[:length] if only_digits else otp_hash[:length]  # Return the first 6 characters as the OTP
    
    return otp
