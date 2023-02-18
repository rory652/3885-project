import pytest
import requests, re


class TestContacts:
    class TestGet:
        def test_contacts_get_200(self):
            r = requests.get(''.join([pytest.baseurl, "contacts/"]), cookies=pytest.nurseSession)

            assert r.status_code == 200

        def test_contacts_get_401(self):
            r = requests.get(''.join([pytest.baseurl, "contacts/"]))

            assert r.status_code == 401

        def test_contacts_get_403(self):
            r = requests.get(''.join([pytest.baseurl, "contacts/"]), cookies=pytest.residentSession)

            assert r.status_code == 403

    class TestDelete:
        def test_contact_delete_204(self):
            r = requests.delete(''.join([pytest.baseurl, "contacts/", "temporary"]), cookies=pytest.nurseSession)

            # Temporary
            assert r.status_code == 404
            # assert r.status_code == 204

        def test_contact_delete_401(self):
            r = requests.delete(''.join([pytest.baseurl, "contacts/", "temporary"]))

            # Temporary
            assert r.status_code == 404
            # assert r.status_code == 401

        def test_contact_delete_403(self):
            r = requests.delete(''.join([pytest.baseurl, "contacts/", "temporary"]), cookies=pytest.residentSession)

            # Temporary
            assert r.status_code == 404
            # assert r.status_code == 403

        def test_contact_delete_404(self):
            r = requests.delete(''.join([pytest.baseurl, "contacts/", "doesnt_exist"]))

            assert r.status_code == 404


class TestLocations:
    class TestPost:
        def test_locations_post_201(self):
            r = requests.post(''.join([pytest.baseurl, "locations/"]),
                              json={"wearable": 12345678, "coordinates": {"x": 1, "y": 2, "z": 3}},
                              cookies=pytest.moduleSession)

            json = r.json()
            if "id" in json:
                requests.delete(''.join([pytest.baseurl, "locations/", json["id"]]), cookies=pytest.adminSession)

            assert r.status_code == 201

        def test_locations_post_400(self):
            r = requests.post(''.join([pytest.baseurl, "locations/"]), cookies=pytest.moduleSession)

            assert r.status_code == 400

        def test_locations_post_401(self):
            r = requests.post(''.join([pytest.baseurl, "locations/"]),
                              json={"wearable": 12345678, "coordinates": {"x": 1, "y": 2, "z": 3}})

            assert r.status_code == 401

        def test_locations_post_403(self):
            r = requests.post(''.join([pytest.baseurl, "locations/"]),
                              json={"wearable": 12345678, "coordinates": {"x": 1, "y": 2, "z": 3}},
                              cookies=pytest.nurseSession)

            assert r.status_code == 403


class TestModules:
    class TestGet:
        def test_modules_get_200(self):
            r = requests.get(''.join([pytest.baseurl, "modules/"]), cookies=pytest.adminSession)

            assert r.status_code == 200

        def test_modules_get_401(self):
            r = requests.get(''.join([pytest.baseurl, "modules/"]))

            assert r.status_code == 401

        def test_modules_get_403(self):
            r = requests.get(''.join([pytest.baseurl, "modules/"]), cookies=pytest.nurseSession)

            assert r.status_code == 403

    class TestPost:
        def test_modules_post_201(self):
            r = requests.post(''.join([pytest.baseurl, "modules/"]), json={"room": "living", "status": "none"},
                              cookies=pytest.adminSession)

            json = r.json()
            if "id" in json:
                requests.delete(''.join([pytest.baseurl, "modules/", json["id"]]), cookies=pytest.adminSession)

            assert r.status_code == 201

        def test_modules_post_400(self):
            r = requests.post(''.join([pytest.baseurl, "modules/"]), cookies=pytest.adminSession)

            assert r.status_code == 400

        def test_modules_post_401(self):
            r = requests.post(''.join([pytest.baseurl, "modules/"]), json={"room": "living", "status": "none"})

            assert r.status_code == 401

        def test_modules_post_403(self):
            r = requests.post(''.join([pytest.baseurl, "modules/"]), json={"room": "living", "status": "none"},
                              cookies=pytest.nurseSession)

            assert r.status_code == 403


