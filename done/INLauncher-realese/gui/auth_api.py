import requests

class AuthApiIntegration:
    def __init__(self):
        ...
    def elyby_auth(self, login: str, password: str, totp_token: str | None = None):
        self.url_elyby = "https://authserver.ely.by"
        

        user_data = requests.post(
            url=self.url_elyby + "/auth/authenticate",
            json={
                "username": login.strip(),
                "password": password.strip() if totp_token is None or totp_token == "" else password + ":" + totp_token
            }
        ).json()

        # errors = "two_factor" or "error_data"
        if "error" in user_data:
            print(user_data)
            if user_data["errorMessage"] == "Account protected with two factor auth.":
                return "two_factor"
            else :
                return "error_data"
        else :
            print(user_data)
            return user_data
