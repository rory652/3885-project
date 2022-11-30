---
site: https://api.jerbtracker.com/
---
# Endpoints

## Users
***
This section focuses on endpoints related to the user experience, this includes logging in, viewing their information and signing up. There are also some endpoints for system admins that will be able to use to view who has access to their care home.
### {{ site }}users/
=== "GET"
    !!! info "Usage"
        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` |  Cookies | String | Session ID for the admin |
    ???+ success "Successful Request"
        ``` json
        {
            "Response": "Here"
        }
        ```
    ??? failure "Failed Request"
        ``` json
        {
            "Error": "Here"
        }
        ```
=== "POST"
    !!! info "Usage"
        |    Field    | Location |  Type   |        Description         |
        |:-----------:|:--------:|:-------:|:--------------------------:|
        |   `email`   |   Body   | String  |        User's email        |
        |   `name`    |   Body   | String  |        User's name         |
        | `username`  |   Body   | String  |      User's username       |
        | `password`  |   Body   | String  | User's password (unhashed) |
        | `care-home` |   Body   | Integer |        Care home ID        |
    ???+ success "Successful Request"
        ``` json
        {
            "Response": "Here"
        }
        ```
    ??? failure "Failed Request"
        ``` json
        {
            "Error": "Here"
        }
        ```
### {{ site }}users/<user-id>
=== "GET"
    !!! info "Usage"
        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` |  Cookies | String | Session ID for the user  |
    ???+ success "Successful Request"
        ``` json
        {
            "Response": "Here"
        }
        ```
    ??? failure "Failed Request"
        ``` json
        {
            "Error": "Here"
        }
        ```
=== "PUT"
    !!! info "Usage"
        |     Field      | Location |  Type  |       Description       |
        |:--------------:|:--------:|:------:|:-----------------------:|
        |   `username`   |   Body   | String |        Username         |
        |   `password`   |   Body   | String |        Password         |
        | `new-username` |   Body   | String | New Username (optional) |
        | `new-password` |   Body   | String | New Password (optional) |
    ???+ success "Successful Request"
        ``` json
        {
            "Response": "Here"
        }
        ```
    ??? failure "Failed Request"
        ``` json
        {
            "Error": "Here"
        }
        ```
=== "DELETE"
    !!! info "Usage"
        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` |  Cookies | String | Session ID for the user  |
    ???+ success "Successful Request"
        ``` json
        {
            "Response": "Here"
        }
        ```
    ??? failure "Failed Request"
        ``` json
        {
            "Error": "Here"
        }
        ```
### {{ site }}login/
=== "GET"
    !!! info "Usage"
        |   Field    | Location |  Type  | Description |
        |:----------:|:--------:|:------:|:-----------:|
        | `username` |   Body   | String |  Username   |
        | `password` |   Body   | String |  Password   |
    ???+ success "Successful Request"
        ``` json
        {
            "Response": "Here"
        }
        ```
    ??? failure "Failed Request"
        ``` json
        {
            "Error": "Here"
        }
        ```
### {{ site }}logout/
=== "DELETE"
    !!! info "Usage"
        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` |  Cookies | String | Session ID for the user  |
    ???+ success "Successful Request"
        ``` json
        {
            "Response": "Here"
        }
        ```
    ??? failure "Failed Request"
        ``` json
        {
            "Error": "Here"
        }
        ```
## Residents
***
The endpoints in this section will allow users to view the residents within their care home. It will allow them to add/remove residents as well as update their information. This is where a user can register a new covid case for a resident or say that a resident has recovered.
### {{ site }}residents/
=== "GET"
    !!! info "Usage"
        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` |  Cookies | String | Session ID for the user |
    ???+ success "Successful Request"
        ``` json
        {
            "Response": "Here"
        }
        ```
    ??? failure "Failed Request"
        ``` json
        {
            "Error": "Here"
        }
        ```
=== "POST"
    !!! info "Usage"
        |   Field    | Location |  Type   |       Description        |
        |:----------:|:--------:|:-------:|:------------------------:|
        |   `auth`   | Cookies  | String  | Session ID for the user  |
        |   `name`   |   Body   | String  |     Resident's name      |
        | `wearable` |   Body   | Integer | Resident's wearable's ID |
    ???+ success "Successful Request"
        ``` json
        {
            "Response": "Here"
        }
        ```
    ??? failure "Failed Request"
        ``` json
        {
            "Error": "Here"
        }
        ```
### {{ site }}residents/<resident-id>
=== "GET"
    !!! info "Usage"
        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` |  Cookies | String | Session ID for the user  |
    ???+ success "Successful Request"
        ``` json
        {
            "Response": "Here"
        }
        ```
    ??? failure "Failed Request"
        ``` json
        {
            "Error": "Here"
        }
        ```
