import argparse
import os
import shutil
import subprocess
import sys
from sys import argv
from typing import Iterable, Callable

from TestGeneratorPluginLib import BackendManager, Manager
from TestGeneratorPluginLib._language import _FastRunOption
from TestGeneratorPluginLib._widgets import MainTab, SideTab


class Plugin:
    def __init__(self,
                 name: str,
                 description: str,
                 version: str,
                 author: str,
                 url='',
                 platform_specific: bool = None,
                 dependencies: Iterable[str] = tuple(),
                 conflicts: Iterable[str] = tuple(),

                 directories: Iterable[str] = tuple(),
                 requirements: Iterable[str] = tuple(),

                 main_tabs: dict[str: Callable[[BackendManager], MainTab]] = None,
                 side_tabs: dict[str: Callable[[BackendManager], SideTab]] = None,
                 managers: dict[str: Callable[[BackendManager], Manager]] = None,
                 fast_run_options: dict[str, list[_FastRunOption]] = None,
                 ):
        self.name = name
        self.description = description
        self.version = version
        self.author = author
        self.url = url
        self.platform_specific = bool(requirements) if platform_specific is None else platform_specific
        self.dependencies = list(dependencies)
        self.conflicts = list(conflicts)

        self._directories = list(directories)
        self._requirements = list(requirements)

        self.main_tabs = main_tabs or dict()
        self.side_tabs = side_tabs or dict()
        self.managers = managers or dict()
        self.fast_run_options = fast_run_options or dict()

        self._parse_args()

    def _parse_args(self):
        _parser = argparse.ArgumentParser()
        _parser.add_argument('-b', '--build', action='store_true')
        _parser.add_argument('-o', '--output')
        _parser.add_argument('-u', '--upload', action='store_true')
        args = _parser.parse_args()

        if args.build:
            self._build(args.output)

    def _build(self, output=None):
        build_path = f'build/{self.name}'
        dist_path = output or f'dist/{self.name}.TGPlugin'
        if os.path.isdir(build_path):
            shutil.rmtree(build_path)
        os.makedirs(build_path)
        if os.path.dirname(dist_path):
            os.makedirs(os.path.dirname(dist_path), exist_ok=True)

        for el in self._directories:
            shutil.copytree(el, os.path.join(build_path, el))
        shutil.copy(argv[0], os.path.join(build_path, os.path.basename(argv[0])))

        if self._requirements:
            subprocess.run(['pip', 'install', *self._requirements, '-t', os.path.join(build_path, '__packages__')])

        with open(os.path.join(build_path, '__plugin__.py'), 'w', encoding='utf-8') as f:
            f.write(f"""from TestGeneratorPluginLib._built_plugin import BuiltPlugin
from {os.path.basename(argv[0][:-3])} import plugin

__plugin__ = BuiltPlugin(plugin, '{sys.platform}')
""")

        shutil.make_archive(dist_path, 'zip', build_path)
