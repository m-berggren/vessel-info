from requests import Response
from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import requests


def setup_driver() -> Edge:
    """
    Adding options and service to install edgedriver.
    :return: Edge webdriver
    """
    options = Options()
    options.add_argument("--headless")
    service = Service(EdgeChromiumDriverManager().install())
    return Edge(service=service, options=options)


def get_request(url: str) -> Response:
    headers = {
        'User-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    return requests.get(url, headers=headers)



