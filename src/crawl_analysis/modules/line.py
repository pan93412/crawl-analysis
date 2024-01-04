import datetime
import logging
from pathlib import Path
import platform
import re
import subprocess
from tempfile import NamedTemporaryFile
from typing import TypedDict
import pyautogui
import pyperclip
from pymongo.collection import Collection

from models.post import LineMessageModel

class LineParsedResult(TypedDict):
    timestamp: datetime.datetime
    author: str
    message: str


class LineCrawler:
    def __init__(self, collection: Collection[LineMessageModel]):
        self.collection = collection
        self.assets_path = Path(__file__).parent / "line-screenshots"

    def _get_screenshot_image(self, name: str) -> str:
        return (self.assets_path / name).as_posix()

    def open_line(self) -> None:
        # for macOS, we spawn /Application/LINE.app
        # for Windows, we spawn C:\Program Files\LINE\LINE.exe
        #
        # we don't spawn if the app is already running.

        if platform.system() == "Darwin":
            subprocess.Popen(["/Applications/LINE.app/Contents/MacOS/LINE"])
        elif platform.system() == "Windows":
            subprocess.Popen([r"C:\Program Files\LINE\LINE.exe"])
        else:
            raise NotImplementedError("unsupported platform")

    def search_group(self, group_name: str) -> tuple[str, str] | None:
        if platform.system() == "Darwin":
            return self.search_group_mac(group_name)
        # elif platform.system() == "Windows":
            # self.search_group_windows(group_name)
        else:
            raise NotImplementedError("unsupported platform")

    def search_group_mac(self, group_name: str) -> tuple[str, str] | None:  # message, chat name
        pixel_ratio = pyautogui.screenshot().size[0] / pyautogui.size().width
        pr = lambda x: x // pixel_ratio

        pyautogui.sleep(3)  # wait focusing.

        # find the search bar – macos.line.search.png. wait 3s.
        search_bar_image = self._get_screenshot_image("macos.line.search.png")
        search_bar_box = pyautogui.locateOnScreen(search_bar_image, 3, confidence=0.9)
        assert search_bar_box is not None

        # click the search bar
        pyautogui.click(x=pr(search_bar_box.left), y=pr(search_bar_box.top), clicks=3, interval=0.2)
        # type the group name
        pyperclip.copy(group_name)
        pyautogui.hotkey("command", "a")
        pyautogui.hotkey("backspace")
        pyautogui.hotkey("command", "v")
        pyautogui.sleep(2)

        no_result_image = self._get_screenshot_image("maocs.line.search.no-result.png")
        try:
            pyautogui.locateOnScreen(no_result_image, 1)
            raise RuntimeError("no such group")
        except (pyautogui.ImageNotFoundException):
            pyautogui.click(pr(search_bar_box.left) + 120, pr(search_bar_box.top + search_bar_box.height) + 45, clicks=2) # fixme: magic number

        # then, wait for the group to load
        pyautogui.sleep(3)

        # click "scroll to end" button if there's one
        scroll_to_end_image = self._get_screenshot_image("macos.line.scroll-to-end.png")
        try:
            scroll_to_end_box = pyautogui.locateOnScreen(scroll_to_end_image, 3, confidence=0.95)
            assert scroll_to_end_box is not None
            scroll_to_end_x, scroll_to_end_y = pyautogui.center(scroll_to_end_box)
            pyautogui.click(pr(scroll_to_end_x), pr(scroll_to_end_y))
        except (pyautogui.ImageNotFoundException):
            pass

        # find the "..." button – macos.line.more.png. wait 6s.
        more_image = self._get_screenshot_image("macos.line.more.png")
        more_box = pyautogui.locateOnScreen(more_image, 6)
        assert more_box is not None

        # scroll above for 30 times
        for _ in range(30):
            pyautogui.scroll(10000, x=pr(more_box.left), y=(pyautogui.size().height // 2))
            pyautogui.sleep(0.2)

        more_x, more_y = pyautogui.center(more_box)
        pyautogui.click(pr(more_x), pr(more_y))

        # save chat
        save_chat_image = self._get_screenshot_image("macos.line.save-chat.png")
        save_chat_box = pyautogui.locateOnScreen(save_chat_image, 3)
        assert save_chat_box is not None
        save_chat_x, save_chat_y = pyautogui.center(save_chat_box)
        pyautogui.click(pr(save_chat_x), pr(save_chat_y))

        confirm_image = self._get_screenshot_image("macos.line.confirm.png")
        try:
            confirm_box = pyautogui.locateOnScreen(confirm_image, 3, grayscale=True, confidence=0.9)
            assert confirm_box is not None
            confirm_x, confirm_y = pyautogui.center(confirm_box)
            pyautogui.click(pr(confirm_x), pr(confirm_y))
        except (pyautogui.ImageNotFoundException):
            pass  # when users supresses the confirm dialog

        pyautogui.sleep(3)  # wait for saving window

        # copy the original name, which is useful for extracting chat name.
        pyautogui.hotkey("command", "a")
        pyautogui.hotkey("command", "c")
        chat_name = pyperclip.paste()

        if chat_name.startswith("[LINE]"):
            chat_name = chat_name[len("[LINE]"):]

        # remove the content in textbox
        pyautogui.press("backspace", presses = 5, interval = 0.05)

        # save file
        with NamedTemporaryFile(suffix=".txt") as f:
            pyautogui.typewrite(f.name[0])
            pyautogui.sleep(0.75)
            pyautogui.typewrite(f.name[1:], interval=0.1)
            pyautogui.press("enter")

            # wait the save button to be clickable
            save_active_image = self._get_screenshot_image("macos.save.active.png")
            save_active_box = pyautogui.locateOnScreen(save_active_image, 10)
            assert save_active_box is not None
            save_active_x, save_active_y = pyautogui.center(save_active_box)
            pyautogui.click(pr(save_active_x), pr(save_active_y))

            pyautogui.sleep(2.5)  # prevent animations for locating the override button

            # overwrite, of course.
            try:
                overwrite_image = self._get_screenshot_image("macos.save.replace.png")
                overwrite_box = pyautogui.locateOnScreen(overwrite_image, 5, confidence=0.9)
                assert overwrite_box is not None
                overwrite_x, overwrite_y = pyautogui.center(overwrite_box)
                pyautogui.click(pr(overwrite_x), pr(overwrite_y))
            except (pyautogui.ImageNotFoundException):
                logging.warning("override button not found")

            pyautogui.sleep(2)

            # wait 30s for saving. operate now!
            for _ in range(30):
                pyautogui.sleep(1)

                f.seek(0)
                content = f.read()

                if content == "":
                    continue

                return content.decode("utf-8"), chat_name

        return None


    def parse_chat(self, chat_text: str, members: list[str] = []) -> list[LineParsedResult]:
        date_start_regex = re.compile(r"^(\d{4}\.\d{2}\.\d{2}) 星期.$", re.MULTILINE)
        message_start_regex = re.compile(r"^(\d{2}:\d{2}) (.+)$")

        members_regex = "|".join(map(re.escape, members))
        message_split_regex = re.compile(fr"^({members_regex+'|' if members_regex != '' else ''}|.+?) (.+)$", re.MULTILINE)
        logging.debug("message_split_regex: %s", message_split_regex.pattern)

        day_chat_messages: list[str] = date_start_regex.split(chat_text)

        messages = list[LineParsedResult]()
        day_date = datetime.datetime(1970, 1, 1)

        for day_message in day_chat_messages:
            day_message = day_message.strip()

            # 2023.01.01
            try:
                day_date = datetime.datetime.strptime(day_message, "%Y.%m.%d")
                continue
            except ValueError:
                pass

            for message_line in day_message.splitlines():
                message_start_info = message_start_regex.match(message_line)
                if message_start_info is None:
                    if len(messages) == 0:
                        logging.warning("got unexpected part: %s", message_line)
                    else:
                        messages[-1]["message"] += "\n" + message_line
                    continue

                message_sent_time, message_line = message_start_info.groups()
                splited_message = message_split_regex.match(message_line)

                if splited_message is None:
                    # system message. ignore.
                    logging.debug("got system message: %s", message_line)
                    continue

                message_author, first_message_line = splited_message.groups()

                # 00:00
                message_sent_time = datetime.datetime.strptime(message_sent_time, "%H:%M")
                message_sent_time = day_date.replace(hour=message_sent_time.hour, minute=message_sent_time.minute)

                messages.append({
                    "timestamp": message_sent_time,
                    "author": message_author,
                    "message": first_message_line.strip()
                })

        return messages


    def put_to_collection(self, parsed_result: list[LineParsedResult], chat_name: str) -> None:
        self.collection.insert_many((
            {
                "content": message["message"],
                "post_at": message["timestamp"],
                "sender": message["author"],
                "source": chat_name,
            }
            for message in parsed_result
        ))
