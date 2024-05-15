#!/usr/bin/env python
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  author: terry@odd-e.com
#  Website: www.lizard.ws
#
"""
lizard is an extensible Cyclomatic Complexity Analyzer for many programming
languages including C/C++ (doesn't require all the header files).
For more information visit http://www.lizard.ws
"""
from __future__ import print_function, division
import sys
import re
from loguru import logger

try:
    from lizardo.lizard_languages import get_reader_for, CLikeReader
except ImportError:
    sys.stderr.write("Cannot find the lizard_languages module.")
    sys.exit(2)
try:
    from lizardo.lizard_ext import auto_read
except ImportError:
    sys.stderr.write("Cannot find the lizard_ext modules.")

DEFAULT_CCN_THRESHOLD, DEFAULT_WHITELIST, \
    DEFAULT_MAX_FUNC_LENGTH = 15, "whitelizard.txt", 1000


class Nesting(object):  # pylint: disable=R0903
    '''
    Nesting represent one level of nesting in any programming language.
    '''
    @property
    def name_in_space(self):
        return ''

BARE_NESTING = Nesting()

class Namespace(Nesting):  # pylint: disable=R0903

    def __init__(self, name):
        self.name = name

    @property
    def name_in_space(self):
        return self.name + "::" if self.name else ''


class FunctionInfo(Nesting):  # pylint: disable=R0902

    def __init__(self, name, filename, start_line=0, ccn=1):
        self.cyclomatic_complexity = ccn
        self.nloc = 1
        self.token_count = 1  # the first token
        self.name = name
        self.long_name = name
        self.start_line = start_line
        self.end_line = start_line
        self.full_parameters = []
        self.filename = filename
        self.top_nesting_level = -1
        self.fan_in = 0
        self.fan_out = 0
        self.general_fan_out = 0

    @property
    def name_in_space(self):
        return self.name + "."

    @property
    def unqualified_name(self):
        '''
        name without qualification like namespaces or classes.
        Just the bare name without '::'.
        '''
        return self.name.split('::')[-1]

    location = property(lambda self:
                        " %(name)s@%(start_line)s-%(end_line)s@%(filename)s"
                        % self.__dict__)

    parameter_count = property(lambda self: len(self.full_parameters))

    @property
    def parameters(self):
        matches = [re.search(r'(\w+)(\s=.*)?$', f)
                   for f in self.full_parameters]
        return [m.group(1) for m in matches if m]

    @property
    def length(self):
        return self.end_line - self.start_line + 1

    def add_to_function_name(self, app):
        self.name += app
        self.long_name += app

    def add_to_long_name(self, app):
        if self.long_name:
            if self.long_name[-1].isalpha() and app[0].isalpha():
                self.long_name += ' '
        self.long_name += app

    def add_parameter(self, token):
        self.add_to_long_name(" " + token)

        if not self.full_parameters:
            self.full_parameters.append(token)
        elif token == ",":
            self.full_parameters.append('')
        else:
            self.full_parameters[-1] += " " + token


class FileInformation(object):  # pylint: disable=R0903

    def __init__(self, filename, nloc, function_list=None):
        self.filename = filename
        self.nloc = nloc
        self.function_list = function_list or []
        self.token_count = 0

    average_nloc = property(lambda self: self.functions_average("nloc"))
    average_token_count = property(
        lambda self: self.functions_average("token_count"))
    average_cyclomatic_complexity = property(
        lambda self: self.functions_average("cyclomatic_complexity"))
    CCN = property(
        lambda self:
        sum(fun.cyclomatic_complexity for fun in self.function_list))
    ND = property(  # pylint: disable=C0103
        lambda self:
        sum(fun.max_nesting_depth for fun in self.function_list))

    def functions_average(self, att):
        summary = sum(getattr(fun, att) for fun in self.function_list)
        return summary / len(self.function_list) if self.function_list else 0


class NestingStack(object):

    def __init__(self):
        self.nesting_stack = []
        self.pending_function = None
        self.function_stack = []

    def with_namespace(self, name):
        return ''.join([x.name_in_space for x in self.nesting_stack] + [name])

    def add_bare_nesting(self):
        self.nesting_stack.append(self._create_nesting())

    def add_namespace(self, token):
        self.pending_function = None
        self.nesting_stack.append(Namespace(token))

    def start_new_function_nesting(self, function):
        self.pending_function = function

    def _create_nesting(self):
        tmp = self.pending_function
        self.pending_function = None
        if tmp:
            return tmp
        return BARE_NESTING

    def pop_nesting(self):
        self.pending_function = None
        if self.nesting_stack:
            return self.nesting_stack.pop()

    @property
    def current_nesting_level(self):
        return len(self.nesting_stack)

    @property
    def last_function(self):
        funs = [f for f in self.nesting_stack if isinstance(f, FunctionInfo)]
        return funs[-1] if funs else None


