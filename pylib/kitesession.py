"""
This module provides a Python interface for interacting with the Kite trading API
using a Go-based backend. It allows for generating a Kite session and checking
the validity of an enctoken.

The module uses a shared library (kitesession.so on Linux/macOS or kitesession.dll on Windows)
which must be present in the same directory as this script or in a directory
included in the system's library path.
"""

import ctypes
import json
import os
import platform


def load_library():
    """
    Load the appropriate shared library based on the operating system.

    Returns:
        ctypes.CDLL: Loaded shared library object.

    Raises:
        OSError: If the shared library cannot be loaded.
    """
    if platform.system() == "Windows":
        return ctypes.CDLL("./kitesession.dll")
    else:  # Linux, macOS, and other UNIX-like OS
        return ctypes.CDLL("./kitesession.so")


# Load the shared library
lib = load_library()

# Define argument and return types for the functions
lib.GenerateSession.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
lib.GenerateSession.restype = ctypes.c_char_p
lib.CheckEnctokenValid.argtypes = [ctypes.c_char_p]
lib.CheckEnctokenValid.restype = ctypes.c_char_p
lib.SetDebug.argtypes = [ctypes.c_int]
lib.FreeString.argtypes = [ctypes.c_char_p]


class KiteSession:
    """
    A class to interact with the Kite trading API using a Go-based backend.

    This class provides methods to generate a Kite session and check the validity
    of an enctoken.
    """

    @staticmethod
    def generate_session(user_id: str, password: str, totp_secret: str) -> dict:
        """
        Generate a new Kite session.

        Args:
            user_id (str): The Kite user ID.
            password (str): The Kite account password.
            totp_secret (str): The TOTP secret for two-factor authentication.

        Returns:
            dict: A dictionary containing the session information.

        Raises:
            Exception: If there's an error generating the session.
        """
        result = lib.GenerateSession(
            user_id.encode('utf-8'),
            password.encode('utf-8'),
            totp_secret.encode('utf-8')
        )
        result_str = ctypes.string_at(result).decode('utf-8')

        if result_str.startswith('error:'):
            raise Exception(result_str[6:])

        return json.loads(result_str)

    @staticmethod
    def check_enctoken_valid(enctoken: str) -> bool:
        """
        Check if the given enctoken is valid.

        Args:
            enctoken (str): The enctoken to check.

        Returns:
            bool: True if the enctoken is valid, False otherwise.

        Raises:
            Exception: If there's an error checking the enctoken.
        """
        result = lib.CheckEnctokenValid(enctoken.encode('utf-8'))
        result_str = ctypes.string_at(result).decode('utf-8')

        if result_str.startswith('error:'):
            raise Exception(result_str[6:])

        return result_str.lower() == 'true'

    @staticmethod
    def set_debug(debug: bool):
        """
        Set the debug mode for the Kite session.

        Args:
            debug (bool): True to enable debug mode, False to disable.
        """
        lib.SetDebug(int(debug))


def get_env_var(var_name: str) -> str:
    """
    Get the value of an environment variable.

    Args:
        var_name (str): The name of the environment variable.

    Returns:
        str: The value of the environment variable.

    Raises:
        ValueError: If the environment variable is not set.
    """
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"Environment variable {var_name} is not set")
    return value


# Example usage
if __name__ == "__main__":
    KiteSession.set_debug(False)

    try:
        # Read environment variables
        USER_ID = get_env_var("KITE_USER_ID")
        PASSWORD = get_env_var("KITE_PASSWORD")
        TOTP_SECRET = get_env_var("KITE_TOTP_SECRET")
        print("-" * 50)
        print("Environment variables:")
        print("-" * 50)
        print(f"KITE_USER_ID: {USER_ID}")
        print(f"KITE_PASSWORD: {PASSWORD}")
        print(f"KITE_TOTP_SECRET: {TOTP_SECRET}")
        print()

        session = KiteSession.generate_session(USER_ID, PASSWORD, TOTP_SECRET)
        print("-" * 50)
        print("Session generated:")
        print("-" * 50)
        print(json.dumps(session, indent=2))
        print()

        is_valid = KiteSession.check_enctoken_valid(session['enctoken'])
        print("-" * 50)
        print("Enctoken valid:", is_valid)
        print("-" * 50)
    except Exception as e:
        print("-" * 50)
        print("Error:", str(e))
        print("-" * 50)
