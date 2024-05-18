from selenium.webdriver.chrome.webdriver import WebDriver 
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep


class SeleniumHelper():
    def wait_element(self, driver: WebDriver, locator: tuple[By, str], tag_filter: list[tuple[str, str]] = None, timeout: int = 30, delay_before: float = 0.3, delay_after: float = 0.3, return_element:bool = False, max_result:bool = False) -> bool | WebElement:
        """
        Aguarda a presença de um elemento na página, opcionalmente retornando o próprio elemento.

        Args:
            * driver (WebDriver): Instância do WebDriver usada para interagir com o navegador.
            * locator (tuple[By, str]): Localizador do elemento na forma (By, value), onde By é a estratégia de localização e value é o seletor.
            * tag_filter (list[tuple[str, str]], opcional): Filtro de tags para refinar a busca do elemento. Cada filtro é uma tupla (tag_name, attribute). Default é None.
            * timeout (int, opcional): Tempo máximo de espera pelo elemento em segundos. Default é 30 segundos.
            * delay_before (float, opcional): Tempo em segundos para esperar antes de iniciar a busca pelo elemento. Default é 0.3 segundos.
            * delay_after (float, opcional): Tempo em segundos para esperar após a busca pelo elemento. Default é 0.3 segundos.
            * return_element (bool, opcional): Se True, retorna o próprio elemento encontrado. Se False, retorna um booleano indicando se o elemento foi encontrado. Default é False.
            * max_result (bool, opcional): Se True, aplica o filtro tag_filter ao resultado para retornar o elemento mais relevante. Default é False.

        Returns:
            * bool | WebElement: Retorna o elemento WebElement se return_element for True e o elemento for encontrado. Caso contrário, retorna um booleano indicando se o elemento foi encontrado (True) ou não (False).
        """
        sleep(delay_before)
        checked: bool = False
        element: WebElement
        try:
            element = _find_element(driver, locator, tag_filter, timeout, max_result)
            if(element):
                checked = True
            else:
                checked = False
        except:
            checked = False
        sleep(delay_after)
        if(return_element):
            return element
        else:
            return checked

    def wait_and_send_keys(self, driver: WebDriver, locator: tuple[By, str], text: str, tag_filter: list[tuple[str, str]] = None, timeout: int = 30, delay_before: float = 0.3, delay_after: float = 0.3, clear_form: bool = True, click_before: bool = False, max_result:bool = False) -> None:
        """
        Aguarda a presença de um elemento na página e envia um texto para ele, com opções para limpar o campo e clicar no elemento antes de enviar o texto.

        Args:
            * driver (WebDriver): Instância do WebDriver usada para interagir com o navegador.
            * locator (tuple[By, str]): Localizador do elemento na forma (By, value), onde By é a estratégia de localização e value é o seletor.
            * text (str): Texto a ser enviado para o elemento.
            * tag_filter (list[tuple[str, str]], opcional): Filtro de tags para refinar a busca do elemento. Cada filtro é uma tupla (tag_name, attribute). Default é None.
            * timeout (int, opcional): Tempo máximo de espera pelo elemento em segundos. Default é 30 segundos.
            * delay_before (float, opcional): Tempo em segundos para esperar antes de iniciar a busca pelo elemento. Default é 0.3 segundos.
            * delay_after (float, opcional): Tempo em segundos para esperar após enviar o texto para o elemento. Default é 0.3 segundos.
            * clear_form (bool, opcional): Se True, limpa o campo de texto antes de enviar o novo texto. Default é True.
            * click_before (bool, opcional): Se True, clica no elemento antes de enviar o texto. Default é False.
            * max_result (bool, opcional): Se True, aplica o filtro tag_filter ao resultado para retornar o elemento mais relevante. Default é False.
        """
        sleep(delay_before)
        element: WebElement
        element = _find_element(driver, locator, tag_filter, timeout, max_result)
        if(click_before):
            self.wait_and_click(driver, locator, tag_filter)
        if(clear_form):
            element.clear()
        element.send_keys(text)
        sleep(delay_after)

    def wait_and_click(self, driver: WebDriver, locator: tuple[By, str], tag_filter: list[tuple[str, str]] = None, timeout: int = 30, delay_before: float = 0.3, delay_after: float = 0.3, max_result: bool = False) -> None:
        """
        Aguarda a presença de um elemento na página e clica nele.

        Args:
            * driver (WebDriver): Instância do WebDriver usada para interagir com o navegador.
            * locator (tuple[By, str]): Localizador do elemento na forma (By, value), onde By é a estratégia de localização e value é o seletor.
            * tag_filter (list[tuple[str, str]], opcional): Filtro de tags para refinar a busca do elemento. Cada filtro é uma tupla (tag_name, attribute). Default é None.
            * timeout (int, opcional): Tempo máximo de espera pelo elemento em segundos. Default é 30 segundos.
            * delay_before (float, opcional): Tempo em segundos para esperar antes de iniciar a busca pelo elemento. Default é 0.3 segundos.
            * delay_after (float, opcional): Tempo em segundos para esperar após clicar no elemento. Default é 0.3 segundos.
            * max_result (bool, opcional): Se True, aplica o filtro tag_filter ao resultado para retornar o elemento mais relevante. Default é False.
        """
        sleep(delay_before)
        element: WebElement
        element = _find_element(driver, locator, tag_filter, timeout, max_result)
        element.click()
        sleep(delay_after)

    def wait_and_select(self, driver: WebDriver, locator: tuple[By, str], text: str, tag_filter: list[tuple[str, str]] = None, timeout: int = 30, delay_before: float = 0.3, delay_after: float = 0.3, max_result: bool = False) -> None:
        """
        Aguarda a presença de um elemento na página e seleciona uma opção por texto visível em um elemento <select>.

        Args:
            * driver (WebDriver): Instância do WebDriver usada para interagir com o navegador.
            * locator (tuple[By, str]): Localizador do elemento na forma (By, value), onde By é a estratégia de localização e value é o seletor.
            * text (str): Texto visível da opção a ser selecionada no elemento <select>.
            * tag_filter (list[tuple[str, str]], opcional): Filtro de tags para refinar a busca do elemento. Cada filtro é uma tupla (tag_name, attribute). Default é None.
            * timeout (int, opcional): Tempo máximo de espera pelo elemento em segundos. Default é 30 segundos.
            * delay_before (float, opcional): Tempo em segundos para esperar antes de iniciar a busca pelo elemento. Default é 0.3 segundos.
            * delay_after (float, opcional): Tempo em segundos para esperar após selecionar a opção. Default é 0.3 segundos.
            * max_result (bool, opcional): Se True, aplica o filtro tag_filter ao resultado para retornar o elemento mais relevante. Default é False.
        """
        sleep(delay_before)
        element: WebElement
        element = _find_element(driver, locator, tag_filter, timeout, max_result)
        select_object = Select(element)
        select_object.select_by_visible_text(text)
        sleep(delay_after)

    def wait_and_click_in_text(self, driver: WebDriver, locator: tuple[By, str], text: str, delay_before: float = 0.3, delay_after: float = 0.3) -> None:
        """
        Aguarda um breve período e clica em um elemento cujo texto corresponde ao texto fornecido.

        Args:
            * driver (WebDriver): Instância do WebDriver usada para interagir com o navegador.
            * locator (tuple[By, str]): Localizador dos elementos na forma (By, value), onde By é a estratégia de localização e value é o seletor.
            * text (str): Texto a ser correspondido com o texto dos elementos encontrados.
            * delay_before (float, opcional): Tempo em segundos para esperar antes de iniciar a busca pelos elementos. Default é 0.3 segundos.
            * delay_after (float, opcional): Tempo em segundos para esperar após clicar no elemento. Default é 0.3 segundos.
        """
        sleep(delay_before)
        elements: list[WebElement] = driver.find_elements(locator[0], locator[1])
        for element in elements:
            if(text.lower() == element.text.lower()):
                element.click()
                break
        sleep(delay_after)

    def wait_and_hover(self, driver: WebDriver, locator: tuple[By, str], tag_filter: list[tuple[str, str]] = None, timeout: int = 30, delay_before: float = 0.3, delay_after: float = 0.3, max_result: bool = False) -> None:
        """
        Aguarda a presença de um elemento na página e passa o cursor do mouse sobre ele.

        Args:
            * driver (WebDriver): Instância do WebDriver usada para interagir com o navegador.
            * locator (tuple[By, str]): Localizador do elemento na forma (By, value), onde By é a estratégia de localização e value é o seletor.
            * tag_filter (list[tuple[str, str]], opcional): Filtro de tags para refinar a busca do elemento. Cada filtro é uma tupla (tag_name, attribute). Default é None.
            * timeout (int, opcional): Tempo máximo de espera pelo elemento em segundos. Default é 30 segundos.
            * delay_before (float, opcional): Tempo em segundos para esperar antes de iniciar a busca pelo elemento. Default é 0.3 segundos.
            * delay_after (float, opcional): Tempo em segundos para esperar após passar o cursor sobre o elemento. Default é 0.3 segundos.
            * max_result (bool, opcional): Se True, aplica o filtro tag_filter ao resultado para retornar o elemento mais relevante. Default é False.
        """
        sleep(delay_before)
        element: WebElement
        element = _find_element(driver, locator, tag_filter, timeout, max_result)
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        sleep(delay_after)

