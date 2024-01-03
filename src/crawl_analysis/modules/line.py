from pathlib import Path
import platform
import subprocess
from tempfile import NamedTemporaryFile
import time
import pyautogui
import pyperclip
from torch import le


class LineCrawler:
    def __init__(self):
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

    def search_group(self, group_name: str) -> str:
        if platform.system() == "Darwin":
            return self.search_group_mac(group_name)
        # elif platform.system() == "Windows":
            # self.search_group_windows(group_name)
        else:
            raise NotImplementedError("unsupported platform")

    def search_group_mac(self, group_name: str) -> str:
        pixel_ratio = pyautogui.screenshot().size[0] / pyautogui.size().width
        pr = lambda x: x // pixel_ratio

        pyautogui.sleep(3)  # wait focusing.

        # find the search bar – macos.line.search.png. wait 3s.
        search_bar_image = self._get_screenshot_image("macos.line.search.png")
        search_bar_box = pyautogui.locateOnScreen(search_bar_image, 3)
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
        confirm_box = pyautogui.locateOnScreen(confirm_image, 3, grayscale=True, confidence=0.9)
        assert confirm_box is not None
        confirm_x, confirm_y = pyautogui.center(confirm_box)
        pyautogui.click(pr(confirm_x), pr(confirm_y))
        pyautogui.sleep(3)  # wait for saving window

        # save file
        with NamedTemporaryFile(suffix=".txt") as f:
            pyautogui.typewrite(f.name[0])
            pyautogui.sleep(0.75)
            pyautogui.typewrite(f.name[1:], interval=0.1)
            pyautogui.press("enter", presses=4, interval=0.5)

            # check if there are content - wait for 30s
            for i in range(0, 30):
                pyautogui.sleep(1)
                f.seek(0)
                content = f.read()
                if len(content) > 0:
                    return content.decode("utf-8")

        return "<no result>"
