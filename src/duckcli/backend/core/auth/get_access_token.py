import time
import requests
import urllib3

urllib3.disable_warnings()


class GetAccessToken:
    token_url = None
    username = None
    password = None
    access_token = None
    access_token_expiration = None

    def __init__(self, token_url, username, password):
        # sourcery skip: raise-specific-error
        # the function that is executed when
        # an instance of the class is created
        self.token_url = token_url
        self.username = username
        self.password = password

        try:
            self.access_token = self.getAccessToken()
            if self.access_token is None:
                raise Exception("Request for access token failed.")
        except Exception as e:
            print(e)
        else:
            self.access_token_expiration = time.time() + 3600

    def getAccessToken(self):
        # the function that is
        # used to request the JWT
        try:
            # build the JWT and store
            # in the variable `token_body`
            # request an access token
            data = {"username": self.username, "password": self.password}
            # sending post request and saving response as response object
            response = requests.post(url=self.token_url, data=data, verify=False)
            # optional: raise exception for status code
            response.raise_for_status()
        except Exception as e:
            print(e)
            return None
        else:
            # assuming the response's structure is
            # {"access_token": ""}
            return response.json()["access_token"]

    class Decorators:
        @staticmethod
        def refreshToken(decorated):
            # the function that is used to check
            # the JWT and refresh if necessary
            def wrapper(auth, *args, **kwargs):
                if time.time() > auth.access_token_expiration:
                    auth.access_token = auth.getAccessToken()
                return decorated(auth, *args, **kwargs)

            return wrapper