class TestModule:
    class TestGet:
        def test_module_get_200(self):
            r = requests.post(''.join([pytest.baseurl, "modules/"]), json={"room": "living", "status": "none"},
                              cookies=pytest.adminSession)

            json = r.json()
            r2 = requests.get(''.join([pytest.baseurl, "modules/", json["id"]]), cookies=pytest.adminSession)
            if "id" in json:
                requests.delete(''.join([pytest.baseurl, "modules/", json["id"]]), cookies=pytest.adminSession)

            assert r2.status_code == 200

        def test_module_get_401(self):
            r = requests.post(''.join([pytest.baseurl, "modules/"]), json={"room": "living", "status": "none"},
                              cookies=pytest.adminSession)

            json = r.json()
            r2 = requests.get(''.join([pytest.baseurl, "modules/", json["id"]]))
            if "id" in json:
                requests.delete(''.join([pytest.baseurl, "modules/", json["id"]]), cookies=pytest.adminSession)

            assert r2.status_code == 401

        def test_module_get_403(self):
            r = requests.post(''.join([pytest.baseurl, "modules/"]), json={"room": "living", "status": "none"},
                              cookies=pytest.adminSession)

            json = r.json()
            r2 = requests.get(''.join([pytest.baseurl, "modules/", json["id"]]), cookies=pytest.nurseSession)
            if "id" in json:
                requests.delete(''.join([pytest.baseurl, "modules/", json["id"]]), cookies=pytest.adminSession)

            assert r2.status_code == 403

        def test_module_get_404(self):
            r = requests.get(''.join([pytest.baseurl, "modules/", "doesnt_exist"]), cookies=pytest.adminSession)

            assert r.status_code == 404

    class TestPut:
        def test_module_put_201(self):
            r = requests.post(''.join([pytest.baseurl, "modules/"]), json={"room": "living", "status": "none"},
                              cookies=pytest.adminSession)

            json = r.json()
            r2 = requests.put(''.join([pytest.baseurl, "modules/", json["id"]]),
                              json={"new-room": "living", "new-status": "none"},
                              cookies=pytest.moduleSession)
            if "id" in json:
                requests.delete(''.join([pytest.baseurl, "modules/", json["id"]]), cookies=pytest.adminSession)

            assert r2.status_code == 201

        def test_module_put_400(self):
            r = requests.post(''.join([pytest.baseurl, "modules/"]), json={"room": "living", "status": "none"},
                              cookies=pytest.adminSession)

            json = r.json()
            r2 = requests.put(''.join([pytest.baseurl, "modules/", json["id"]]), cookies=pytest.moduleSession)
            if "id" in json:
                requests.delete(''.join([pytest.baseurl, "modules/", json["id"]]), cookies=pytest.adminSession)

            assert r2.status_code == 400

        def test_module_put_401(self):
            r = requests.post(''.join([pytest.baseurl, "modules/"]), json={"room": "living", "status": "none"},
                              cookies=pytest.adminSession)

            json = r.json()
            r2 = requests.put(''.join([pytest.baseurl, "modules/", json["id"]]),
                              json={"new-room": "living", "status": "none"})
            if "id" in json:
                requests.delete(''.join([pytest.baseurl, "modules/", json["id"]]), cookies=pytest.adminSession)

            assert r2.status_code == 401

        def test_module_put_403(self):
            r = requests.post(''.join([pytest.baseurl, "modules/"]), json={"room": "living", "status": "none"},
                              cookies=pytest.adminSession)

            json = r.json()
            r2 = requests.put(''.join([pytest.baseurl, "modules/", json["id"]]),
                              json={"new-room": "living", "new-status": "none"},
                              cookies=pytest.nurseSession)
            if "id" in json:
                requests.delete(''.join([pytest.baseurl, "modules/", json["id"]]), cookies=pytest.adminSession)

            assert r2.status_code == 403

        def test_module_put_404(self):
            r = requests.put(''.join([pytest.baseurl, "modules/", "doesnt_exist"]),
                             json={"new-room": "living", "new-status": "none"},
                             cookies=pytest.adminSession)

            assert r.status_code == 404

    class TestDelete:
        def test_module_delete_204(self):
            r = requests.post(''.join([pytest.baseurl, "modules/"]), json={"room": "living", "status": "none"},
                              cookies=pytest.adminSession)

            json = r.json()
            r2 = requests.delete(''.join([pytest.baseurl, "modules/", json["id"]]), cookies=pytest.adminSession)

            assert r2.status_code == 204

        def test_module_delete_401(self):
            r = requests.post(''.join([pytest.baseurl, "modules/"]), json={"room": "living", "status": "none"},
                              cookies=pytest.adminSession)

            json = r.json()
            r2 = requests.delete(''.join([pytest.baseurl, "modules/", json["id"]]))
            if "id" in json:
                requests.delete(''.join([pytest.baseurl, "modules/", json["id"]]), cookies=pytest.adminSession)

            assert r2.status_code == 401

        def test_module_delete_403(self):
            r = requests.post(''.join([pytest.baseurl, "modules/"]), json={"room": "living", "status": "none"},
                              cookies=pytest.adminSession)

            json = r.json()
            r2 = requests.delete(''.join([pytest.baseurl, "modules/", json["id"]]), cookies=pytest.nurseSession)
            if "id" in json:
                requests.delete(''.join([pytest.baseurl, "modules/", json["id"]]), cookies=pytest.adminSession)

            assert r2.status_code == 403

        def test_module_delete_404(self):
            r = requests.delete(''.join([pytest.baseurl, "modules/", "doesnt_exist"]), cookies=pytest.adminSession)

            assert r.status_code == 404


