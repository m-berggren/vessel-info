from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def setup_driver() -> Edge:
    """
    Adding options and service to install edgedriver.
    :return: Edge webdriver
    """
    options = Options()
    options.add_argument("--headless")
    service = Service(EdgeChromiumDriverManager().install())
    return Edge(service=service, options=options)
