from requests import get, post
from requests.models import Response
from typing import Optional, Dict
from json import dumps

from ..exceptions import BadResponseException
from ..models import CookieRequest, IncapsulaGeeTest, TakionAPI

class TakionAPIReese84(TakionAPI):
    BASE_URL = "{}/incapsula{}?api_key={}"
    DOMAIN = "incapsula.takionapi.tech"
    api_key: str

    @staticmethod
    def is_challenge(response: Response) -> bool:
        """
        # Reese84 cookie needed?
        ## Check if the response has been blocked by Incapsula
        This is a very basic check, should **never** be used in production, since each website
        uses a different method to return an incapsula challenge page.

        ### Parameters
        - `response`: The response object to check

        ### Returns
        - `bool`: True if the response is a Incapsula challenge, False otherwise
        """
        return response.status_code in [403, 401]

    def __init__(
        self,
        api_key: str,
    ) -> None:
        '''
        # Takion API Reese84
        ## Incapsula Reese84 API wrapper for Takion
        This class is a wrapper for the Incapsula API, it can be used to solve reese84 challenge.
        To get your takion API key please check the [Takion API](https://takionapi.tech/) website.

        ### Parameters
        - `api_key`: The API key to use

        ### Example Usage
        ```py
        from requests import Session
        from takion_api import TakionAPIReese84

        session = Session()
        takion_api = TakionAPIReese84(
            api_key="TAKION_API_XXXXXXXXXX"
        )
        
        protected_url = "https://www.ticketmaster.com/event/1C005E959B003CA9"
        headers = {
            "Host": "www.ticketmaster.com",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-ch-ua-mobile": "?0",
            "upgrade-insecure-requests": "1",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "sec-fetch-mode": "navigate",
            "sec-fetch-dest": "document",
            "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            "sec-fetch-site": "same-site",
            "sec-fetch-user": "?1",
            "accept-language": "en-US,en;q=0.9"
        }
        
        def send_request_with_solving() -> None:
            # Create a new session
            session = Session()
            print("Loading page with solved reese84...")

            # Generate payload
            data = takion_api.solve_challenge("www.ticketmaster.com", headers["user-agent"])
            
            # Send challenge
            res = session.post(
                data["url"], 
                data=data["payload"], 
                headers=data["headers"]
            ).json()
            
            # Set cookie
            session.cookies.set("reese84", res['token'])
            print(f"Got cookie: {res['token'][:15]}...{res['token'][-15:]}")

            # Sending request to protected url 
            res = session.get(protected_url, headers=headers)
            print(f"Response {'not ' if not TakionAPIReese84.is_challenge(res) else ''}blocked (Status code {res.status_code})")

        def send_request_without_solving() -> None:
            # Create a new session
            session = Session()
            print("Loading page without solving the challenge...")

            # Sending request to protected url
            res = session.get(protected_url, headers=headers)
            print(f"Response {'not ' if not TakionAPIReese84.is_challenge(res) else ''}blocked (Status code {res.status_code})")

        if __name__ == "__main__":
            send_request_without_solving() # Will return 403 or 401
            print("-----------------------------------")
            send_request_with_solving() # Will return 404, old event
        '''
        self.api_key = api_key
        self.challenge_url = False
        self.challenge_headers = False
        pass

    def load_geetest(
        self,
        website_domain: str,
        user_agent: Optional[str]="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    ) -> Dict[str, IncapsulaGeeTest]:
        '''
        # Load Geetest challenge details
        Load the Geetest captcha challenge details

        ### Parameters
        - `website_domain`: The website domain to use for the payload generation
        - `user_agent`: The User-Agent used to request the challenge page

        ### Returns
        - `Dict[str, IncapsulaGeeTest]`: The Geetest challenge details

        ### Raises
        - `BadResponseException`: If the challenge could not be loaded
        '''
        try:
            res = get(
                f"https://epsf.{website_domain}/vamigood",
                headers={
                    "authority": f"epsf.{website_domain}",
                    "accept": "*/*",
                    "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                    "brand": "tm",
                    "origin": f"https://{website_domain}",
                    "referer": f"https://www.{website_domain}/",
                    "requesting-host": website_domain,
                    "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": "\"macOS\"",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-site",
                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                    "x-lang": "co.uk-co.uk"
                }
            ).text
            return {
                "gt": res.split("gt: '")[1].split("'")[0],
                "challenge": res.split("challenge: '")[1].split("'")[0],
                "gee_test_reese84": res.split('solvedCaptcha({')[1].split('data: "')[1].split('"')[0],
                "request_reese84": res.split('protectionSubmitCaptcha("geetest", payload, timeoutMs,')[1].split('"')[1].split('"')[0]
            }
        except:
            raise BadResponseException("Could not load challenge")
    
    def solve_captcha_challenge(
        self,
        website_domain: str,
        session_reese84: str,
        user_agent: Optional[str]="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    ) -> Dict[str, CookieRequest]:
        challenge = self.load_geetest(website_domain, user_agent)

        try:
            captcha_response = post(
                "https://takionapi.tech/geetest/?api_key={}".format(
                    self.api_key,
                ),
                json={
                    "gt": challenge["gt"],
                    "challenge": challenge["challenge"],
                },
                headers={
                    "User-Agent": user_agent,
                }
            ).json()
        except:
            raise BadResponseException("Could not solve challenge")
        if (error := captcha_response.get("error")):
            raise BadResponseException(error)
        return {
            "url": self.challenge_url,
            "headers": self.challenge_headers,
            "payload": dumps({
                "data": challenge["request_reese84"],
                "payload": {
                    "geetest_challenge": challenge["challenge"],
                    "geetest_seccode": captcha_response['geetest_validate'],
                    "geetest_validate": captcha_response['geetest_seccode'],
                    "data": challenge["gee_test_reese84"]
                },
                "provider":"geetest",
                "token": session_reese84
            })
        }
    
    def solve_challenge(
        self,
        website_domain: str,
        user_agent: Optional[str]="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    ) -> Dict[str, CookieRequest]:
        '''
        # Solve the challenge
        Solve the challenge and return the payload, headers and url for the cookie generation request

        ### Parameters
        - `website_domain`: The website domain to use for the payload generation
        - `user_agent`: The User-Agent used to request the challenge page

        ### Returns
        - `Dict[str, CookieRequest]`: The payload, headers and url for the cookie generation request

        ### Raises
        - `BadResponseException`: If the challenge could not be solved
        '''
        try:
            res = get(
                self.BASE_URL.format(
                    self.DOMAIN,
                    website_domain,
                    self.api_key,
                ),
                headers={
                    "User-Agent": user_agent,
                }
            ).json()
        except:
            raise BadResponseException("Could not solve challenge")
        if (error := res.get("error")):
            raise BadResponseException(error)
        self.challenge_url = res["url"]
        self.challenge_headers = res["headers"]
        return res