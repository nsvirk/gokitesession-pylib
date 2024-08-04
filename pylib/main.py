"""
This script demonstrates the usage of the KiteSession class
from the kite_session module.
"""

import json
from kite_session import KiteSession


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


def main():
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

        # Generate TOTP value
        totp_value = KiteSession.generate_totp_value(TOTP_SECRET)
        print("-" * 50)
        print(f"Generated TOTP value: {totp_value}")
        print("-" * 50)
        print()

        # Generate session
        session = KiteSession.generate_session(USER_ID, PASSWORD, totp_value)
        print("-" * 50)
        print("Session generated:")
        print("-" * 50)
        print(json.dumps(session, indent=2))
        print()

        # Check if enctoken is valid
        is_valid = KiteSession.check_enctoken_valid(session['enctoken'])
        print("-" * 50)
        print("Enctoken valid:", is_valid)
        print("-" * 50)
    except Exception as e:
        print("-" * 50)
        print("Error:", str(e))
        print("-" * 50)


if __name__ == "__main__":
    main()
