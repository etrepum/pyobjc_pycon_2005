#!/usr/bin/env python
import cStringIO, cgi, sys, urllib, os
import docutils.core, docutils.io
from docutils import writers, nodes, languages
from reportlab.tools.pythonpoint import pythonpoint
import Image

def _hackhackhack():
    styles = pythonpoint.getStyles()
    codeStyle = styles['Code']
    codeStyle.leftIndent = 72
    codeStyle.leading = 36
    codeStyle.spaceBefore = 24
    styles['Code'] = codeStyle
    pythonpoint.setStyles(styles)
#_hackhackhack()

class Writer(writers.Writer):

    settings_spec = ()
    settings_default_overrides = {}
    output = None

    def translate(self):
        visitor = DumbPythonPointFormatter(self.document)
        self.document.walkabout(visitor)
        self.output = visitor.astext()
        #self.head_prefix = visitor.head_prefix
        #self.head = visitor.head
        #self.body_prefix = visitor.body_prefix
        #self.body = visitor.body
        #self.body_suffix = visitor.body_suffix

class DumbPythonPointFormatter(nodes.NodeVisitor):

    def __init__(self, document):
        nodes.NodeVisitor.__init__(self, document)
        self.section = 0
        self.closers = []
        self.slidenum = 0
        self.body = []
        self.w = self.body.append
        self.suppress_para = 0

    def astext(self):
        return ''.join(self.body)

    def visit_reference(self, node):
        pass

    def depart_reference(self, node):
        pass

    def visit_document(self, node):
        self.w('<presentation>\n'
        '<stylesheet module="modern" function="getParagraphStyles"/>\n'
        '<section name="Main">\n'
        '<fixedimage filename="../../sidebar.jpg"'
        ' height="600" width="150" x="0" y="0" />\n'
        )

    def depart_document(self, node):
        self.w('</section>\n'
        '</presentation>\n')

    def visit_section(self, node):
        #if node.attributes.has_key('dupname'):
        #    name = node.attributes['dupname']
        #else:
        #    name = node.attributes['name']

        # HACK HACK HACK
        name = node.astext().split('\n', 1)[0]
        self.slidenum += 1
        self.w('<slide id="Slide%03d" title="%s">\n'
               '<frame x="110" y="30" width="690" height="520" leftmargin="12"'
               ' rightmargin="0">\n'%(self.slidenum, name))

    def depart_section(self, node):
        self.w('</frame>\n</slide>\n')

    def visit_title(self, node):
        self.w('<para style="Heading1">')
        self.suppress_para = 1

    def depart_title(self, node):
        self.suppress_para = 0
        self.w('</para>\n')

    def visit_paragraph(self, node):
        if not self.suppress_para: self.w('<para style="BodyText">')

    def depart_paragraph(self, node):
        if not self.suppress_para: self.w('</para>\n')

    # Simple lists
    def visit_bullet_list(self, node):
        pass

    def depart_bullet_list(self, node):
        pass

    def visit_enumerated_list(self, node):
        pass

    def depart_enumerated_list(self, node):
        pass

    def visit_list_item(self, node):
        self.w('<para style="Bullet">')
        self.suppress_para = 1

    def depart_list_item(self, node):
        self.suppress_para = 0
        self.w('</para>\n')

    # Definition List
    def visit_definition_list(self, node):
        pass

    def depart_definition_list(self, node):
        pass

    def visit_definition_list_item(self, node):
        pass

    def depart_definition_list_item(self, node):
        pass

    def visit_term(self, node):
        self.w('<para><b>')

    def depart_term(self, node):
        self.w('</b>')

    def visit_classifier(self, node):
        self.w('<i>')

    def depart_classifier(self, node):
        self.w('</i>')

    def visit_definition(self, node):
        self.w('</para>\n<para style="Definition">')
        self.suppress_para = 1

    def depart_definition(self, node):
        self.suppress_para = 0
        self.w('</para>\n')

    def visit_field(self, node):
        self.w('<para>')

    def depart_field(self, node):
        self.w('</para>\n')

    def visit_field_body(self, node):
        self.suppress_para = 1
        return

    def depart_field_body(self, node):
        self.suppress_para = 0

    def visit_field_list(self, node):
        return

    def depart_field_list(self, node):
        return

    def visit_field_name(self, node):
        self.w('<b>')

    def depart_field_name(self, node):
        self.w(':')
        self.w('</b>')
    
    # Literal Block
    def visit_literal_block(self, node):
        self.w('<para style="BodyText"></para><pycode style="Code">')
        self.suppress_para = 1

    def depart_literal_block(self, node):
        self.suppress_para = 0
        self.w('</pycode>\n')

    # Block Quote
    def visit_block_quote(self, node):
        self.w('<para style="Indent">')

    def depart_block_quote(self, node):
        self.w('</para>\n')

    def visit_image(self, node):
        ''' EMPTY
            uri       CDATA     #REQUIRED
            alt       CDATA     #IMPLIED
            height    NMTOKEN   #IMPLIED
            width     NMTOKEN   #IMPLIED
            scale     NMTOKEN   #IMPLIED
        '''
        attrs = node.attributes
        # TODO: scale
        uri = node.attributes['uri']
        try:
            img = Image.open(uri)
        except IOError:
            uri = uri[3:]
            img = Image.open(uri)
        w, h = img.size
        print '%dx%d %s' % (w, h, uri)
        if h > 420:
            nw = int((w * 420) / float(h))
            nh = 420
        else:
            nw, nh = w, h
        self.w('<image filename="../%s" width="%d" height="%d" />' %
            (uri, nw, nh))


    def depart_image(self, node):
        pass

    #
    # Tables:
    #  NOT IN DOM YET
    #
    def visit_table(self, node):
        '''
            +------------------------+------------+----------+----------+
            | Header row, column 1   | Header 2   | Header 3 | Header 4 |
            | (header rows optional) |            |          |          |
            +========================+============+==========+==========+
            | body row 1, column 1   | column 2   | column 3 | column 4 |
            +------------------------+------------+----------+----------+
            | body row 2             | Cells may span columns.          |
            +------------------------+------------+---------------------+
            | body row 3             | Cells may  | - Table cells       |
            +------------------------+ span rows. | - contain           |
            | body row 4             |            | - body elements.    |
            +------------------------+------------+---------------------+
        '''
        self.w('<table border=1>\n')

    def depart_table(self, node):
        self.w('</table>\n')

    def visit_tgroup(self, node):
        pass

    def depart_tgroup(self, node):
        pass

    def visit_colspec(self, node):
        pass

    def depart_colspec(self, node):
        pass

    def visit_row(self, node):
        self.body.append(self.starttag(node, 'tr', ''))

    def depart_row(self, node):
        self.body.append('</tr>\n')

    def visit_thead(self, node):
        self.thead = 1

    def depart_thead(self, node):
        self.thead = 0

    def visit_tbody(self, node):
        self.thead = 1

    def depart_tbody(self, node):
        self.thead = 0

    def visit_entry(self, node):
        if self.thead:
            s = 'th '
        else:
            s = 'td '
        attrs = node.attributes
        if attrs.has_key('morecols'):
            s = s + 'colspan=%d '%(attrs['morecols']+1)
        if attrs.has_key('morerows'):
            s = s + 'rowspan=%d '%(attrs['morerows']+1)
        self.w('<%svalign="top" align="left">'%s)

    def depart_entry(self, node):
        if self.thead:
            self.w('</th>\n')
        else:
            self.w('</td>\n')

    def visit_emphasis(self, node):
        self.w('<i>')

    def depart_emphasis(self, node):
        self.w('</i>')

    def visit_strong(self, node):
        self.w('<b>')

    def depart_strong(self, node):
        self.w('</b>')

    def visit_interpreted(self, node):
        pass #raise NotImplementedError, node

    def depart_interpreted(self, node):
        pass #raise NotImplementedError, node

    def visit_literal(self, node):
        self.w('<div style="Code">')

    def depart_literal(self, node):
        self.w('</div>')

    def visit_reference(self, node):
        attrs = node.attributes
        doc = self.document
        ok = 1
        if attrs.has_key('refuri'):
            self.w('<a href="%s">'%attrs['refuri'])
        elif doc.explicit_targets.has_key(attrs['refname']):
            # an external reference has been defined
            ref = doc.explicit_targets[attrs['refname']]
            if ref.attributes.has_key('refuri'):
                self.w('<a href="%s">'%ref.attributes['refuri'])
            else:
                self.w('<a href="#%s">'%attrs['refname'])
        elif doc.implicit_targets.has_key(attrs['refname']):
            # internal reference
            name = attrs['refname']
            self.w('<a href="#%s">'%urllib.quote(name))
        else:
            self.w('<span class="formatter_error">target "%s" '
                'undefined</span>'%attrs['refname'])

    def depart_reference(self, node):
        self.w('</a>')

    def visit_footnote_reference(self, node):
        raise NotImplementedError, node

    def visit_substitution_reference(self, node):
        pass

    def depart_substitution_reference(self, node):
        pass

    def visit_problematic(self, node):
        raise NotImplementedError, node

    def depart_problematic(self, node):
        raise NotImplementedError, node

    def visit_system_message(self, node):
        print >>sys.stderr, '%s: %s'%(node.attributes['type'], node[0][0].data)

    def depart_system_message(self, node):
        pass

    def visit_comment(self, node):
        pass

    def depart_comment(self, node):
        pass

    def visit_Text(self, node):
        self.w(cgi.escape(node.data))

    def depart_Text(self, node):
        pass