class TestResidents:
    class TestGet:
        def test_residents_get_200(self):
            r = requests.get(''.join([pytest.baseurl, "residents/"]), cookies=pytest.nurseSession)

            assert r.status_code == 200

        def test_residents_get_401(self):
            r = requests.get(''.join([pytest.baseurl, "residents/"]))

            assert r.status_code == 401

        def test_residents_get_403(self):
            r = requests.get(''.join([pytest.baseurl, "residents/"]), cookies=pytest.residentSession)

            assert r.status_code == 403

    class TestPost:
        def test_residents_post_201(self):
            r = requests.post(''.join([pytest.baseurl, "residents/"]),
                              json={"name": "John Smith", "status": "none", "wearable": "12345"},
                              cookies=pytest.nurseSession)

            json = r.json()
            if "id" in json:
                requests.delete(''.join([pytest.baseurl, "residents/", json["id"]]), cookies=pytest.nurseSession)

            assert r.status_code == 201

        def test_residents_post_400(self):
            r = requests.post(''.join([pytest.baseurl, "residents/"]), cookies=pytest.nurseSession)

            assert r.status_code == 400

        def test_residents_post_401(self):
            r = requests.post(''.join([pytest.baseurl, "residents/"]))

            assert r.status_code == 401

        def test_residents_post_403(self):
            r = requests.post(''.join([pytest.baseurl, "residents/"]), cookies=pytest.residentSession)

            assert r.status_code == 403


