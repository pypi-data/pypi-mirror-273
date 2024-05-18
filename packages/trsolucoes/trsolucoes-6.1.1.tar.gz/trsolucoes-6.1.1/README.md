# Selenium Helper

Este pacote fornece um conjunto de utilitários para facilitar a interação com o Selenium WebDriver, incluindo funcionalidades para esperar por elementos, enviar texto, clicar em elementos, selecionar opções e mover o cursor sobre elementos.

## Instalação

Você pode instalar o pacote diretamente do PyPI usando `pip`:

```sh
pip install trsolucoes
```

# Uso

Aqui estão alguns exemplos de como usar as funções fornecidas pelo pacote.

# Funções Principais

### Importar pacotes
```python
from selenium_helper import SeleniumHelper
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
sh = SeleniumHelper()
```

### `wait_element`
Aguarda a presença de um elemento na página e retorna o próprio elemento ou um booleano indicando se o elemento foi encontrado.
```python
locator = (By.ID, 'example-id')
element_found = sh.wait_element(driver, locator, return_element=True)
```

### `wait_and_send_keys`
Aguarda a presença de um elemento e envia um texto para ele, com opções para limpar o campo e clicar no elemento antes de enviar o texto.
```python
locator = (By.NAME, 'example-name')
sh.wait_and_send_keys(driver, locator, 'example text', clear_form=True)
```

### `wait_and_click`
Aguarda a presença de um elemento e clica nele.
```python
locator = (By.XPATH, '//button[@class="example-class"]')
sh.wait_and_click(driver, locator)
```

### `wait_and_select`
Aguarda a presença de um elemento select e seleciona uma opção pelo texto visível.
```python
locator = (By.TAG_NAME, 'select')
tag_filter = [('ng-reflect-name', 'labelOption'), ('ngcontent-c2', 'xp789e687')]
sh.wait_and_select(driver, locator, 'Option Text', tag_filter=tag_filter)
```

### `wait_and_click_in_text`
Aguarda um breve período e clica em um elemento cujo texto corresponde ao texto fornecido.
```python
locator = (By.TAG_NAME, 'button')
sh.wait_and_click_in_text(driver, locator, 'Button Text')
```

### `wait_and_hover`
Aguarda a presença de um elemento e passa o cursor do mouse sobre ele.
```python
locator = (By.CLASS_NAME, 'hover-target')
sh.wait_and_hover(driver, locator)
```
