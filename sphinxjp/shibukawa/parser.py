# -*- coding: utf-8 -*-

import codecs
import datetime
import re
from re import MULTILINE, DOTALL
from funcparserlib.lexer import make_tokenizer, Token, LexerError
from funcparserlib.parser import (some, a, maybe, many, finished, skip,
    oneplus, forward_decl, NoParseError)

try:
    from collections import namedtuple
except:
    def namedtuple(name, fields):
        'Only space-delimited fields are supported.'
        def prop(i, name):
            return (name, property(lambda self: self[i]))
        methods = dict(prop(i, f) for i, f in enumerate(fields.split(' ')))
        methods.update({
            '__new__': lambda cls, *args: tuple.__new__(cls, args),
            '__repr__': lambda self: '%s(%s)' % (
                name,
                ', '.join('%s=%r' % (
                    f, getattr(self, f)) for f in fields.split(' ')))})
        return type(name, (tuple,), methods)


ENCODING = 'utf-8'

Chart = namedtuple('Chart', 'stmts')
Node = namedtuple('Node', 'id starts ends')


class ParseException(Exception):
    pass


def tokenize(str):
    'str -> Sequence(Token)'
    specs = [
        ('Comment', (r'/\*(.|[\r\n])*?\*/', MULTILINE)),
        ('Comment', (r'//.*',)),
        ('NL',      (r'[\r\n]+',)),
        ('Space',   (r'[ \t\r\n]+',)),
        ('Date',    (r'[0-9]+(/[0-9]+){1,2}',)),
        ('Name',    (ur'[A-Za-z_\u0080-\uffff][A-Za-z_0-9\.\u0080-\uffff]*',)),
        ('Op',      (r'[{}():;,\-=\[\]]',)),
        ('Color',  (r'[A-Za-z0-9]+',)),
        ('Number',  (r'-?(\.[0-9]+)|([0-9]+(\.[0-9]*)?)',)),
        ('String',  (r'(?P<quote>"|\').*?(?<!\\)(?P=quote)', DOTALL)),
    ]
    useless = ['Comment', 'NL', 'Space']
    t = make_tokenizer(specs)
    return [x for x in t(str) if x.type not in useless]


def parse(seq):
    'Sequence(Token) -> object'
    unarg = lambda f: lambda args: f(*args)
    tokval = lambda x: x.value
    n = lambda s: a(Token('Name', s)) >> tokval
    op = lambda s: a(Token('Op', s)) >> tokval
    op_ = lambda s: skip(op(s))
    id = some(lambda t:
        t.type in ['Name', 'Number', 'Color', 'String']).named('id') >> tokval
    date = some(lambda t: t.type == 'Date').named('date') >> tokval
    make_node = lambda args: Node(*args)

    node_stmt = id + op_(':') + date + maybe(op_('-') + date) >> make_node
    chart = (
        many(node_stmt + skip(maybe(op(';'))))
        >> Chart)
    dotfile = chart + skip(finished)

    return dotfile.parse(seq)


def unquote(string):
    if string:
        m = re.match('\A(?P<quote>"|\')((.|\s)*)(?P=quote)\Z', string, re.M)
        if m:
            return re.sub("\\\\" + m.group(1), m.group(1), m.group(2))
        else:
            return string
    else:
        return string


def str2date(date):
    parts = unquote(date).split('/')
    if len(parts) == 2:
        today = datetime.date.today()
        obj = datetime.date(today.year, int(parts[0]), int(parts[1]))
    elif len(parts) == 3:
        obj = datetime.date(*[int(p) for p in parts])
    else:
        raise

    return obj


class Schedule(object):
    def __init__(self):
        self.items = []

    def append(self, node):
        self.items.append(_Node(node))

    @property
    def max(self):
        return max(n.ends for n in self.items)

    @property
    def min(self):
        return min(n.starts for n in self.items)

    @property
    def days(self):
        return (self.max - self.min).days + 1

    def far_to(self, node):
        return (node.starts - self.min).days


class _Node(object):
    def __init__(self, obj):
        self.label = obj.id
        self.starts = str2date(obj.starts)
        if obj.ends:
            self.ends = str2date(obj.ends)
        else:
            self.ends = self.starts

        if self.starts > self.ends:
            raise AttributeError('caught starts > ends: %s' % self.label)

    @property
    def width(self):
        return (self.ends - self.starts).days + 1


def parse_string(code):
    tree = parse(tokenize(code))

    schedule = Schedule()
    for stmt in tree.stmts:
        if isinstance(stmt, Node):
            schedule.append(stmt)

    return schedule


def parse_file(path):
    try:
        input = codecs.open(path, 'r', 'utf-8').read()
        return parse_string(input)
    except LexerError, e:
        message = "Got unexpected token at line %d column %d" % e.place
        raise ParseException(message)
    except Exception, e:
        raise ParseException(str(e))