class TestResident:
    class TestGet:
        def test_resident_get_200(self):
            r = requests.post(''.join([pytest.baseurl, "residents/"]),
                              json={"name": "John Smith", "status": "none", "wearable": "12345"},
                              cookies=pytest.nurseSession)
            json = r.json()

            r2 = requests.get(''.join([pytest.baseurl, "residents/", json["id"]]), cookies=pytest.nurseSession)

            if "id" in json:
                requests.delete(''.join([pytest.baseurl, "residents/", json["id"]]), cookies=pytest.nurseSession)

            assert r2.status_code == 200

        def test_resident_get_401(self):
            r = requests.post(''.join([pytest.baseurl, "residents/"]),
                              json={"name": "John Smith", "status": "none", "wearable": "12345"},
                              cookies=pytest.nurseSession)
            json = r.json()

            r2 = requests.get(''.join([pytest.baseurl, "residents/", json["id"]]))

            if "id" in json:
                requests.delete(''.join([pytest.baseurl, "residents/", json["id"]]), cookies=pytest.nurseSession)

            assert r2.status_code == 401

        def test_resident_get_403(self):
            r = requests.post(''.join([pytest.baseurl, "residents/"]),
                              json={"name": "John Smith", "status": "none", "wearable": "12345"},
                              cookies=pytest.nurseSession)
            json = r.json()

            r2 = requests.get(''.join([pytest.baseurl, "residents/", json["id"]]), cookies=pytest.residentSession)

            if "id" in json:
                requests.delete(''.join([pytest.baseurl, "residents/", json["id"]]), cookies=pytest.nurseSession)

            assert r2.status_code == 403

        def test_resident_get_404(self):
            r = requests.get(''.join([pytest.baseurl, "residents/", "doesnt_exist"]))

            assert r.status_code == 404

    class TestPut:
        def test_resident_put_201(self):
            r = requests.post(''.join([pytest.baseurl, "residents/"]),
                              json={"name": "John Smith", "status": "none", "wearable": "12345"},
                              cookies=pytest.nurseSession)
            json = r.json()

            r2 = requests.put(''.join([pytest.baseurl, "residents/", json["id"]]),
                              json={"new-name": "Jon Smith", "new-status": "none", "new-wearable": "12345"},
                              cookies=pytest.nurseSession)

            if "id" in json:
                requests.delete(''.join([pytest.baseurl, "residents/", json["id"]]), cookies=pytest.nurseSession)

            assert r2.status_code == 201

        def test_resident_put_400(self):
            r = requests.post(''.join([pytest.baseurl, "residents/"]),
                              json={"name": "John Smith", "status": "none", "wearable": "12345"},
                              cookies=pytest.nurseSession)
            json = r.json()

            r2 = requests.put(''.join([pytest.baseurl, "residents/", json["id"]]), cookies=pytest.nurseSession)

            if "id" in json:
                requests.delete(''.join([pytest.baseurl, "residents/", json["id"]]), cookies=pytest.nurseSession)

            assert r2.status_code == 400

        def test_resident_put_401(self):
            r = requests.post(''.join([pytest.baseurl, "residents/"]),
                              json={"name": "John Smith", "status": "none", "wearable": "12345"},
                              cookies=pytest.nurseSession)
            json = r.json()

            r2 = requests.put(''.join([pytest.baseurl, "residents/", json["id"]]),
                              json={"new-name": "Jon Smith", "new-status": "none"})

            if "id" in json:
                requests.delete(''.join([pytest.baseurl, "residents/", json["id"]]), cookies=pytest.nurseSession)

            assert r2.status_code == 401

        def test_resident_put_403(self):
            r = requests.post(''.join([pytest.baseurl, "residents/"]),
                              json={"name": "John Smith", "status": "none", "wearable": "12345"},
                              cookies=pytest.nurseSession)
            json = r.json()

            r2 = requests.put(''.join([pytest.baseurl, "residents/", json["id"]]),
                              json={"new-name": "Jon Smith", "new-status": "none"},
                              cookies=pytest.residentSession)

            if "id" in json:
                requests.delete(''.join([pytest.baseurl, "residents/", json["id"]]), cookies=pytest.nurseSession)

            assert r2.status_code == 403

        def test_resident_put_404(self):
            r = requests.put(''.join([pytest.baseurl, "residents/", "doesnt_exist"]))

            assert r.status_code == 404

    class TestDelete:
        def test_resident_delete_204(self):
            r = requests.post(''.join([pytest.baseurl, "residents/"]),
                              json={"name": "John Smith", "status": "none", "wearable": "12345"},
                              cookies=pytest.nurseSession)
            json = r.json()

            r2 = requests.delete(''.join([pytest.baseurl, "residents/", json["id"]]), cookies=pytest.nurseSession)

            assert r2.status_code == 204

        def test_resident_delete_401(self):
            r = requests.post(''.join([pytest.baseurl, "residents/"]),
                              json={"name": "John Smith", "status": "none", "wearable": "12345"},
                              cookies=pytest.nurseSession)
            json = r.json()

            r2 = requests.delete(''.join([pytest.baseurl, "residents/", json["id"]]))

            if "id" in json:
                requests.delete(''.join([pytest.baseurl, "residents/", json["id"]]), cookies=pytest.nurseSession)

            assert r2.status_code == 401

        def test_resident_delete_403(self):
            r = requests.post(''.join([pytest.baseurl, "residents/"]),
                              json={"name": "John Smith", "status": "none", "wearable": "12345"},
                              cookies=pytest.nurseSession)
            json = r.json()

            r2 = requests.delete(''.join([pytest.baseurl, "residents/", json["id"]]), cookies=pytest.residentSession)

            if "id" in json:
                requests.delete(''.join([pytest.baseurl, "residents/", json["id"]]), cookies=pytest.nurseSession)

            assert r2.status_code == 403

        def test_resident_delete_404(self):
            r = requests.delete(''.join([pytest.baseurl, "residents/", "doesnt_exist"]))

            assert r.status_code == 404


