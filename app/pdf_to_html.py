#forked from: Julian_Todd / PDF to HTML
#(https://scraperwiki.com/views/pdf-to-html-preview-1/)
from __future__ import unicode_literals

import codecs
import sys
import scraperwiki
import requests
import requests_cache
import lxml.etree
import lxml.html
import re

from jinja2 import Environment, PackageLoader


def render_template(pages_data, fontspecs, pdf_info):
    """ Render template and print it. """
    env = Environment(loader=PackageLoader('pdf_to_html', 'templates'))
    template = env.get_template('output_template.html')
    return template.render(pages_data=pages_data,
                           fontspecs=fontspecs,
                           pdf_info=pdf_info)


def pageblock(page):
    '''
    Print a page of the PDF, outputting the contents as HTML.
    '''
    page_data = {}
    assert page.tag == 'page'
    page_height = int(page.attrib.get('height'))
    page_width = int(page.attrib.get('width'))
    page_number = page.attrib.get('number')
    assert page.attrib.get('position') == "absolute"

    page_data = {'page_height': page_height, 'page_width': page_width,
                 'page_number': page_number}

    v_list = []
    for v in page:
        if v.tag == 'fontspec':
            continue
        assert v.tag == 'text'
        text = re.match('(?s)<text.*?>(.*?)</text>',
                        lxml.etree.tostring(v)).group(1)
        top = int(v.attrib.get('top'))
        left = int(v.attrib.get('left'))
        width = int(v.attrib.get('width'))
        height = int(v.attrib.get('height'))
        fontid = v.attrib.get('font')
        # TODO: Move this style into template, no need for it here.
        style = ('top:%dpx; left:%dpx; height:%dpx; width:%dpx'
                 % (top, left, height, width))
        v_list.append({'top': top, 'left': left, 'height': height,
                       'width': width, 'fontid': fontid, 'style': style,
                       'text': text})
    page_data['v'] = v_list
    return page_data


def main(pdfurl, hidden=-1, cmdline=False):
    '''
    Take the URL of a PDF, and use scraperwiki.pdftoxml and lxml to output the
    contents as a styled HTML div.
    '''
    requests_cache.install_cache()
    pdfdata = requests.get(pdfurl).content

    options = ''
    if hidden == 1:
        options = '-hidden'
    # TODO: readd this if implemented in scraperwiki-python
    # see https://github.com/scraperwiki/scraperwiki-python/issues/48
    # pdfxml = scraperwiki.pdftoxml(pdfdata, options)
    pdfxml = scraperwiki.pdftoxml(pdfdata).decode('utf-8')
    try:
        root = lxml.etree.fromstring(pdfxml.encode('utf-8'))
    except lxml.etree.XMLSyntaxError, e:
        print str(e), str(type(e)).replace("<", "&lt;")
        print pdfurl
        print pdfxml.replace("<", "&lt;")
        root = []

    fontspecs = {}
    # Get the PDF's internal styles: we'll use these to
    # style the divs containing the PDF.
    for fontspec in (root is not None and root.xpath('page/fontspec')):
        id = fontspec.attrib.get('id')
        fontdesc = {'size': int(fontspec.attrib.get('size')),
                    'family': fontspec.attrib.get('family'),
                    'color': fontspec.attrib.get('color')}
        fontspecs[id] = fontdesc

    # Code from old template:
    # Removed hidden option for now
    #if hidden == 1:
    #    checked = "checked "
    #else:
    #    checked = ""
    #print '<br /><label for="hidden">Force hidden text extraction</label>'
    #print ('    <input type="checkbox" name="hidden" id="hidden"'
    #       'value="1" %stitle="force hidden text extraction">' % checked)
    ttx = re.sub('<', '&lt;', pdfxml)
    ttx = re.sub('\n', '\r\n', ttx)
    # Does this truncate in case of large PDF?
    pdf_info = {'pdfurl': pdfurl, 'ttx': ttx[:5000], 'total_pages': len(root)}
    all_pages_data = [pageblock(page) for page in root]

    if cmdline:
        with codecs.open('output.html', 'w', encoding='utf8') as f:
            f.write(render_template(all_pages_data, fontspecs, pdf_info))
    else:
        return all_pages_data, fontspecs, pdf_info


if __name__ == '__main__':
    try:
        pdfurl = sys.argv[1]
    except IndexError:
        print "Enter a valid URL. For example:"
        print ("http://soswy.state.wy.us/Elections/Docs/2004/04Results"
               "/04General/AL_PbP_Candidate_Summary.pdf")
        sys.exit(1)
    hidden = -1
    main(pdfurl, hidden, cmdline=True)
