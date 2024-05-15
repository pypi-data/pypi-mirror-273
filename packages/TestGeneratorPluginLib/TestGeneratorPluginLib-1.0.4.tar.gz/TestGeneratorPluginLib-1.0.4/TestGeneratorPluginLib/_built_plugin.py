from typing import Callable

from TestGeneratorPluginLib._language import _FastRunOption
from TestGeneratorPluginLib._plugin import Plugin
from TestGeneratorPluginLib._managers import BackendManager, Manager
from TestGeneratorPluginLib._widgets import MainTab, SideTab


class BuiltPlugin:
    def __init__(self,
                 plugin: Plugin,
                 platform: str):
        self._plugin = plugin
        self._platform = platform if plugin.platform_specific else ''

    @property
    def name(self) -> str:
        return self._plugin.name

    @property
    def description(self) -> str:
        return self._plugin.description

    @property
    def version(self) -> str:
        return self._plugin.version

    @property
    def author(self) -> str:
        return self._plugin.author

    @property
    def url(self) -> str:
        return self._plugin.url

    @property
    def platform(self) -> str:
        return self._platform

    @property
    def dependencies(self) -> list[str]:
        return self._plugin.dependencies

    @property
    def conflicts(self) -> list[str]:
        return self._plugin.conflicts

    @property
    def main_tabs(self) -> dict[str: Callable[[BackendManager], MainTab]]:
        return self._plugin.main_tabs

    @property
    def side_tabs(self) -> dict[str: Callable[[BackendManager], SideTab]]:
        return self._plugin.side_tabs

    @property
    def managers(self) -> dict[str: Callable[[BackendManager], Manager]]:
        return self._plugin.managers

    @property
    def fast_run_options(self) -> dict[str, _FastRunOption]:
        return self._plugin.fast_run_options

