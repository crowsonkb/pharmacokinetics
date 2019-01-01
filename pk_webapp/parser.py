"""Parses and evaluates expressions that denote an amount of time."""

from functools import partial, reduce
from operator import mul

import pyparsing as pp
from pyparsing import pyparsing_common as ppc


def _build_expr_parser():
    atom = ppc.fnumber + pp.Optional(pp.oneOf('m h d w'))
    def do_atom(t):
        if len(t) == 2:
            if t[1] == 'm':
                return t[0] / 60
            if t[1] == 'h':
                return t[0]
            if t[1] == 'd':
                return t[0] * 24
            if t[1] == 'w':
                return t[0] * 24 * 7
        return t[0]
    atom.addParseAction(do_atom)

    term = atom + pp.ZeroOrMore(pp.Suppress('*') + atom)
    term.addParseAction(partial(reduce, mul))

    expr = term + pp.ZeroOrMore(pp.Suppress('+') + term)
    expr.addParseAction(sum)

    return expr

_expr_parser = _build_expr_parser()


def parse_expr(s):
    """Parses and evaluates expressions that denote an amount of time."""
    return _expr_parser.parseString(s, parseAll=True)[0]
