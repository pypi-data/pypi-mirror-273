from typing import Optional, List
from abc import ABC, abstractmethod
import gradio as gr
from selenium.webdriver.common.by import By  # import used by generated selenium code
from selenium.webdriver.common.keys import (
    Keys,
)

from .telemetry import send_telemetry
from .action_engine import ActionEngine
from .driver import AbstractDriver
import base64


class CommandCenter(ABC):
    @abstractmethod
    def init_driver():
        pass

    @abstractmethod
    def process_instructions():
        pass


class GradioDemo(CommandCenter):
    """
    CommandCenter allows you to launch a gradio demo powered by selenium and the ActionEngine

    Args:
        actionEngine (`BaseActionEngine`):
            The action engine, with streaming enabled
        driver (`AbstractDriver`):
            The driver
    """

    title = """
    <div align="center">
    <h1>🌊 Welcome to LaVague</h1>
    <p>Redefining internet surfing by transforming natural language instructions into seamless browser interactions.</p>
    </div>
    """

    def __init__(self, actionEngine: ActionEngine, get_driver: callable):
        self.actionEngine = actionEngine
        self.get_driver = get_driver
        self.driver = None
        self.base_url = ""
        self.success = False
        self.error = ""

    def init_driver(self):
        def init_driver_impl(url):
            self.driver = self.get_driver() if self.driver is None else self.driver
            self.driver.goTo(url)
            self.driver.getScreenshot("screenshot.png")
            # This function is supposed to fetch and return the image from the URL.
            # Placeholder function: replace with actual image fetching logic.
            return "screenshot.png"

        return init_driver_impl

    def process_instructions(self):
        def process_instructions_impl(query, url_input):
            if url_input != self.driver.getUrl():
                self.driver.goTo(url_input)
            state = self.driver.getHtml()
            response = ""
            for text in self.actionEngine.get_action_streaming(query, state):
                # do something with text as they arrive.
                response += text
                yield response

        return process_instructions_impl

    def __telemetry(self):
        def telemetry(query, code, html):
            source_nodes = self.actionEngine.get_nodes(query, html)
            retrieved_context = "\n".join(source_nodes)
            send_telemetry(
                self.actionEngine.llm.metadata.model_name,
                code,
                html,
                query,
                self.driver.getUrl(),
                "Lavague-Launch",
                self.success,
                False,
                self.error,
                retrieved_context
            )

        return telemetry

    def __exec_code(self):
        def exec_code(code, full_code):
            self.error = ""
            code = self.actionEngine.cleaning_function(code)
            html = self.driver.getHtml()
            driver_name, driver = self.driver.getDriver()  # define driver for exec
            exec(f"{driver_name.strip()} = driver")  # define driver in case its name is different
            try:
                exec(code)
                output = "Successful code execution"
                status = """<p style="color: green; font-size: 20px; font-weight: bold;">Success!</p>"""
                self.success = True
                full_code += code
            except Exception as e:
                output = f"Error in code execution: {str(e)}"
                status = """<p style="color: red; font-size: 20px; font-weight: bold;">Failure! Open the Debug tab for more information</p>"""
                self.success = False
                self.error = repr(e)
            return output, code, html, status, full_code

        return exec_code

    def __update_image_display(self):
        def update_image_display():
            self.driver.getScreenshot("screenshot.png")
            url = self.driver.getUrl()
            return "screenshot.png", url

        return update_image_display

    def __show_processing_message(self):
        return lambda: "Processing..."

    def run(self, base_url: str, instructions: List[str], server_port: int = 7860):
        """
        Launch the gradio demo

        Args:
            base_url (`str`): the url placeholder
            instructions (List[`str`]): List of default instructions
            max_tokens
        """
        with gr.Blocks() as demo:
            with gr.Tab("LaVague"):
                with gr.Row():
                    gr.HTML(self.title)
                with gr.Row():
                    url_input = gr.Textbox(
                        value=base_url,
                        label="Enter URL and press 'Enter' to load the page.",
                    )

                with gr.Row():
                    with gr.Column(scale=7):
                        image_display = gr.Image(label="Browser", interactive=False)

                    with gr.Column(scale=3):
                        with gr.Accordion(label="Full code", open=False):
                            full_code = gr.Code(
                                value="", language="python", interactive=False
                            )
                        code_display = gr.Code(
                            label="Generated code",
                            language="python",
                            lines=5,
                            interactive=True,
                        )

                        status_html = gr.HTML()
                with gr.Row():
                    with gr.Column(scale=8):
                        text_area = gr.Textbox(
                            label="Enter instructions and press 'Enter' to generate code."
                        )
                        gr.Examples(examples=instructions, inputs=text_area)
            with gr.Tab("Debug"):
                with gr.Row():
                    with gr.Column():
                        log_display = gr.Textbox(interactive=False, lines=20)
                with gr.Row():
                    with gr.Accordion(label="Full HTML", open=False):
                        full_html = gr.Code(
                            language="html",
                            label="Full HTML",
                            interactive=False,
                            lines=20,
                        )

            # Linking components
            url_input.submit(
                self.init_driver(),
                inputs=[url_input],
                outputs=[image_display],
            )
            text_area.submit(
                self.__show_processing_message(), outputs=[status_html]
            ).then(
                self.init_driver(),
                inputs=[url_input],
                outputs=[image_display],
            ).then(
                self.process_instructions(),
                inputs=[text_area, url_input],
                outputs=[code_display],
            ).then(
                self.__exec_code(),
                inputs=[code_display, full_code],
                outputs=[log_display, code_display, full_html, status_html, full_code],
            ).then(
                self.__update_image_display(),
                inputs=[],
                outputs=[image_display, url_input],
            ).then(
                self.__telemetry(),
                inputs=[text_area, code_display, full_html],
            )
        demo.launch(server_port=server_port, share=True, debug=True)
