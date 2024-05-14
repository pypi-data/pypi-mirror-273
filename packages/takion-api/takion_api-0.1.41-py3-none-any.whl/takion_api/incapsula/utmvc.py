from requests import post, get
from requests.models import Response
from requests.cookies import RequestsCookieJar
from re import search
from typing import Optional, Union

from ..exceptions import BadResponseException
from ..models import TakionAPI

class TakionAPIUtmvc(TakionAPI):
    BASE_URL = "{}/utmvc?api_key={}"
    DOMAIN = "incapsula.takionapi.tech"
    api_key: str

    @staticmethod
    def is_challenge(response: Response) -> Union[bool, str]:
        """
        # Utmvc cookie needed?
        ## Check if the response has the utmvc script in it
        This is a very basic check, it only checks if the html page returned by the server contains the utmvc script.
        This method should be edited based on the website you are trying to access.

        ### Parameters
        - `response`: The response object to check

        ### Returns
        - `Union[bool, str]`: The utmvc script if the response is a Utmvc challenge, False otherwise
        """
        pattern = r'src="(/_Incapsula_Resource\?[^"]+)"'
        match = search(pattern, response.text)
        return f"https://{response.url.split('/')[2]}/{match.group(1)}" if match else False

    def __init__(
        self,
        api_key: str,
    ) -> None:
        '''
        # Takion API Utmvc
        ## Incapsula Utmvc API wrapper for Takion
        This class is a wrapper for the Incapsula API, it can be used to solve utmvc challenge.
        To get your takion API key please check the [Takion API](https://takionapi.tech/) website.

        ### Parameters
        - `api_key`: The API key to use

        ### Example Usage
        ```py
        from requests import Session
        from takion_api import TakionAPIUtmvc

        session = Session()
        takion_api = TakionAPIUtmvc(
            api_key="TAKION_API_XXXXXXXXXX"
        )
        url = "https://tickets.rolandgarros.com/fr/"
        headers = {...}
        response = session.get(url, headers=headers)
        if not takion_api.is_challenge(response):
            print("Page loaded successfully")
        else:
            print("Found challenge, solving...")
            # Solve the challenge
            utmvc = takion_api.solve_challenge(
                response,
                cookies=session.cookies # Optional but recommended
            )
            # Set the utmvc cookie
            session.cookies.set("___utmvc", utmvc)
            print(f"Got cookie: {utmvc[:15]}...{utmvc[-15:]}")
            # Now we send the original request again
            response = session.get(url, headers=headers)
            print(f"Challenge {'' if takion_api.is_challenge(response) else 'not '}found using cookie")
        '''
        self.api_key = api_key
        pass

    def get_challenge_url(
        self,
        user_agent: Optional[str]="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    ) -> str:
        '''
        # Load the challenge script
        
        ### Parameters
        - `user_agent`: The User-Agent used to request the challenge page

        ### Returns
        - `str`: The challenge URL

        ### Raises
        - `BadResponseException`: If the challenge URL could not be parsed from the response
        '''
        try:
            return get(
                self.challenge_url,
                headers={
                    "User-Agent": user_agent,
                },
            ).text
        except:
            raise BadResponseException("Could not parse challenge data from response")
    
    def solve_challenge(
        self,
        response: Response,
        user_agent: Optional[str]="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        cookies: Optional[RequestsCookieJar]=None,
    ) -> str:
        '''
        # Solve the challenge
        Solve the challenge and return the payload, headers and url for the cookie generation request

        ### Parameters
        - `response`: The response of the challenge page (the page returned by get_challenge_url)
        - `user_agent`: The User-Agent used to request the challenge page
        - `cookies`: The cookies to send with the request

        ### Returns
        - `str`: The utmvc cookie

        ### Raises
        - `BadResponseException`: If the challenge could not be solved
        '''
        self.challenge_url = TakionAPIUtmvc.is_challenge(response)
        if not self.challenge_url:
            return False
        
        content = self.get_challenge_url(user_agent)
        try:
            res = post(
                self.BASE_URL.format(
                    self.DOMAIN,
                    self.api_key,
                ),
                json={
                    "content": content,
                    "cookies": [[name, value] for name, value in cookies.items()]
                },
                headers={
                    "User-Agent": user_agent,
                }
            ).json()
        except:
            raise BadResponseException("Could not solve challenge")
        if (error := res.get("error")):
            raise BadResponseException(error)
        return res.get("___utmvc")