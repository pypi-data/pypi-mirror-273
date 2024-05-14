from yeeducli.utility.json_utils import response_validator
from yeeducli.constants import CONFIG_FILE_PATH
from yeeducli.utility.logger_utils import Logger
from yeeducli.utility.configure_utils import ConfigFile
from yeeducli.utility.request_utils import Requests
from yeeducli import config
import requests
import sys
import webbrowser

logger = Logger.get_logger(__name__, True)


class ConfigureUser:

    def generate_token(username, password, noBrowser, timeout=None):
        try:
            if timeout is None:
                logger.error("Provided timeout is empty")
                sys.exit(-1)

            url = f"{config.YEEDU_RESTAPI_URL}/login"

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers,
                json={
                    "username": username,
                    "password": password,
                    "timeout": timeout
                }
            ).send_http_request()

            if (response.status_code == 200 and (isinstance(response.json(), dict) and response.json().get('loginURL') is not None)):

                loginURL = response.json().get("loginURL")

                if (noBrowser == 'true'):
                    logger.info(
                        "Please use the below URL to complete the login:")
                    logger.info(f"\n\t{loginURL}\n")
                else:
                    # Open the URL in the default system browser
                    browserCheck = webbrowser.open(loginURL)

                    if (browserCheck):
                        # Prompt the URL on the console for the user to copy
                        logger.info(
                            "Your browser has been opened and can visit:")
                        logger.info(f"\n\t{loginURL}\n")
                    else:
                        # Prompt the Login URL on the console for the user to copy
                        logger.info(
                            "Can not open the browser to visit:")
                        logger.info(f"\n\t{loginURL}\n")

                authToken = input("Enter yeedu session token: ")

                if len(authToken.strip()) != 0:
                    ConfigFile.writeToConfig({"token": authToken})

                    return_json = {
                        "message": f"The token has been stored at location: {CONFIG_FILE_PATH}"
                    }
                    return return_json, 200
                else:
                    logger.error(
                        "\Provided yeedu session token is invalid, please configure again")
                    sys.exit(-1)

            if (response.status_code == 200 and (isinstance(response.json(), dict) and response.json().get('token') is not None)):
                ConfigFile.writeToConfig(response.json())
                return_json = {
                    "message": f"The token has been configured for the username: {username} and stored at location: {CONFIG_FILE_PATH}"
                }
                return return_json, response.status_code

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def logout():
        url = f"{config.YEEDU_RESTAPI_URL}/logout"
        try:
            response = Requests(
                url=url,
                method="POST",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
