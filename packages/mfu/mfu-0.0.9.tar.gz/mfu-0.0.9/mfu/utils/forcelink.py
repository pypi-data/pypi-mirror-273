import requests


def login(s, username, password, schema, subdomain):
    requests.packages.urllib3.disable_warnings()
    url = (
        "https://" + subdomain + ".forcelink.net/forcelink/j_spring_security_check"
    )
    data = {}
    data["j_username"] = username
    data["j_password"] = password
    data["j_subscriberID"] = schema
    data["j_timezone"] = "Africa/Johannesburg"
    response = s.get(
        "https://"
        + subdomain
        + ".forcelink.net/forcelink/rest/usermanager/isSuperadminUserPass?username="
        + data["j_username"]
        + "&password="
        + data["j_password"]
        + "&subscriberId="
        + data["j_subscriberID"],
        verify=False,
        allow_redirects=False,
    )

    if response.status_code != 200 and response.status_code != 204:
        raise Exception(response.text)

    response = s.get(
        "https://"
        + subdomain
        + ".forcelink.net/forcelink/rest/usermanager/isConcurrentSessionsExceeded?subscriberId="
        + data["j_subscriberID"]
        + "&username="
        + data["j_username"],
        verify=False,
        allow_redirects=False,
    )

    if response.status_code != 200 and response.status_code != 204:
        raise Exception(response.text)

    if response.json():
        print("Kicking out user as your are still logged in...")
        response = s.get(
            "https://"
            + subdomain
            + ".forcelink.net/forcelink/rest/usermanager/kickOutUsername?subscriberId="
            + data["j_subscriberID"]
            + "&username="
            + data["j_username"],
            verify=False,
        )

    if response.status_code != 200 and response.status_code != 204:
        raise Exception(response.text)

    response = s.post(url, data=data, allow_redirects=True)

    if response.status_code != 200 and response.status_code != 204:
        raise Exception(response.text)

    cookies = s.cookies.get_dict()
    response = s.get(
        "https://"
        + subdomain
        + ".forcelink.net/forcelink/;jsessionid="
        + cookies["JSESSIONID"],
        verify=False,
    )

    if response.status_code != 200 and response.status_code != 204:
        raise Exception(response.text)

    response = s.get(
        "https://"
        + subdomain
        + ".forcelink.net/forcelink/rest/usermanager/isSessionAuthenticated",
        verify=False,
        allow_redirects=False,
    )

    if response.status_code != 200 and response.status_code != 204:
        raise Exception(response.text)

    response = s.get(
        "https://"
        + subdomain
        + ".forcelink.net/forcelink/rest/usermanager/getCurrentUserDWR",
        verify=False,
        allow_redirects=False,
    )

    if response.status_code != 200 and response.status_code != 204:
        raise Exception(response.text)
