# -*- coding: utf-8 -*-
# Copyright (c) 2012 by Pablo Martín <goinnn@gmail.com>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

import compiler
import glob
import os
import pkgutil
import sys

from pysmell.codefinder import CodeFinder, ModuleDict

PYSMELL_PREFIX = '__package____module__.'


class PyPleteModuleDict(ModuleDict):

    def addPointer(self, name, pointer):
        if not name == '%s*' % PYSMELL_PREFIX:
            super(PyPleteModuleDict, self).addPointer(name, pointer)
        else:
            if not name in self['POINTERS']:
                self['POINTERS'][name] = []
            self['POINTERS'][name].append(pointer)


class PyPlete(object):

    def __init__(self, func_info=None, pythonpath=None, separator='.', *args, **kwargs):
        super(PyPlete, self).__init__(*args, **kwargs)
        if func_info:
            self.func_info = func_info
        if pythonpath:
            self.pythonpath = pythonpath
        else:
            self.pythonpath = sys.path
        self.separator = separator
        self.get_importables_top_level([])

    def func_info(self, **kwargs):
        return kwargs

    def get_importables_top_level(self, list_autocomplete, use_cache=True):
        # http://code.google.com/p/djangode/source/browse/trunk/djangode/data/codemodel/codemodel.py#57
        if use_cache and getattr(self, 'importables_top_level', None):
            list_autocomplete.extend(self.importables_top_level)
            return bool(len(list_autocomplete))
        self.importables_top_level = []
        self.importables_path = {}
        for directory in self.pythonpath:
            for filename in glob.glob(directory + os.sep + "*"):
                name = None
                if filename.endswith(".py"):
                    name = filename.split(os.sep)[-1][:-3]
                    category = 'module'
                elif os.path.isdir(filename) and os.path.exists(filename + os.sep + "__init__.py"):
                    name = filename.split(os.sep)[-1]
                    category = 'package'
                if not name:
                    continue
                importable = self.func_info(text=name, category=category)
                if importable and not importable in self.importables_top_level:
                    self.importables_top_level.append(importable)
                    self.importables_path[name] = [filename]
        list_autocomplete.extend(self.importables_top_level)
        return list_autocomplete and bool(len(list_autocomplete))

    def get_importables_rest_level(self, list_autocomplete, imp_name, subimportables=None, into_module=True):
        if not self.importables_path.get(imp_name):
            return False
        imp_path = self.importables_path.get(imp_name)[0]
        subimportables = subimportables or []
        subimportables = [subimportable for subimportable in subimportables if subimportable]
        if subimportables:
            subimportables_path = os.sep.join(subimportables)
            imp_path = "%s%s%s" % (imp_path, os.sep, subimportables_path)
        for loader, name, is_pkg in pkgutil.walk_packages([imp_path]):
            category = is_pkg and 'package' or 'module'
            importable = self.func_info(text=name, category=category)
            list_autocomplete.append(importable)
        if into_module:
            into_dir = os.sep.join(imp_path.split(os.sep)[:-1])
            into_module = imp_path.split(os.sep)[-1].replace('.py', '').replace('.pyc', '')
            importer = pkgutil.get_importer(into_dir)
            imp = importer.find_module(into_module)
            source = imp and imp.get_source()
            if source:
                self.get_importables_from_text(list_autocomplete, source, path=['django', 'forms'])
        return list_autocomplete and bool(len(list_autocomplete))

    def get_importables_from_text(self, list_autocomplete, text, path=None):
        code_walk = self.get_pysmell_code_walk_to_text(text)
        pysmell_modules = code_walk.modules
        treatment_dict = {'CONSTANTS': self.treatment_pysmell_const,
                          'FUNCTIONS': self.treatment_pysmell_func,
                          'CLASSES': self.treatment_pysmell_cls,
                          'POINTERS': self.treatment_pysmell_pointer}
        for key, func in treatment_dict.items():
            pysmell_items = pysmell_modules[key]
            if isinstance(pysmell_items, dict):
                pysmell_items = pysmell_items.items()
            for pysmell_item in pysmell_items:
                item = func(pysmell_item, pysmell_modules, path)
                if item:
                    if isinstance(item, list):
                        list_autocomplete.extend(item)
                    elif not item in list_autocomplete:
                        list_autocomplete.append(item)
        list_autocomplete = self._reduce_pointer(list_autocomplete)
        return len(list_autocomplete) > 0

    def _reduce_pointer(self, list_autocomplete):
        list_autocomplete.sort(cmp=lambda x, y: cmp(x['category'], y['category']))
        list_autocomplete_text = [x['text'] for x in list_autocomplete]
        i = len(list_autocomplete) - 1
        while i >= 0:
            item = list_autocomplete[i]
            index = list_autocomplete.index(item)
            if i != index:
                del list_autocomplete[i]
            elif item['category'] == 'pointer':
                index_text = list_autocomplete_text.index(item['text'])
                if i != index_text:
                    del list_autocomplete[i]
            i = i - 1
        return list_autocomplete

    def get_importables_from_line(self, list_autocomplete, text, code_line, text_info=True):
        pysmell_modules = self.get_pysmell_modules_to_text(text)
        code_line_split = code_line.split(self.separator)
        prefix = code_line_split[0]
        prfx_code_line = '%s%s' % (PYSMELL_PREFIX, prefix)
        if prfx_code_line in pysmell_modules['CONSTANTS']:
            return False
        elif pysmell_modules['CLASSES'].get(prfx_code_line, None) and not code_line_split[1:]:
            class_smell = pysmell_modules['CLASSES'].get(prfx_code_line)
            self.treatment_pysmell_into_cls(class_smell, pysmell_modules, list_autocomplete)
            return True
        elif prfx_code_line in [name for name, args, desc in pysmell_modules['FUNCTIONS']]:
            index_func = [f[0] for f in pysmell_modules['FUNCTIONS']].index(prfx_code_line)
            func_smell = pysmell_modules['FUNCTIONS'][index_func]
            list_autocomplete.append(self.treatment_pysmell_into_func(func_smell))
            return True
        elif pysmell_modules['POINTERS'].get(prfx_code_line, None):
            module_path = pysmell_modules['POINTERS'].get(prfx_code_line, None)
            module = module_path.split(self.separator)[0]
            submodules = module_path.split(self.separator)[1:]
            submodules.extend(code_line_split[1:])
            imp_loader, submodules_undone = self.get_imp_loader_from_path(module, submodules)
            if not submodules_undone:
                self.get_importables_rest_level(list_autocomplete, module, submodules, True)
            submodules_undone.reverse()
            line = self.separator.join(submodules_undone)
            text = imp_loader.get_source()
            if line:
                return self.get_importables_from_line(list_autocomplete, text, line)
            if text_info:
                return self.get_importables_from_text(list_autocomplete, text)
        return False

    def get_pysmell_code_walk_to_text(self, text):
        code = compiler.parse(text)
        codefinder = CodeFinder()
        codefinder.modules = PyPleteModuleDict()
        return compiler.walk(code, codefinder)

    def get_pysmell_modules_to_text(self, text):
        return self.get_pysmell_code_walk_to_text(text).modules

    def get_imp_loader_from_path(self, imp_name, subimportables, subimportables_undone=None):
        if not imp_name in self.importables_path:
            return (None, [])
        imp_path = self.importables_path[imp_name][0]
        subimportables_undone = subimportables_undone or []
        subimportables_str = os.sep.join(subimportables)
        if subimportables_str:
            imp_path = "%s%s%s" % (imp_path, os.sep, subimportables_str)
        into_dir = os.sep.join(imp_path.split(os.sep)[:-1])
        into_module = imp_path.split(os.sep)[-1].replace('.py', '').replace('.pyc', '')
        importer = pkgutil.get_importer(into_dir)
        importable = importer.find_module(into_module)
        if importable:
            return (importable, subimportables_undone)
        elif subimportables:
            subimportables_undone.append(subimportables[-1])
            return self.get_imp_loader_from_path(imp_name, subimportables[:-1], subimportables_undone)
        return (None, subimportables_undone)

    def treatment_pysmell_const(self, constant, modules=None, path=None):
        constant = constant.replace(PYSMELL_PREFIX, '')
        return self.func_info(text=constant, category='constant')

    def treatment_pysmell_func(self, func, modules=None, path=None):
        func_name, args, description = func
        func_name = func_name.replace(PYSMELL_PREFIX, '')
        args = ', '.join(args)
        args = ' (%s)' % args
        return self.func_info(text=func_name,
                              category='function',
                              args=args,
                              description=description)

    def treatment_pysmell_into_func(self, func, path=None):
        return self.treatment_pysmell_func(func, path=path)

    def treatment_pysmell_constructor(self, cls_name, args_constructor, description=None, path=None):
        args_constructor = ', '.join(args_constructor)
        args_constructor = ' (%s)' % args_constructor
        return self.func_info(text=cls_name,
                             category='class',
                             args=args_constructor,
                             description=description)

    def treatment_pysmell_cls(self, cls, modules, path=None):
        cls_name, info = cls
        cls_name = cls_name.replace(PYSMELL_PREFIX, '')
        args_constructor = self.get_pysmell_constructor(info, modules)
        return self.treatment_pysmell_constructor(cls_name, args_constructor, info.get('docstring', None), path)

    def treatment_pysmell_pointer(self, pointer, modules=None, path=None):
        pointer_name, pointer_path = pointer
        if isinstance(pointer_path, list):  # when there is __package____module__.*
            list_autocomplete = []
            for pointer_path_item in pointer_path:
                list_autocomplete_item = self.treatment_pysmell_pointer((pointer_name, pointer_path_item),
                                                                         modules=modules, path=path)
                list_autocomplete.extend(list_autocomplete_item)
            return list_autocomplete
        else:
            pointer_name = pointer_name.replace(PYSMELL_PREFIX, '')
            if not pointer_path.startswith('__'):
                if pointer_name == '*':
                    pointer_path_split = pointer_path.split('.')
                    if pointer_path_split:
                        list_autocomplete = []
                        imp_name = pointer_path_split[0]
                        subimportables = pointer_path_split[1:-1]
                        is_auto = self.get_importables_rest_level(list_autocomplete, imp_name, subimportables, True)
                        if not is_auto and path:
                            subimportables = path[1:] + [imp_name] + subimportables
                            self.get_importables_rest_level(list_autocomplete, path[0], subimportables, True)
                        return list_autocomplete
                else:
                    return self.func_info(text=pointer_name, category='pointer')

    def treatment_pysmell_into_cls(self, cls, modules, list_autocomplete, inherited_methods=None):
        inherited_methods = inherited_methods or []
        for m in cls['methods']:
            if m[0] in inherited_methods:
                continue
            inherited_methods.append(m[0])
            item = self.treatment_pysmell_func(m)
            if not item in list_autocomplete:
                list_autocomplete.append(item)
        for m in cls['properties']:
            item = self.treatment_pysmell_const(m)
            if not item in list_autocomplete:
                list_autocomplete.append(item)
        bases = cls['bases']
        for base in bases:
            base_info = self.get_parent_pysmell_info(base, modules)
            if base_info:
                return self.treatment_pysmell_into_cls(base_info, modules,
                                        list_autocomplete, inherited_methods)

    def get_pysmell_constructor(self, info, modules):
        constructor = info.get('constructor', None)
        if constructor:
            return constructor
        bases = info['bases']
        for base in bases:
            if base == 'object':
                continue
            base_info = self.get_parent_pysmell_info(base, modules)
            if not base_info:
                continue
            constructor = base_info.get('constructor', None)
            if constructor:
                return constructor
            return self.get_pysmell_constructor(base_info, modules)
        return ''

    def get_parent_pysmell_info(self, base, modules):
        cls_name = base.replace(PYSMELL_PREFIX, '')
        base_info = modules['CLASSES'].get(base, None)
        if not base_info:
            base_path = base.split('.')
            imp_loader, submodules_undone = self.get_imp_loader_from_path(base_path[0], base_path[1:])
            if len(submodules_undone) != 1:
                return None
            cls_name = '%s%s' % (PYSMELL_PREFIX, submodules_undone[0])
            source = imp_loader.get_source()
            if source:
                base_info = self.get_pysmell_modules_to_text(imp_loader.get_source())['CLASSES'].get(cls_name, None)
        return base_info
