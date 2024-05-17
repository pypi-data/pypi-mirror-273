from typing import Callable

from TestGeneratorPluginLib import BackendManager, MainTab, SideTab, Manager
from TestGeneratorPluginLib._language import _FastRunOption


class Plugin:
    def __init__(self, bm):
        self.main_tabs: dict[str: Callable[[BackendManager], MainTab]] = dict()
        self.side_tabs: dict[str: Callable[[BackendManager], SideTab]] = dict()
        self.managers: dict[str: Callable[[BackendManager], Manager]] = dict()
        self.fast_run_options: dict[str, list[_FastRunOption]] = dict()
