from http.server import BaseHTTPRequestHandler, HTTPServer #this line implements the BaseHTTPRequestHandler and HTTPServer classes from the http.server module. I understand that the BaseHTTPRequestHandler class is a base class for handling requests and the HTTPServer class is a simple server class. I looked for alternate libraries, but was unable to find one.
from Crypto.PublicKey import RSA #this line imports the RSA module from the Crypto.PublicKey library.
from urllib.parse import urlparse, parse_qs #this line imports urlparse and parse_qs from the urllib.parse module.
import base64 #this line imports the base64 module. I messed around with bitascii a little bit, but ultimately couldn't find a solution that pleased the auto grader. It seems as if the base64 and bitascii modules use different encoding methods that produces a different output for the same input.
import json #this line imports the json module. I understand what json is and have a vague idea of how it is used in python, but have never used it myself.
import jwt #this line imports the jwt module. I have learned about jwt due to this assignment.
import datetime #this line imports the datetime module. Messed around with the time library, but ended up messing around with the base64 encoding.

#all import code must be present. try a different order?

host_name = "localhost" #this line sets the variable h to the string "localhost". The "localhost" value is required for testing on the local machine
port_num = 8080 #this line sets the variable p to the integer 8080. The use of port 8080 is required for the assignment.

private_key = RSA.generate(4096, e=65539) #this line sets the variable private_key to the result of the RSA.generate function call. 4096 is the key size, and 65539 is the public exponent.
expired_key = RSA.generate(4096, e=65539) #this line sets the variable expired_key to the result of the RSA.generate function call. 4096 is the key size, and 65539 is the public exponent.

pem = private_key.export_key(format='PEM') #this line sets the variable pem to the result of the private_key.export_key function call. The format is set to 'PEM'.
expired_pem = expired_key.export_key(format='PEM') #this line sets the variable expired_pem to the result of the expired_key.export_key function call. The format is set to 'PEM'.

modulus = private_key.n #this line sets the variable modulus to the private_key.n attribute. This is the modulus of the key to be used in the JWT later.
exponent = private_key.e #this line sets the variable exponent to the private_key.e attribute. This is the exponent of the key to be used in the JWT later.

def convert_int_to_base64(int_value): #this line defines a function called convert_int_to_base64 that takes an integer as an argument.
    hex_value = format(int_value, 'x') #this line sets the variable hex_value to the result of the format function call. The format function call takes two arguments, int_value and 'x'.
    if len(hex_value) % 2 == 1: #this line checks if the length of hex_value is odd.
        hex_value = '0' + hex_value #if the length of hex_value is odd, then hex_value is set to '0' + hex_value.
    byte_value = bytes.fromhex(hex_value) #this line sets the variable byte_value to the result of the bytes.fromhex function call. The bytes.fromhex function call takes one argument, hex_value.
    enc = base64.urlsafe_b64encode(byte_value).rstrip(b'=') #this line sets the variable enc to the result of the base64.urlsafe_b64encode function call. The base64.urlsafe_b64encode function call takes one argument, byte_value. The result is then passed to the rstrip function call, which takes one argument, b'='.
    return enc.decode('utf-8') #this line returns the result of the enc.decode function call. The enc.decode function call takes one argument, 'utf-8'.

