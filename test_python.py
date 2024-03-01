import requests

server_url = "http://localhost:8080"

def test_get_jwks():
    response = requests.get(server_url + "/.well-known/jwks.json")
    return response.status_code == 200

def test_post_auth():
    response = requests.post(server_url + "/auth")
    return response.status_code == 200

if __name__ == "__main__":
    passed_tests = 0

    if test_get_jwks():
        passed_tests += 1
        print("GET /.well-known/jwks.json: Passed")
    else:
        print("GET /.well-known/jwks.json: Failed")

    if test_post_auth():
        passed_tests += 1
        print("POST /auth: Passed")
    else:
        print("POST /auth: Failed")

    total_tests = 2
    coverage_percentage = (passed_tests / total_tests) * 100
    print(f"Coverage: {coverage_percentage:.2f}%")
