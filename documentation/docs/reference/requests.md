# HTTP Requests

This page contains help for the 4 different HTTP requests that will be used to interact with this API. It contains examples written in popular languages and what you should expect from successful and unsuccessful requests.

## GET
***
??? info "Summary"
    A GET request is used to fetch data from a specific data source from a server.
    Performing a GET request will not have any effect on the server, it simply fetches data.
    You send a GET request to a specific endpoint, data can be supplied in the URL or in headers.

???+ example "GET Example"
    === "Python"
        ``` py
        import requests

        url = 'https://<url>/<endpoint>'
        params = {"key1": "value1", "key2": "value2"}

        r = requests.get(url=url, params=params)

        print(r.status_code)
        print(r.text)
        ```

    ??? success "Successful Request"
        A successful request will return the HTTP status code: `200` which means okay. There will be some header fields and then a body containing the requested data.
    ??? failure "Failed Request"
        A failed request will return the HTTP status code: `400` if the request is formatted incorrectly, `401`/`403` if you are unauthenticated or denied access to the data, `404` if the data can't be found or `500` if an error occurs with the server.

        There may also be a body in the response which will give more details as to what went wrong.

## POST
***
??? info "Summary"
    A POST request is used to submit data to a server. 
    The request asks the server to accept the data stored in the body of the request.
    It is used to create a resource on the server, often sent to general endpoints rather than specific URIs.
    Logging into a website typically uses POST, where the login credentials are stored in the body and a user session is created.

???+ example "POST Example"
    === "Python"
        ``` py
        import requests

        url = 'https://<url>/<endpoint>'
        data = {"key1": "value1", "key2": "value2"}

        r = requests.post(url=url, data=data)

        print(r.status_code)
        print(r.text)
        ```

    ??? success "Successful Request"
        A successful request will return the HTTP status code: `201` which means created. There will be some header fields and then a body containing the data added to the server, often formatted differently to what was sent.
    ??? failure "Failed Request"
        A failed request will return the HTTP status code: `400` if the request is formatted incorrectly, `401`/`403` if you are unauthenticated or denied access to the data, `404` if the data can't be found or `500` if an error occurs with the server.

        There may also be a body in the response which will give more details as to what went wrong.

## PUT
***
??? info "Summary"
    A PUT request is used to update a resource on the server. The request URI points to an existing resource which must be completely replaced by the new data in the request. If the URI doesn't exist, the server may or may not create a new resource, for this application, it will return an error and not create the resource.

???+ example "PUT Example"
    === "Python"
        ``` py
        import requests

        url = 'https://<url>/<endpoint>'
        data = {"key1": "value1", "key2": "value2"}

        r = requests.put(url=url, data=data)

        print(r.status_code)
        print(r.text)
        ```

    ??? success "Successful Request"
        A successful request will return the HTTP status code: `200` which means okay. There will be some header fields and then a body containing the updated data. The response may also be `201` if the request caused an entry to be created.
    ??? failure "Failed Request"
        A failed request will return the HTTP status code: `400` if the request is formatted incorrectly, `401`/`403` if you are unauthenticated or denied access to the data, `404` if the data can't be found or `500` if an error occurs with the server.

        There may also be a body in the response which will give more details as to what went wrong.

## DELETE
***
??? info "Summary"
    A DELETE request simply removes a resource on the server. The request URI must exist, otherwise the request will fail (as there is nothing to delete).

???+ example "DELETE Example"
    === "Python"
        ``` py
        import requests

        url = 'https://<url>/<endpoint>'

        r = requests.delete(url=url)

        print(r.status_code)
        print(r.text)
        ```

    ??? success "Successful Request"
        A successful request will return the HTTP status code: `204` which means the data was deleted and there is no content. No body will be returned but there may be headers containing useful information.
    ??? failure "Failed Request"
        A failed request will return the HTTP status code: `400` if the request is formatted incorrectly, `401`/`403` if you are unauthenticated or denied access to the data, `404` if the data can't be found or `500` if an error occurs with the server.

        There may also be a body in the response which will give more details as to what went wrong.