def makexml(filename, outfile=sys.stdout, debug=0):
    pub = docutils.core.Publisher()
    pub.set_reader('standalone', None, 'restructuredtext')
    pub.writer = Writer()
    pub.get_settings()
    pub.settings._destination = ''
    pub.source = docutils.io.StringInput(source=open(filename).read(),
        encoding='latin-1')
    pub.destination = docutils.io.StringOutput(encoding='latin-1')
    document = pub.reader.read(pub.source, pub.parser, pub.settings)
    pub.apply_transforms(document)

    if debug == 1:
        print >>outfile, document.pformat()
    else:
        print >>outfile, pub.writer.write(document, pub.destination)

def ns_open(*args):
    OPEN = '/usr/bin/open'
    return os.spawnl(os.P_WAIT, OPEN, OPEN, *args)

def main(filename='slides.rst'):
    try:
        os.makedirs('build')
    except:
        pass
    basefile = os.path.realpath(os.path.join('build', os.path.splitext(os.path.basename(filename))[0]))
    # sio = cStringIO.StringIO()
    sio = file(basefile+'.xml', 'w')
    makexml(filename, outfile=sio)
    # sio.seek(0)
    sio = file(basefile+'.xml', 'r')
    datafilename = basefile+'.pdf'
    pythonpoint.process(sio, datafilename=datafilename)
    ns_open(datafilename)
    
if __name__ == '__main__':
    main(*sys.argv[1:])
