---
site: api.jerbtracker.com/
---
# Endpoints

## Users
***
This section focuses on endpoints related to the user experience, this includes logging in, viewing their information and signing up. There are also some endpoints for system admins that will be able to use to view who has access to their care home.
### {{ site }}users/
=== "GET"
    !!! info "Usage"
        This is used to get a list of all users registered to a given care home. It will provide their names and their role (resident or nurse).

        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` |  Cookies | String | Session ID for the admin |
        !!! warning "Admin Only"
            Any request made to this endpoint not coming from an Admin's account will be rejected
    ???+ success "Successful Request - Status Code 200"
        ``` json
        {
            "users": [
                {"name": "Steve", "role": "Nurse}
            ]
        }
        ```
    ??? failure "Failed Request - Status Code 403"
        ``` json
        {
            "error": "This endpoint is for admins only"
        }
        ```
=== "POST"
    !!! info "Usage"
        This is used to register a new user to a care home. Successful responses will return a header setting the session ID in cookies and a body confirming the successful registration. The user will be redirected and logged in. (Email Confirmation Later?)

        |    Field    | Location |  Type   |                    Description                     |
        |:-----------:|:--------:|:-------:|:--------------------------------------------------:|
        |   `email`   |   Body   | String  |                    User's email                    |
        |   `name`    |   Body   | String  |                    User's name                     |
        | `username`  |   Body   | String  |                  User's username                   |
        | `password`  |   Body   | String  |             User's password (unhashed)             |
        |   `nurse`   |   Body   | Boolean | True = User is a nurse, False = User is a resident |
        | `care-home` |   Body   | Integer |                    Care home ID                    |
    ???+ success "Successful Request - status Code 201"
        Header: 
        ```http
        Set-Cookie: id=ACJHBSDKAJ21312; Expires=Thu, 01 Dec 2022 19:30:00 GMT; Secure; HttpOnly
        ```
        Body: 
        ```json
        {
            "registration": True
        }
        ```
    ??? failure "Failed Request - Status Code 400"
        ``` json
        {
            "error": "The field `password` was not filled correctly - must contain..."
        }
        ```
### {{ site }}users/<user-id\>
=== "GET"
    !!! info "Usage"
        Returns information for the user: including their email, username, name, role and care home name. Can only be accessed by the user of the account themselves.

        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` |  Cookies | String | Session ID for the user  |
        !!! warning "User Only"
            Any request made to this endpoint not coming from the User's own account will be rejected
    ???+ success "Successful Request - Status Code 200"
        ``` json
        {
            "email": "frank@gmail.com",
            "username": "frank-smith01", 
            "name": "Frank Smith", 
            "role": "Resident",
            "care-home": "Barnaby's Home for the Senile"
        }
        ```
    ??? failure "Failed Request - Status Code 403"
        ``` json
        {
            "error": "Only user can access this resource"
        }
        ```
=== "PUT"
    !!! info "Usage"
        This is used to update a user's information, such as setting a new username or password. Only one of the optional fields needs to be set, but both can be if the user wishes. It returns a new session id for the user in the cookies.

        |     Field      | Location |  Type  |       Description       |
        |:--------------:|:--------:|:------:|:-----------------------:|
        |   `username`   |   Body   | String |        Username         |
        |   `password`   |   Body   | String |        Password         |
        | `new-username` |   Body   | String | New Username (optional) |
        | `new-password` |   Body   | String | New Password (optional) |
    ???+ success "Successful Request - Status Code 200"
        Header: 
        ```http
        Set-Cookie: id=IASHGDK21765213; Expires=Thu, 01 Dec 2022 19:30:00 GMT; Secure; HttpOnly
        ```
        Body:
        ``` json
        {
            "valid": True
        }
        ```
    ??? failure "Failed Request - Status Code 400"
        ``` json
        {
            "error": "User not found" OR "One of the optional fields must be set"
        }
        ```
=== "DELETE"
    !!! info "Usage"
        This is used to delete the user's account. It must come from a valid session and contain the user's details, to help authenticate that the request came from them.

        |   Field    | Location |  Type  |       Description       |
        |:----------:|:--------:|:------:|:-----------------------:|
        |   `auth`   | Cookies  | String | Session ID for the user |
        | `username` |   Body   | String |        Username         |
        | `password` |   Body   | String |        Password         |
    ???+ success "Successful Request - Status Code 204"
        No body is returned
    ??? failure "Failed Request - Status Code 403"
        ``` json
        {
            "error": "Invalid credentials - request must contain user information"
        }
        ```
### {{ site }}login/
=== "POST"
    !!! info "Usage"
        Logs the user in to the system. Returns a session ID for the system in the cookies.

        |   Field    | Location |  Type  | Description |
        |:----------:|:--------:|:------:|:-----------:|
        | `username` |   Body   | String |  Username   |
        | `password` |   Body   | String |  Password   |
    ???+ success "Successful Request - Status Code 201"
        Header: 
        ```http
        Set-Cookie: id=IASHGDK21765213; Expires=Thu, 01 Dec 2022 19:30:00 GMT; Secure; HttpOnly
        ```
        Body:
        ``` json
        {
            "valid": True
        }
        ```
    ??? failure "Failed Request - Status Code 400"
        ``` json
        {
            "error": "Invalid user credentials"
        }
        ```
### {{ site }}logout/
=== "DELETE"
    !!! info "Usage"
        Logs the user out by deleting the session ID on the server and returning a None session ID to their cookies.

        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` |  Cookies | String | Session ID for the user  |
    ???+ success "Successful Request - Status Code 204"
        Header: 
        ```http
        Set-Cookie: id=None; Secure; HttpOnly
        ```
        No body is returned
    ??? failure "Failed Request - 400"
        !!! warning "Security Concern"
            Important not to tell the user that the session ID failed as this would allow them to brute force to find valid session IDs.
        ``` json
        {
            "error": "Logout failed"
        }
        ```
## Residents
***
The endpoints in this section will allow users to view the residents within their care home. It will allow them to add/remove residents as well as update their information. This is where a user can register a new covid case for a resident or say that a resident has recovered.
### {{ site }}residents/
=== "GET"
    !!! info "Usage"
        This returns a list of residents in the user's care home. This list contains their name, wearable ID and covid status

        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` |  Cookies | String | Session ID for the user  |
        !!! warning "Nurse Only"
            This endpoint can only be accessed by the nurses in the care home, any other users requesting this endpoint will fail.
    ???+ success "Successful Request - Status Code 200"
        ``` json
        {
            "residents": [
                {"name": "Joanne", "wearable": 123456, "covid": True},
                {"name": "Elliot", "wearable": 654321, "covid": False}
            ]
        }
        ```
    ??? failure "Failed Request - Status Code 403"
        ``` json
        {
            "error": "Unauthorised User"
        }
        ```
=== "POST"
    !!! info "Usage"
        This is used to add new residents to the system for a specific care home. This can only be performed by nurses working for the care home.

        |   Field    | Location |  Type   |       Description        |
        |:----------:|:--------:|:-------:|:------------------------:|
        |   `auth`   | Cookies  | String  | Session ID for the user  |
        |   `name`   |   Body   | String  |     Resident's name      |
        | `wearable` |   Body   | Integer | Resident's wearable's ID |
        |  `covid`   |   Body   | Boolean | Resident's covid status  |
        !!! warning "Nurse Only"
            This endpoint can only be accessed by the nurses in the care home, any other users requesting this endpoint will fail.
    ???+ success "Successful Request - Status Code 201"
        ``` json
        {
            "response": "Resident successfully registered"
        }
        ```
    ??? failure "Failed Request - Status Code 400"
        ``` json
        {
            "error": "Invalid details entered"
        }
        ```
### {{ site }}residents/<resident-id\>
=== "GET"
    !!! info "Usage"
        This gets the information for a specific resident. Can only be accessed by nurses and the resident themselves.

        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` |  Cookies | String | Session ID for the user  |
        !!! warning "Nurse Only"
            This endpoint can only be accessed by the nurses in the care home, any other users requesting this endpoint will fail.
    ???+ success "Successful Request - Status Code 200"
        ``` json
        {
            "name": "Phil", 
            "wearable": 098213, 
            "covid": True
        }
        ```
    ??? failure "Failed Request - Status Code 404"
        ``` json
        {
            "error": "Resident not found"
        }
        ```
=== "PUT"
    !!! info "Usage"
        Updates a user's information, only one of the optional fields needs to be set. Only nurses can use this. Allows updating of the residents covid status
        !!! warning "Nurse Only"
            This endpoint can only be accessed by the nurses in the care home, any other users requesting this endpoint will fail.
        |     Field      | Location |  Type   |        Description         |
        |:--------------:|:--------:|:-------:|:--------------------------:|
        |     `auth`     | Cookies  | String  |  Session ID for the user   |
        |   `new-name`   |   Body   | String  |    New Name (optional)     |
        |  `new-status`  |   Body   | String  |   New Status (optional)    |
        | `new-wearable` |   Body   | Integer | New Wearable ID (optional) |
    ???+ success "Successful Request - Status Code 200"
        ``` json
        {
            "valid": True
        }
        ```
    ??? failure "Failed Request - Status Code 400"
        ``` json
        {
            "error": "At least one of the optional fields must be provided"
        }
        ```
=== "DELETE"
    !!! info "Usage"
        Removes a resident from the system.

        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` |  Cookies | String | Session ID for the user  |
        !!! warning "Nurse Only"
            This endpoint can only be accessed by the nurses in the care home, any other users requesting this endpoint will fail.
    ???+ success "Successful Request - Status Code 204"
        No body is returned
    ??? failure "Failed Request - 404"
        ``` json
        {
            "error": "Resident not found"
        }
        ```
## Contacts
***
This is where users can find information related to contacts between residents. It will allow them to acknowledge a contact, which means that the necessary resident has been spoken to and tested and the systems knows not to give the notification to other staff.
### {{ site }}contacts/
=== "GET"
    !!! info "Usage"
        Gets all the contacts currently unacknowledged.

        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` |  Cookies | String | Session ID for the user  |
        !!! warning "Nurse Only"
            This endpoint can only be accessed by the nurses in the care home, any other users requesting this endpoint will fail.
    ???+ success "Successful Request - Status Code 200"
        ``` json
        {
            "contacts": [
                {"who": ["infected": 123455, "healthy": 123876], "test": True}
            ]
        }
        ```
    ??? failure "Failed Request - Status Code 403"
        ``` json
        {
            "error": "Invalid User"
        }
        ```
### {{ site }}contacts/<contact-id\>
=== "DELETE"
    !!! info "Usage"
        Used to acknowledge a contact, ie a test has been performed. A seperate request to the "residents/<resident-id\>" endpoint is required to update their covid status
        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` |  Cookies | String | Session ID for the user  |
    ???+ success "Successful Request - Status Code 204"
        No body is returned.
    ??? failure "Failed Request - Status Code 404"
        ``` json
        {
            "error": "Contact not found"
        }
        ```
## Modules
***
This section focuses on endpoints that interact with the detection modules throughout the care home. This includes the modules themselves being able to update their statuses and send in location data and users being able to view the status of modules. This means users can see if any module needs maintainence and perform it accordingly.
### {{ site }}modules/
=== "GET"
    !!! info "Usage"
        Used by system admins to view all the modules currently registered in their care home. Will return a list including the module ID, the room its in and its status (any issues with it).
        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` |  Cookies | String | Session ID for the admin |
        !!! warning "Admin Only"
            Any request made to this endpoint not coming from an Admin's account will be rejected
    ???+ success "Successful Request - Status Code 200"
        ``` json
        {
            "modules": [
                {"id": 8965, "room": "Bedroom 1", "status": "None"},
                {"id": 6520, "room": "Living Room", "status": "Battery change needed"}
            ]
        }
        ```
    ??? failure "Failed Request - Status Code 403"
        ``` json
        {
            "error": "Unauthorised User"
        }
        ```
=== "POST"
    !!! info "Usage"
        Allows a system admin to add new detection modules to the system.

        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` | Cookies  | String | Session ID for the admin |
        |  `id`  |   Body   | String |        Module ID         |
        | `room` |   Body   | String |  Room the module is in   |
        !!! warning "Admin Only"
            Any request made to this endpoint not coming from an Admin's account will be rejected
    ???+ success "Successful Request - 201"
        ``` json
        {
            "response": "Module successfully registered"
            "module": {...}
        }
        ```
    ??? failure "Failed Request - Status Code 403"
        ``` json
        {
            "error": "Unauthorised User"
        }
        ```
### {{ site }}module/<module-id\>
=== "GET"
    !!! info "Usage"
        Allows a nurse to view information about a module such as its location and status.
        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` |  Cookies | String | Session ID for the nurse |
        !!! warning "Nurse Only"
            Any request made to this endpoint not coming from a Nurses's account will be rejected
    ???+ success "Successful Request - Status Code 200"
        ``` json
        {
            "module": 1265,
            "room": "Conservatory",
            "Status": "None"
        }
        ```
    ??? failure "Failed Request - Status Code 403"
        ``` json
        {
            "error": "Unauthorized User"
        }
        ```
=== "PUT"
    !!! info "Usage"
        Lets a module update its status and send in location data to be processed.

        |    Field     | Location |   Type   |        Description        |
        |:------------:|:--------:|:--------:|:-------------------------:|
        |    `auth`    | Cookies  |  String  | Session ID for the module |
        |  `location`  |   Body   | Location |       Location Data       |
        | `new-status` |   Body   |  String  |   New Status (optional)   |
        !!! warning "Module Only"
            Any request made to this endpoint not coming from a module itself will be rejected
    ???+ success "Successful Request - Status Code 200"
        ``` json
        {
            "valid": True
        }
        ```
    ??? failure "Failed Request - Status Code 403"
        ``` json
        {
            "error": "Unauthorized User"
        }
=== "DELETE"
    !!! info "Usage"
        Allows an admin to remove a module from the system.

        | Field  | Location |  Type  |        Description        |
        |:------:|:--------:|:------:|:-------------------------:|
        | `auth` | Cookies  | String | Session ID for the admin  |
        !!! warning "Admin Only"
            Any request made to this endpoint not coming from an Admin's account will be rejected
    ???+ success "Successful Request - Status Code 204"
        No body is returned.
    ??? failure "Failed Request - Status Code 403"
        ``` json
        {
            "error": "Unauthorized User"
        }
        ```
