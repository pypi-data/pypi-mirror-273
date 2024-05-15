from http import HTTPStatus

from perun.proxygui.tests.shared_test_data import client

import json

# prevent client from being "unused" during static code analysis, it is injected to
# the tests upon launch
_ = client


def test_auth_no_auth_header_sent(client):
    response = client.get("/proxygui/kerberos/authenticate")

    no_auth_header_msg = "Negotiate"

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert no_auth_header_msg in response.headers.get("WWW-Authenticate")


def test_auth_invalid_format_auth_header(client):
    headers = {"Authorization": "Something wrong here"}
    response = client.get("/proxygui/kerberos/authenticate", headers=headers)

    invalid_format_auth_header_msg = (
        "Kerberos ticket in authorization "
        "header must start with 'Negotiate'. "
        "Incorrect format was provided in "
        "authorization header."
    )  # noqa

    result = json.loads(response.data.decode())
    print(result)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert invalid_format_auth_header_msg in result.get("_text", None)