class Server(BaseHTTPRequestHandler): 
    def do_GET(self): #this line defines a function called do_GET that takes self as an argument. Processes what happens when a GET request is made.
        if self.path == "/.well-known/jwks.json": #this line checks if the path attribute of self is equal to the string "/.well-known/jwks.json".
            self.send_response(200) #this line calls the send_response function on self. The send_response function call takes one argument, 200. Notifies that the request was successful.
            self.send_header("Content-type", "application/json") #this line calls the send_header function on self. The send_header function call takes two arguments, "Content-type" and "application/json". Adds an HTML header to the response and indicates that the response is in json format.
            self.end_headers() #this line calls the end_headers function on self. The end_headers function call takes no arguments. Ends the headers of the response.
            issued_keys = { #this line sets the variable issued_keys to a dictionary.
                "keys": [ #this line sets the "keys" key to a list.
                    {
                        "alg": "RS256", #this line sets the "alg" key to the string "RS256". RS256 is a type of encryption algorithm.
                        "kty": "RSA", #this line sets the "kty" key to the string "RSA". RSA is a key type.
                        "use": "sig", #this line sets the "use" key to the string "sig". sig is a type of way that a key is used.
                        "kid": "keyidentifier1", #this line sets the "kid" key to the string "keyidentifier1". The kid is the key identifier.
                        "n": base64.urlsafe_b64encode(modulus.to_bytes((modulus.bit_length() + 7) // 8, byteorder='big')).decode(), #this line sets the "n" key to the result of the base64.urlsafe_b64encode function call. The base64.urlsafe_b64encode function call takes one argument, modulus.to_bytes((modulus.bit_length() + 7) // 8, byteorder='big'). The result is then passed to the decode function call, which takes one argument, 'utf-8'. The modulus is the modulus of the key to be used in the JWT later.
                        "e": base64.urlsafe_b64encode(exponent.to_bytes((exponent.bit_length() + 7) // 8, byteorder='big')).decode(), #this line sets the "e" key to the result of the base64.urlsafe_b64encode function call. The base64.urlsafe_b64encode function call takes one argument, exponent.to_bytes((exponent.bit_length() + 7) // 8, byteorder='big'). The result is then passed to the decode function call, which takes one argument, 'utf-8'. The exponent is the exponent of the key to be used in the JWT later.
                    }
                ]
            }
            self.wfile.write(bytes(json.dumps(issued_keys), "utf-8")) #this line calls the write function on self.wfile. The write function call takes one argument, bytes(json.dumps(issued_keys), "utf-8"). The json.dumps function call takes one argument, issued_keys. The result is then passed to the bytes function call, which takes two arguments, and "utf-8". Writes the response to the client.
            return #this line returns None. The function as a whole is dedicated to returning the public key to the client.

        self.send_response(405) #this line calls the send_response function on self. The send_response function call takes one argument, 405. Notifies that the request was not successful.
        self.end_headers() #this line calls the end_headers function on self. The end_headers function call takes no arguments. Ends the headers of the response.
        return #this line returns None. The function as a whole is dedicated to denying the user the ability to make certain kinds of requests on the server
    
    def do_POST(self): #this line defines a function called do_POST that takes self as an argument. Processes what happens when a POST request is made.
        path = urlparse(self.path)  #this line sets the variable path to the result of the urlparse function call. The urlparse function call takes one argument, self.path. The result is a parsed version of the path attribute of self.
        parameters = parse_qs(path.query) #this line sets the variable parameters to the result of the parse_qs function call. The parse_qs function call takes one argument, path.query. The result is a dictionary of the query parameters. I attempted to parse the lines manually, but was not able to get it to work.
        if path.path == "/auth": #this line checks if the path attribute of path is equal to the string "/auth".
            header = { #this line sets the variable header to a dictionary.
                "kid": "keyidentifier1" #this line sets the "kid" key to the string "keyidentifier1". The kid is the key identifier.
            }
            payload = { #this line sets the variable payload to a dictionary.
                "user": "username", #this line sets the "user" key to the string "username". The user is the username.
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1) #this line sets the "exp" key to the result of the datetime.datetime.utcnow function call. The result is then passed to the datetime.timedelta function call, which takes one argument, hours=1. The result is the expiration time of the token.
            } 
            if 'expired' in parameters: #this line checks if the string "expired" is in the parameters dictionary.
                header["kid"] = "expiredKID" #this line sets the "kid" key of the header dictionary to the string "expiredKID". The kid is the key identifier.
                payload["exp"] = datetime.datetime.utcnow() - datetime.timedelta(hours=1) #this line sets the "exp" key of the payload dictionary to the result of the datetime.datetime.utcnow function call. The result is then passed to the datetime.timedelta function call, which takes one argument, hours=1. The result is the expiration time of the token.
            ej = jwt.encode(payload, pem, algorithm="RS256", headers=header) #this line sets the variable ej to the result of the jwt.encode function call. The jwt.encode function call takes three arguments, payload, pem, and headers=header. The result is the encoded JWT.
            self.send_response(200) #this line calls the send_response function on self. The send_response function call takes one argument, 200. Notifies that the request was successful.
            self.end_headers() #this line calls the end_headers function on self. The end_headers function call takes no arguments. Ends the headers of the response.
            self.wfile.write(bytes(ej, "utf-8")) #this line calls the write function on self.wfile. The write function call takes one argument, bytes(ej, "utf-8"). Writes the response to the client.
            return #this line returns None. The function as a whole is dedicated to returning the JWT to the client.

        self.send_response(405) #this line calls the send_response function on self. The send_response function call takes one argument, 405. Notifies that the request was not successful.
        self.end_headers() #this line calls the end_headers function on self. The end_headers function call takes no arguments. Ends the headers of the response.
        return #this line returns None. The function as a whole is dedicated to denying the user the ability to make certain kinds of requests on the server

    def do_PUT(self): #this line defines a function called do_PUT that takes self as an argument. Processes what happens when a PUT request is made.
        self.send_response(405) #this line calls the send_response function on self. The send_response function call takes one argument, 405.
        self.end_headers() #this line calls the end_headers function on self. The end_headers function call takes no arguments.
        return #this line returns None. The function as a whole as well as PATH, DELETE, and HEAD functs are dedicated to denying the user the ability to make certain kinds of requests on the server

    def do_PATCH(self): #this line defines a function called do_PATCH that takes self as an argument. Processes what happens when a PATCH request is made.
        self.send_response(405) #this line calls the send_response function on self. The send_response function call takes one argument, 405.
        self.end_headers() #this line calls the end_headers function on self. The end_headers function call takes no arguments.
        return #this line returns None. The function as a whole as well as PUT, DELETE, and HEAD functs are dedicated to denying the user the ability to make certain kinds of requests on the server

    def do_DELETE(self): #this line defines a function called do_DELETE that takes self as an argument. Processes what happens when a DELETE request is made.
        self.send_response(405) #this line calls the send_response function on self. The send_response function call takes one argument, 405.
        self.end_headers() #this line calls the end_headers function on self. The end_headers function call takes no arguments.
        return #this line returns None. The function as a whole as well as PUT, PATCH, and HEAD functs are dedicated to denying the user the ability to make certain kinds of requests on the server

    def do_HEAD(self): #this line defines a function called do_HEAD that takes self as an argument. Processes what happens when a HEAD request is made.
        self.send_response(405) #this line calls the send_response function on self. The send_response function call takes one argument, 405.
        self.end_headers() #this line calls the end_headers function on self. The end_headers function call takes no arguments.
        return #this line returns None. The function as a whole as well as PUT, PATCH, and DELETE functs are dedicated to denying the user the ability to make certain kinds of requests on the server

    #all of the functions for the class thus far just deny the user the ability to make certain kinds of requests on the server.

if __name__ == "__main__": #this line checks if the __name__ variable is equal to the string "__main__".
    server = HTTPServer((host_name, port_num), Server) #this line sets the variable w to the result of the HTTPServer function call. The HTTPServer function call takes two arguments, host_name and port_num, and a class. uses http.server to create a server instance.
    try: #this line starts a try block.
        server.serve_forever()  #this line calls the serve_forever function on w. The serve_forever function call takes no arguments. Function is from the HTTPServer class.
    except KeyboardInterrupt: #this line starts an except block. The except block is executed if the KeyboardInterrupt exception is raised.
        pass #this line does nothing. It is a placeholder for the except block.

    server.server_close() #this line calls the server_close function on w. The server_close function call takes no arguments. Function is from the HTTPServer class.