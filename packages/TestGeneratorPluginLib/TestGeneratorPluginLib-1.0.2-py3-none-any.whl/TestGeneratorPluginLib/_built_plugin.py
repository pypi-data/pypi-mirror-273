from TestGeneratorPluginLib import Plugin


class BuiltPlugin:
    def __init__(self,
                 plugin: Plugin,
                 platform: str):
        self._plugin = plugin
        self._platform = platform

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
    def dependencies(self) -> list:
        return self._plugin.dependencies

    @property
    def conflicts(self) -> list:
        return self._plugin.conflicts

