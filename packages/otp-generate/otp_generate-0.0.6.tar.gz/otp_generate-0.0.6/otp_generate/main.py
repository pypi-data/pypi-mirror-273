import hashlib
import time


def generate_otp(secret_key, interval=None, length=6, only_digits=True):
    try:
        if isinstance(secret_key, int):
            _secret_key = str(secret_key)
            # pre define minutes
            minutes = 60
            if interval:
                interval = interval * minutes
            if interval == 0:
                raise ValueError("Zero minute was not allowed.")
            else:
                interval = 2 * minutes
            """
            Generate a time-based OTP using SHA-256 hashing algorithm.
            Args:
            secret_key (str): Secret key used for hashing.
            interval (int): Time interval in seconds for OTP validity. Default is 300 seconds (5 minutes).
            Returns:
            str: Generated OTP.
            """
            current_time = int(time.time() / interval)
            otp = hashlib.sha256((str(current_time) + _secret_key).encode()).hexdigest()
            otp_numeric = ''.join(char for char in otp if char.isdigit())
            otp = otp_numeric[:length] if only_digits else otp[:length]
            return otp  # Return OTP
        else:
            raise TypeError("Invalid secret_key, Please enter valid integer format")
    except Exception as _err:
        raise ImportError(
            f"import error"
        ) from _err


def package_check():
    print("Hello from otp-package")