def _find_element(driver: WebDriver, locator: tuple[By, str], tag_filter: list[tuple[str, str]], timeout: int, max_result: bool) -> WebElement:
        """
        Encontra um elemento na página e espera até que o elemento seja clicável.

        Args:
            * driver (WebDriver): Instância do WebDriver usada para interagir com o navegador.
            * locator (tuple[By, str]): Localizador do elemento na forma (By, value), onde By é a estratégia de localização e value é o seletor.
            * tag_filter (list[tuple[str, str]]): Lista de filtros de tags na forma [(atributo, valor)] para refinar a busca do elemento. Usado apenas quando a estratégia de localização é By.TAG_NAME.
            * timeout (int): Tempo máximo de espera pelo elemento em segundos.
            * max_result (bool): Se True, continua buscando até encontrar o elemento mais relevante baseado no filtro. Se False, retorna o primeiro elemento correspondente.

        Returns:
            * WebElement: O elemento WebElement encontrado que atende aos critérios, ou None se nenhum elemento for encontrado ou se ocorrer uma exceção.
        """
        element: WebElement = None
        try:
            if(locator[0] == By.TAG_NAME):
                elements = driver.find_elements(locator[0], locator[1])
                for el in elements:
                    for filter in tag_filter:
                        if (el.get_attribute(filter[0]) == filter[1]):
                            element = el    
                        else:
                            element = None
                            break
                    if(element):
                        if(max_result):
                            continue
                        else:
                            break
            else:
                element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
        except:
            element = None
        return element