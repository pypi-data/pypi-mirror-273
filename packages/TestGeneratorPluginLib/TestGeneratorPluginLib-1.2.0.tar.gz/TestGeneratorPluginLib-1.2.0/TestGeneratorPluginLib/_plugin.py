from typing import Callable, Any

from PyQtUIkit.widgets import KitForm

from TestGeneratorPluginLib import BackendManager, MainTab, SideTab
from TestGeneratorPluginLib._language import _FastRunOption


class Plugin:
    def __init__(self, bm):
        self.main_tabs: dict[str: Callable[[BackendManager], MainTab]] = dict()
        self.side_tabs: dict[str: Callable[[BackendManager], SideTab]] = dict()
        self.fast_run_options: dict[str, list[_FastRunOption]] = dict()
        self.files_context_menu_options: dict[str, tuple[Callable[[], KitForm], Callable[[list], Any]]] = dict()