class FileInfoBuilder(object):
    '''
    The builder is also referred as "context" in the code,
    because each language readers use this builder to build
    source file and function information and the builder keep
    the context information that's needed for the building.
    '''

    def __init__(self, filename):
        self.fileinfo = FileInformation(filename, 0)
        self.current_line = 0
        self.forgive = False
        self.newline = True
        self.global_pseudo_function = FunctionInfo('*global*', filename, 0)
        self.current_function = self.global_pseudo_function
        self.stacked_functions = []
        self._nesting_stack = NestingStack()

    def __getattr__(self, attr):
        # delegating to _nesting_stack
        return getattr(self._nesting_stack, attr)

    def decorate_nesting_stack(self, decorate_class):
        self._nesting_stack = decorate_class(self._nesting_stack)
        return self._nesting_stack

    def pop_nesting(self):
        nest = self._nesting_stack.pop_nesting()
        if isinstance(nest, FunctionInfo):
            endline = self.current_function.end_line
            self.end_of_function()
            self.current_function = (
                    self._nesting_stack.last_function or
                    self.global_pseudo_function)
            self.current_function.end_line = endline

    def add_nloc(self, count):
        self.fileinfo.nloc += count
        self.current_function.nloc += count
        self.current_function.end_line = self.current_line
        self.newline = count > 0

    def try_new_function(self, name):    
        self.current_function = FunctionInfo(
            self.with_namespace(name),
            self.fileinfo.filename,
            self.current_line)
        self.current_function.top_nesting_level = self.current_nesting_level

    def confirm_new_function(self):
        self.start_new_function_nesting(self.current_function)
        self.current_function.cyclomatic_complexity = 1

    def restart_new_function(self, name):
        self.try_new_function(name)
        self.confirm_new_function()

    def push_new_function(self, name):
        self.stacked_functions.append(self.current_function)
        self.restart_new_function(name)

    def add_condition(self, inc=1):
        """Returns True if maximum cyclomatique complexity is reached"""
        self.current_function.cyclomatic_complexity += inc

    def add_to_long_function_name(self, app):
        self.current_function.add_to_long_name(app)

    def add_to_function_name(self, app):
        self.current_function.add_to_function_name(app)

    def parameter(self, token):
        self.current_function.add_parameter(token)

    def end_of_function(self):
        if not self.forgive:
            self.fileinfo.function_list.append(self.current_function)
        self.forgive = False
        if self.stacked_functions:
            self.current_function = self.stacked_functions.pop()
        else:
            self.current_function = self.global_pseudo_function


def preprocessing(tokens, reader):
    if hasattr(reader, "preprocess"):
        return reader.preprocess(tokens)
    return (t for t in tokens if not t.isspace() or t == '\n')


def comment_counter(tokens, reader):
    for token in tokens:
        comment = reader.get_comment_from_token(token)
        if comment is not None:
            for _ in comment.splitlines()[1:]:
                yield '\n'
            if comment.strip().startswith("#lizard forgive"):
                reader.context.forgive = True
            if "GENERATED CODE" in comment:
                return
        else:
            yield token


def line_counter(tokens, reader):
    context = reader.context
    context.current_line = 1
    newline = 1
    for token in tokens:
        if token != "\n":
            count = token.count('\n')
            context.current_line += count
            context.add_nloc(count + newline)
            newline = 0
            yield token
        else:
            context.current_line += 1
            newline = 1


def token_counter(tokens, reader):
    context = reader.context
    for token in tokens:
        context.fileinfo.token_count += 1
        context.current_function.token_count += 1
        yield token


def condition_counter(tokens, reader):
    conditions = reader.conditions
    
    for i,token in enumerate(tokens):
        if token in conditions:
            reader.context.add_condition()
        yield token


class FileAnalyzer(object):  # pylint: disable=R0903

    def __init__(self, extensions):
        self.processors = extensions

    def __call__(self, filename):
        try:
            return self.analyze_source_code(
                filename, auto_read(filename))
        except UnicodeDecodeError:
            sys.stderr.write("Error: doesn't support none utf encoding '%s'\n"
                             % filename)
        except IOError:
            sys.stderr.write("Error: Fail to read source file '%s'\n"
                             % filename)
        except IndexError:
            sys.stderr.write("Error: Fail to parse file '%s'\n"
                             % filename)
            raise
        return FileInformation(filename, 0, [])

    def analyze_source_code(self, filename, code):
        context = FileInfoBuilder(filename)
        reader = (get_reader_for(filename) or CLikeReader)(context)
        tokens = reader.generate_tokens(code)
        try:
            for processor in self.processors:
                tokens = processor(tokens, reader)
            for _ in reader(tokens, reader):
                pass
        except RecursionError as e:
            sys.stderr.write("[skip] fail to process '%s' with RecursionError - %s\n" % (filename, e))
        return context.fileinfo




def get_extensions(extension_names):
    from importlib import import_module as im

    def expand_extensions(existing):
        for name in extension_names:
            ext = (
                    im('lizard_ext.lizard' + name.lower())
                    .LizardExtension()
                    if isinstance(name, str) else name)
            existing.insert(
                len(existing) if not hasattr(ext, "ordering_index") else
                ext.ordering_index,
                ext)
        return existing

    return expand_extensions([
            preprocessing,
            comment_counter,
            line_counter,
            token_counter,
            condition_counter,
        ])


analyze_file = FileAnalyzer(get_extensions([]))  # pylint: disable=C0103