=== "PUT"
    !!! info "Usage"
        |     Field      | Location |  Type   |        Description         |
        |:--------------:|:--------:|:-------:|:--------------------------:|
        |     `auth`     | Cookies  | String  |  Session ID for the user   |
        |   `new-name`   |   Body   | String  |    New Name (optional)     |
        |  `new-status`  |   Body   | String  |   New Status (optional)    |
        | `new-wearable` |   Body   | Integer | New Wearable ID (optional) |
    ???+ success "Successful Request"
        ``` json
        {
            "Response": "Here"
        }
        ```
    ??? failure "Failed Request"
        ``` json
        {
            "Error": "Here"
        }
        ```
=== "DELETE"
    !!! info "Usage"
        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` |  Cookies | String | Session ID for the user  |
    ???+ success "Successful Request"
        ``` json
        {
            "Response": "Here"
        }
        ```
    ??? failure "Failed Request"
        ``` json
        {
            "Error": "Here"
        }
        ```
## Contacts
***
This is where users can find information related to contacts between residents. It will allow them to acknowledge a contact, which means that the necessary resident has been spoken to and tested and the systems knows not to give the notification to other staff.
### {{ site }}contacts/
=== "GET"
    !!! info "Usage"
        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` |  Cookies | String | Session ID for the user  |
    ???+ success "Successful Request"
        ``` json
        {
            "Response": "Here"
        }
        ```
    ??? failure "Failed Request"
        ``` json
        {
            "Error": "Here"
        }
        ```
### {{ site }}contacts/<contact-id>
=== "DELETE"
    !!! info "Usage"
        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` |  Cookies | String | Session ID for the user  |
    ???+ success "Successful Request"
        ``` json
        {
            "Response": "Here"
        }
        ```
    ??? failure "Failed Request"
        ``` json
        {
            "Error": "Here"
        }
        ```
## Modules
***
This section focuses on endpoints that interact with the detection modules throughout the care home. This includes the modules themselves being able to update their statuses and send in location data and users being able to view the status of modules. This means users can see if any module needs maintainence and perform it accordingly.
### {{ site }}modules/
=== "GET"
    !!! info "Usage"
        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` |  Cookies | String | Session ID for the user  |
    ???+ success "Successful Request"
        ``` json
        {
            "Response": "Here"
        }
        ```
    ??? failure "Failed Request"
        ``` json
        {
            "Error": "Here"
        }
        ```
=== "POST"
    !!! info "Usage"
        | Field  | Location |  Type  |      Description      |
        |:------:|:--------:|:------:|:---------------------:|
        |  `id`  |   Body   | String |       Module ID       |
        | `room` |   Body   | String | Room the module is in |
    ???+ success "Successful Request"
        ``` json
        {
            "Response": "Here"
        }
        ```
    ??? failure "Failed Request"
        ``` json
        {
            "Error": "Here"
        }
        ```
### {{ site }}module/<module-id>
=== "GET"
    !!! info "Usage"
        | Field  | Location |  Type  |       Description        |
        |:------:|:--------:|:------:|:------------------------:|
        | `auth` |  Cookies | String | Session ID for the user  |
    ???+ success "Successful Request"
        ``` json
        {
            "Response": "Here"
        }
        ```
    ??? failure "Failed Request"
        ``` json
        {
            "Error": "Here"
        }
        ```
=== "PUT"
    !!! info "Usage"
        |    Field     | Location |   Type   |        Description        |
        |:------------:|:--------:|:--------:|:-------------------------:|
        |    `auth`    | Cookies  |  String  | Session ID for the module |
        |  `location`  |   Body   | Location |       Location Data       |
        | `new-status` |   Body   |  String  |   New Status (optional)   |
    ???+ success "Successful Request"
        ``` json
        {
            "Response": "Here"
        }
        ```
    ??? failure "Failed Request"
        ``` json
        {
            "Error": "Here"
        }
        ```
=== "DELETE"
    !!! info "Usage"
        | Field  | Location |  Type  |        Description        |
        |:------:|:--------:|:------:|:-------------------------:|
        | `auth` | Cookies  | String | Session ID for the module |
    ???+ success "Successful Request"
        ``` json
        {
            "Response": "Here"
        }
        ```
    ??? failure "Failed Request"
        ``` json
        {
            "Error": "Here"
        }
        ```
