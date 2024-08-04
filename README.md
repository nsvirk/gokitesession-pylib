# Golang binary for Python binding for kitesession

This library provides a Python interface to interact with the Kite trading API using a Go-based backend. It allows you to generate a Kite session and check the validity of an enctoken.

## Prerequisites

- Go 1.16 or later
- Python 3.6 or later
- Git (for cloning the repository)

## Building the Shared Library

1. Clone the repository:

   ```
   git clone https://github.com/nsvirk/gokitesession-pylib.git
   cd gokitesession-pylib
   ```

2. Build the shared library:

   For Linux/macOS:

   ```code
   go build -buildmode=c-shared -o pylib/kitesession.so main.go
   ```

   For Windows:

   ```code
   go build -buildmode=c-shared -o pylib/kitesession.dll pylib/main.go
   ```

   This will generate either `kitesession.so` (Linux/macOS) or `kitesession.dll` (Windows) in the pylib directory.

## Python Setup

1. Ensure you have Python 3.6 or later installed.

2. Place the `kitesession.py` file in the same directory as the shared library you just built.

## Usage

1. Set the required environment variables:

   For Linux/macOS:

   ```
   export KITE_USER_ID="your_user_id"
   export KITE_PASSWORD="your_password"
   export KITE_TOTP_SECRET="your_totp_secret"
   ```

   For Windows:

   ```
   set KITE_USER_ID=your_user_id
   set KITE_PASSWORD=your_password
   set KITE_TOTP_SECRET=your_totp_secret
   ```

2. Run the Python script:

   ```
   python3.12 kitesession.py
   ```

   This will generate a session and check if the enctoken is valid.

## Using the Library in Your Own Python Scripts

You can import and use the `KiteSession` class in your own Python scripts:
For python implementaiton see the `kitesession.py` file

## Important Notes

- The shared library file (`kitesession.so` or `kitesession.dll`) must be in the same directory as your Python script or in a directory included in your system's library path.
- This library is for educational purposes only. Use it at your own risk and ensure you comply with Kite's terms of service and API usage guidelines.

## Troubleshooting

If you encounter any issues:

1. Ensure all prerequisites are installed correctly.
2. Verify that the shared library is built correctly and is in the same directory as your Python script.
3. Check that you've set the environment variables correctly.
4. If you're still having problems, please open an issue in the GitHub repository with a detailed description of the error and your environment.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