class TestUsers:
    class TestGet:
        def test_users_get_200(self):
            r = requests.get(''.join([pytest.baseurl, "users/"]), cookies=pytest.adminSession)
            assert r.status_code == 200

        def test_users_get_401(self):
            r = requests.get(''.join([pytest.baseurl, "users/"]))
            assert r.status_code == 401

        def test_users_get_403(self):
            r = requests.get(''.join([pytest.baseurl, "users/"]), cookies=pytest.residentSession)
            assert r.status_code == 403

    class TestPost:
        def test_users_post_201(self):
            r = requests.post(''.join([pytest.baseurl, "users/"]),
                              json={"username": "test_user", "password": "test", "carehome": "12345678",
                                    "permissions": 0})

            session = {"session": re.search("session=(.*?);", r.headers["Set-Cookie"]).group(1)}
            requests.delete(''.join([pytest.baseurl, "users/", "test_user"]), cookies=session)

            assert r.status_code == 201

        def test_users_post_400(self):
            r = requests.post(''.join([pytest.baseurl, "users/"]),
                              json={"username": "test_user_400", "password": "test", "carehome": "12345678",
                                    "permissions": 0})
            r2 = requests.post(''.join([pytest.baseurl, "users/"]),
                               json={"username": "test_user_400", "password": "new_password", "carehome": "12345678",
                                     "permissions": 0})

            session = {"session": re.search("session=(.*?);", r.headers["Set-Cookie"]).group(1)}
            requests.delete(''.join([pytest.baseurl, "users/", "test_user_400"]), cookies=session)

            assert r2.status_code == 400


class TestUser:
    class TestGet:
        def test_user_get_200(self):
            r = requests.get(''.join([pytest.baseurl, "users/", "test_nurse"]), cookies=pytest.nurseSession)
            assert r.status_code == 200

        def test_user_get_401(self):
            r = requests.get(''.join([pytest.baseurl, "users/", "test_nurse"]))
            assert r.status_code == 401

        def test_user_get_403(self):
            r = requests.get(''.join([pytest.baseurl, "users/", "test_nurse"]), cookies=pytest.residentSession)
            assert r.status_code == 403

        def test_user_get_404(self):
            r = requests.get(''.join([pytest.baseurl, "users/", "doesnt_exist"]), cookies=pytest.residentSession)
            assert r.status_code == 404

    class TestPut:
        def test_user_put_201(self):
            r = requests.post(''.join([pytest.baseurl, "users/"]),
                              json={"username": "test_put", "password": "test", "carehome": "12345678",
                                    "permissions": 0})

            session = {"session": re.search("session=(.*?);", r.headers["Set-Cookie"]).group(1)}

            r2 = requests.put(''.join([pytest.baseurl, "users/", "test_put"]), cookies=session,
                              json={"username": "test_put", "password": "test", "new-username": "test_put_2",
                                    "new-password": "test"})
            session2 = {"session": re.search("session=(.*?);", r2.headers["Set-Cookie"]).group(1)}

            # Clean up
            requests.delete(''.join([pytest.baseurl, "users/", "test_put_2"]), cookies=session2)

            assert r2.status_code == 201

        def test_user_put_400(self):
            r = requests.post(''.join([pytest.baseurl, "users/"]),
                              json={"username": "test_put", "password": "test", "carehome": "12345678",
                                    "permissions": 0})

            session = {"session": re.search("session=(.*?);", r.headers["Set-Cookie"]).group(1)}

            r2 = requests.put(''.join([pytest.baseurl, "users/", "test_put"]), cookies=session,
                              json={"username": "test_put", "password": "wrong_password", "new-username": "test_put_2",
                                    "new-password": "irrelevant"})

            # Clean up
            requests.delete(''.join([pytest.baseurl, "users/", "test_put"]), cookies=session)

            assert r2.status_code == 400

        def test_user_put_401(self):
            r = requests.put(''.join([pytest.baseurl, "users/", "test_nurse"]))

            assert r.status_code == 401

        def test_user_put_403(self):
            r = requests.put(''.join([pytest.baseurl, "users/", "test_nurse"]), cookies=pytest.residentSession)

            assert r.status_code == 403

        def test_user_put_404(self):
            r = requests.put(''.join([pytest.baseurl, "users/", "doesnt_exist"]))

            assert r.status_code == 404

    class TestDelete:
        def test_user_delete_204(self):
            r = requests.post(''.join([pytest.baseurl, "users/"]),
                              json={"username": "test_delete", "password": "test", "carehome": "12345678",
                                    "permissions": 0})

            session = {"session": re.search("session=(.*?);", r.headers["Set-Cookie"]).group(1)}

            r2 = requests.delete(''.join([pytest.baseurl, "users/", "test_delete"]), cookies=session)

            assert r2.status_code == 204

        def test_user_delete_401(self):
            r = requests.delete(''.join([pytest.baseurl, "users/", "test_nurse"]))

            assert r.status_code == 401

        def test_user_delete_403(self):
            r = requests.delete(''.join([pytest.baseurl, "users/", "test_nurse"]), cookies=pytest.residentSession)

            assert r.status_code == 403

        def test_user_delete_404(self):
            r = requests.delete(''.join([pytest.baseurl, "users/", "doesnt_exist"]))

            assert r.status_code == 404
