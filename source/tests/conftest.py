import pytest
import requests, re


@pytest.fixture(scope="session", autouse=True)
def sessions(request):
    url = "http://api:5000/users"
    r_resident = requests.post(url, json={"username": "test_resident", "password": "resident", "permissions": 0})
    r_nurse = requests.post(url, json={"username": "test_nurse", "password": "nurse", "permissions": 1})
    r_admin = requests.post(url, json={"username": "test_admin", "password": "admin", "permissions": 2})
    r_module = requests.post(url, json={"username": "test_module", "password": "module", "permissions": -1})

    pytest.residentSession = {"session": re.search("session=(.*?);", r_resident.headers["Set-Cookie"]).group(1)}
    pytest.nurseSession = {"session": re.search("session=(.*?);", r_nurse.headers["Set-Cookie"]).group(1)}
    pytest.adminSession = {"session": re.search("session=(.*?);", r_admin.headers["Set-Cookie"]).group(1)}
    pytest.moduleSession = {"session": re.search("session=(.*?);", r_module.headers["Set-Cookie"]).group(1)}

    pytest.baseurl = "http://api:5000/"

    # Delete later
    pytest.data = 1

    def sessions_fin():
        requests.delete(''.join([url, "/test_resident"]), cookies=pytest.residentSession)
        requests.delete(''.join([url, "/test_nurse"]), cookies=pytest.nurseSession)
        requests.delete(''.join([url, "/test_admin"]), cookies=pytest.adminSession)
        requests.delete(''.join([url, "/test_module"]), cookies=pytest.moduleSession)

    request.addfinalizer(sessions_fin)
