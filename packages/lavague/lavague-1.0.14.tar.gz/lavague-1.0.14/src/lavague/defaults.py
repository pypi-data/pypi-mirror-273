from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
import os
from typing import Optional
from dotenv import load_dotenv
import re

try:
    from .driver import SeleniumDriver

    SELENIUM_IMPORT = True
except:
    SELENIUM_IMPORT = False

try:
    from .driver import PlaywrightDriver

    PLAYWRIGHT_IMPORT = True
except:
    PLAYWRIGHT_IMPORT = False


load_dotenv()


class DefaultEmbedder(OpenAIEmbedding):
    def __init__(self, model="text-embedding-3-large"):
        super().__init__(model=model)


DEFAULT_OPENAI_MODEL = "gpt-4-1106-preview"

class DefaultLLM(OpenAI):
    def __init__(self):
        max_new_tokens = 512
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        else:
            super().__init__(model=DEFAULT_OPENAI_MODEL, api_key=api_key, max_tokens=max_new_tokens)


def default_python_code_extractor(markdown_text: str) -> Optional[str]:
    # Pattern to match the first ```python ``` code block
    pattern = r"```python(.*?)```"

    # Using re.DOTALL to make '.' match also newlines
    match = re.search(pattern, markdown_text, re.DOTALL)
    if match:
        # Return the first matched group, which is the code inside the ```python ```
        return match.group(1).strip()
    else:
        # Return None if no match is found
        return None


if SELENIUM_IMPORT:

    def default_get_selenium_driver() -> SeleniumDriver:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.keys import Keys
        import os.path

        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1600,900")

        driver = webdriver.Chrome(options=chrome_options)
        return SeleniumDriver(driver)
    
    def evaluation_get_selenium_driver() -> SeleniumDriver:
        """Extra options to make the driver more static for evaluation purposes."""
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.keys import Keys
        import os.path

        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1600,900")
        chrome_options.add_experimental_option("prefs", {
            "profile.managed_default_content_settings.javascript": 2
        })
        chrome_options.add_argument('--proxy-server=127.0.0.1:9999')

        driver = webdriver.Chrome(options=chrome_options)
        return SeleniumDriver(driver)


if PLAYWRIGHT_IMPORT:

    def default_get_playwright_driver() -> PlaywrightDriver:
        try:
            from playwright.sync_api import sync_playwright
        except (ImportError, ModuleNotFoundError) as error:
            raise ImportError(
                "Please install playwright using `pip install playwright` and then `playwright install` to install the necessary browser drivers"
            ) from error
        p = sync_playwright().start()
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_default_timeout(5000)
        return PlaywrightDriver(page)
