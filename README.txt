I'm less familiar with Python, but the following libraries are not native to built in python libraries and need to be installed for the program and test suite to work. Forgive me if the format for these requirements or instructions is incorrect. I've never worked with python, or anything related to this assignment before so I'm ignorant of best practices.

1. http.server
2. Crypto.PublicKey.RSA
3. urllib.parse.urlparse
4. urllib.parse.parse_qs
5. base64
6. json
7. jwt
8. datetime
9. requests

To run the code, the provided files must be in the same directory and the methods must be installed in the terminal. Once they are, run the main server with the following command

python server.py

I've found that it usually takes a minute or two for the server to start up so some tests with the test code or the auto grader may fail. 

Once it's running, the auto grader can be run with the following command.

go run main.go project1

The test suite can be run with the following command.

python test_python.py

I hope that this can get replicated on other devices. It was a miracle it's working on mine. I did my absolute best with this assignment, but I started the assignment with no previous experiance with any individual component of it.