import os
from config.logging import logger as log
from typing import Final, Dict, Any
from dotenv import load_dotenv
import keyword
from openai import OpenAI, AsyncOpenAI
from ratelimit import limits, sleep_and_retry

load_dotenv(dotenv_path=".env")

MODEL: Final[str] = "nousresearch/nous-capybara-7b:free"
OPENROUTER_API_KEY: Final[str] = os.getenv("OPENROUTER_API_KEY")

# OpenAI Config
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# System Message - TODO: Edit this along the way.
systemMessage = f"""
You are an intelligent chatbot designed to revolutionize the way developers
and tech enthusiasts discover, and interact with hackathons. You are a chatbot 
assistant that provides information about hackathons, and helps users to discover
hackathons near them or online. 

Key Features
- Personalized recommendations by analyzing user preferences,
  skill levels, and interests, to provide a list of hackathons
  that match their criteria.
- Skill-level matching by analyzing the user's skill level and
  categorizing them based on beginner, intermediate, or advanced.
- Location-based recommendations by analyzing the user's location
  and providing a list of hackathons near them.
- Team formation assistance by helping users find team members
  with similar interests and skill levels at a particular hackathon
  or event.
- Event registrations by guiding users through the registration process
  for a particular hackathon or event.
- Post-Event follow-up by providing users with a list of resources,
  collecting feedback, and showcasing their projects to a generated
  simple html page with their project details, with links to their 
  repositories and social media profiles.
  
Your task is to help users discover hackathons, provide information about
hackathons, and assist them along the way. You should aim to lower the barrier
of entry for newcomers and provide a seamless experience for all users.
"""

RATE_LIMIT_PERIOD = 120  # 2 minutes


class RouterRequest:
    def __init__(self, model: str, api_key: str, url: str) -> None:
        self.__model = model
        self.__api_key = api_key
        self.__url = url

    def __isidentifier(self, ident: str) -> bool:
        if not isinstance(ident, str):
            raise TypeError("expect str, but gor {!r}".format(type(ident)))

        if not ident.isidentifier():
            return False

        if keyword.iskeyword(ident):
            return False

    def __construct_message(self, **kwargs):
        var = [{
            "role": key,
            "content": value
        } for key, value in kwargs.items()]

        if var is not None:
            return var

        return None

    @property
    def model(self) -> str:
        return self.__model

    @model.setter
    def model(self, model: str) -> None:
        if self.__isidentifier(model):
            self.__model = model

    @property
    def api_key(self) -> str:
        return self.__api_key

    @api_key.setter
    def api_key(self, api_key: str) -> None:
        if self.__isidentifier(api_key):
            self.__api_key = api_key

    @property
    def url(self) -> str:
        return self.__url

    @url.setter
    def url(self, url: str) -> None:
        if self.__isidentifier(url):
            self.__url = url

    @sleep_and_retry
    @limits(calls=15, period=RATE_LIMIT_PERIOD)
    async def router_request(self, message: str):
        response = await client.chat.completions.create(
            model=self.__model,
            timeout=60,
            messages=[
                {
                    "role": "system",
                    "content": systemMessage
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        if response.choices[0].message.content is None:
            log.info("Improper response received from OpenAI.")
            return None

        else:
            return response.choices[0].message.content

    @sleep_and_retry
    @limits(calls=15, period=RATE_LIMIT_PERIOD)
    async def router_request(self, timeout: int, **kwargs):
        response = client.chat.completions.create(
            model=self.__model,
            timeout=timeout,
            messages=[
                {
                    "role": "system",
                    "content": systemMessage
                },
                self.__construct_message(**kwargs)
            ]
        )

        if response.choices[0].message.content is None:
            log.info("Improper response received from OpenAI.")
            return None

        else:
            return response.choices[0].message.content

    def __eq__(self, other):
        return self.__model == other.__model and self.__api_key == other

    def __str__(self) -> str:
        return f"""
        Model: {self.__model}
        Url: {self.__url}
        Api Key: {"*" * len(self.__api_key)}
        """

    def __repr__(self) -> str:
        return f"""
        Model: {self.__model}
        Url: {self.__url}
        Api Key: {"*" * len(self.__api_key)}
        """
