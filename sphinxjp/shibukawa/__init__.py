# -*- coding: utf-8 -*-
"""
    sphinxjp.shibukawa
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Allow DOT like formatted charts to be included in Sphinx-generated
    documents inline.

    :copyright: Copyright 2010 by Takeshi Komiya.
    :license: BSDL.
"""

import posixpath
import os
import codecs
try:
    from hashlib import sha1 as sha
except ImportError:
    from sha import sha

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx.errors import SphinxError
from sphinx.util.osutil import ensuredir, ENOENT, EPIPE
from sphinx.util.compat import Directive

from sphinxjp.shibukawa import core


__import__('pkg_resources').declare_namespace(__name__)


class ScheduleError(SphinxError):
    category = 'Schedule error'


class schedule(nodes.General, nodes.Element):
    pass


class Schedule(Directive):
    """
    Directive to insert arbitrary dot markup.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        'size': directives.unchanged,
    }

    codeheadings = None

    def run(self):
        dotcode = '\n'.join(self.content)
        if not dotcode.strip():
            return [self.state_machine.reporter.warning(
                'Ignoring "chart" directive without content.',
                line=self.lineno)]

        if self.codeheadings:
            if self.arguments:
                graph_name = self.arguments[0]
                dotcode = "%s %s { %s }" % (self.codeheadings, graph_name, dotcode)
            else:
                dotcode = "%s { %s }" % (self.codeheadings, dotcode)

        node = schedule()
        node['code'] = dotcode
        node['options'] = {}
        if 'size' in self.options:
            node['options']['size'] = self.options['size']

        return [node]


# compatibility to sphinx 1.0 (ported from sphinx trunk)
def relfn2path(env, filename, docname=None):
    if filename.startswith('/') or filename.startswith(os.sep):
        rel_fn = filename[1:]
    else:
        docdir = os.path.dirname(env.doc2path(docname or env.docname,
                                              base=None))
        rel_fn = os.path.join(docdir, filename)
    try:
        return rel_fn, os.path.join(env.srcdir, rel_fn)
    except UnicodeDecodeError:
        # the source directory is a bytestring with non-ASCII characters;
        # let's try to encode the rel_fn in the file system encoding
        enc_rel_fn = rel_fn.encode(sys.getfilesystemencoding())
        return rel_fn, os.path.join(env.srcdir, enc_rel_fn)


def get_image_filename(self, code, options, prefix='schedule'):
    """
    Get path of output file.
    """
    hashkey = code.encode('utf-8') + str(options)
    fname = '%s-%s.png' % (prefix, sha(hashkey).hexdigest())
    if hasattr(self.builder, 'imgpath'):
        # HTML
        relfn = posixpath.join(self.builder.imgpath, fname)
        outfn = os.path.join(self.builder.outdir, '_images', fname)
    else:
        # LaTeX
        relfn = fname
        outfn = os.path.join(self.builder.outdir, fname)

    if os.path.isfile(outfn):
        return relfn, outfn

    ensuredir(os.path.dirname(outfn))

    return relfn, outfn


def render_dot_html(self, node, code, options, prefix='schedule',
                    imgcls=None, alt=None):
    has_thumbnail = False
    try:
        relfn, outfn = get_image_filename(self, code, options, prefix)
        if not os.path.isfile(outfn):
            core.Schedule(code).save(outfn)
    except ScheduleError, exc:
        self.builder.warn('dot code %r: ' % code + str(exc))
        raise nodes.SkipNode

    self.body.append(self.starttag(node, 'p', CLASS='schedule'))
    if relfn is None:
        self.body.append(self.encode(code))
    else:
        if alt is None:
            alt = node.get('alt', self.encode(code).strip())

        imgtag_format = '<img src="%s" alt="%s" />\n'
        self.body.append(imgtag_format % (relfn, alt))

    self.body.append('</p>\n')
    raise nodes.SkipNode


def html_visit_schedule(self, node):
    render_dot_html(self, node, node['code'], node['options'])


def render_dot_latex(self, node, code, options, prefix='schedule'):
    try:
        fname, outfn = get_image_filename(self, code, options, prefix)
        core.Schedule(code).save(outfn)
    except ScheduleError, exc:
        self.builder.warn('dot code %r: ' % code + str(exc))
        raise nodes.SkipNode

    if fname is not None:
        self.body.append('\\par\\includegraphics{%s}\\par' % fname)
    raise nodes.SkipNode


def latex_visit_schedule(self, node):
    render_dot_latex(self, node, node['code'], node['options'])


def setup(app):
    app.add_node(schedule,
                 html=(html_visit_schedule, None),
                 latex=(latex_visit_schedule, None))
    app.add_directive('schedule', Schedule)
