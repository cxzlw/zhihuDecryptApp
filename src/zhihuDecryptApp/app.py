"""
The app to decrypt zhihu's encrypted (probably not) passages. 
"""
import logging

import toga
import zhihudecrypt
from zhihudecrypt import consts
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class LogHandler(logging.Handler):
    def __init__(self, info_text, level=logging.NOTSET):
        super().__init__(level)
        self.info_text = info_text

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self.info_text.value += msg + "\n"
        self.info_text.scroll_to_bottom()


class ZhihuDecrypt(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """

        main_box = toga.Box(style=Pack(direction=COLUMN))

        # Text

        self.passage_text = toga.MultilineTextInput(style=Pack(flex=7))

        # Box(Select, Button)
        btn_and_selection_box = toga.Box(style=Pack(direction=ROW))

        self.selection = toga.Selection(style=Pack(flex=2))

        self.selection.items += ["auto", "none"]
        self.selection.items += consts.dicts.keys()

        button = toga.Button(style=Pack(flex=8), text="Decrypt", on_press=self.on_decrypt_clicked)

        btn_and_selection_box.add(self.selection)
        btn_and_selection_box.add(button)

        # Text
        info_text = toga.MultilineTextInput(style=Pack(flex=3, color="YELLOW", background_color="BLACK"), readonly=True)

        logging.basicConfig(format="[%(levelname)s %(asctime)s] %(message)s",
                            handlers=[LogHandler(info_text), logging.StreamHandler()],
                            level=logging.INFO)

        logging.info("欢迎使用Zhihu Decrypt App")
        logging.info("本工具由cxzlw开发，基于zhihuDecrypt")
        logging.info("本项目开源地址 https://github.com/cxzlw/zhihuDecryptApp")
        logging.info("zhihuDecrypt开源地址 https://github.com/cxzlw/zhihuDecrypt")
        logging.info("均采用GPLv3授权")
        logging.info("")
        logging.info("使用方法: ")
        logging.info("")
        logging.info("1. 在上方文本框输入要解密的文章")
        logging.info("2. 如果知道对应的加密情况，在Decrypt左边的下拉框选择")
        logging.info("   不知道的话保留auto选项自动检测")
        logging.info("3. 单击Decrypt")
        logging.info("4. Enjoy :)")

        main_box.add(self.passage_text)
        main_box.add(btn_and_selection_box)
        main_box.add(info_text)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def on_decrypt_clicked(self, _):
        method = self.selection.value
        passage = self.passage_text.value
        logging.info("解密中")
        if method == "auto":
            logging.info("加密情况设为auto, 正在自动检测")
            probability = zhihudecrypt.detect_encrypt_method_probability(passage)
            logging.info("各情况概率: ")
            for k, v in probability.items():
                logging.info(f"{k}: {round(v * 10000) / 100}%")
            method = max(probability, key=lambda x: probability[x])
            logging.info(f"检测结果为: {method}")
        self.passage_text.value = zhihudecrypt.decrypt(passage, method)
        logging.info("解密完成")


def main():
    return ZhihuDecrypt()
