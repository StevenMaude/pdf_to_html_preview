#forked from: Julian_Todd / PDF to HTML
#(https://scraperwiki.com/views/pdf-to-html-preview-1/)
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
    template = env.get_template('pageblock_template.html')
    return template.render(pages_data=pages_data,
                           fontspecs=fontspecs,
                           pdf_info=pdf_info)


def pageblock(page):
    '''
    Print a page of the PDF, outputting the contents as HTML.
    '''
    page_data = {}
    result = []
    assert page.tag == 'page'
    page_height = int(page.attrib.get('height'))
    page_width = int(page.attrib.get('width'))
    page_number = page.attrib.get('number')
    assert page.attrib.get('position') == "absolute"

    page_data = {'page_height': page_height, 'page_width': page_width,
                 'page_number': page_number}

    result.append('<p>Page %s height=%d width=%d</p>'
                  % (page_number, page_height, page_width))
    result.append('<div class="page" style="height:%dpx; width:%dpx">'
                  % (page_height, page_width))
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
        style = ('top:%dpx; left:%dpx; height:%dpx; width:%dpx'
                 % (top, left, height, width))
        result.append('    <div class="text fontspec-%s" style="%s">%s</div>'
                      % (fontid, style, text))
        v_list.append({'top': top, 'left': left, 'height': height,
                       'width': width, 'fontid': fontid, 'style': style,
                       'text': text})
    result.append('</div>')
    page_data['v'] = v_list
    return '\n'.join(result), page_data


def main(pdfurl, hidden):
    '''
    Take the URL of a PDF, and use scraperwiki.pdftoxml and lxml to output the
    contents as a styled HTML div.
    '''
    requests_cache.install_cache()
    pdfdata = requests.get(pdfurl).content
    #pdfdata = urllib2.urlopen(pdfurl).read()
    options = ''
    if hidden == 1:
        options = '-hidden'
    # TODO: readd this if implemented in scraperwiki-python
    # see https://github.com/scraperwiki/scraperwiki-python/issues/48
    # pdfxml = scraperwiki.pdftoxml(pdfdata, options)
    pdfxml = scraperwiki.pdftoxml(pdfdata)
    try:
        root = lxml.etree.fromstring(pdfxml)
    except lxml.etree.XMLSyntaxError, e:
        print str(e), str(type(e)).replace("<", "&lt;")
        print pdfurl
        print pdfxml.replace("<", "&lt;")
        root = []
    global styles
    fontspecs = {}

    # Get the PDF's internal styles: we'll use these to
    # style the divs containing the PDF.
    for fontspec in (root is not None and root.xpath('page/fontspec')):
        id = fontspec.attrib.get('id')
        fontdesc = {'size': int(fontspec.attrib.get('size')),
                    'family': fontspec.attrib.get('family'),
                    'color': fontspec.attrib.get('color')}
        fontspecs[id] = fontdesc
        styles['div.fontspec-%s' % id] = \
            ('color:%s;font-family:%s;font-size:%dpx'
             % (fontdesc['color'], fontdesc['family'], fontdesc['size']))

    # Output the view, with instructions for the user.
    print '<html dir="ltr" lang="en">'
    print '<head>'
    print ('    <meta http-equiv="Content-Type" content="text/html; '
           'charset=utf-8"/>')
    print '    <title>PDF to XML text positioning</title>'
    print ('    <style type="text/css" media="screen">%s</style>'
           % "\n".join(["%s { %s }" % (k, v) for k, v in styles.items()]))
    print ('    <script type="text/javascript" '
           'src="https://ajax.googleapis.com/ajax/libs/jquery/1.4.2'
           '/jquery.min.js"></script>')
    print ('    <script type="text/javascript" '
           'src="static/pdf_click_view.js"></script>')
    print '</head>'

    print '<div class="info" id="info1">&lt;text block&gt;</div>'
    print '<div class="info" id="info2">&lt;position&gt;</div>'

    print '<div class="heading">'
    print '<h2>Graphical preview of scraperwiki.pdftoxml(pdfdata)</h2>'

    print ('<p>Click on a text line to see its coordinates and any other'
           'text that shares the same column or row.')
    print ('   Useful for discovering what coordinates to use when extracting '
           'rows from tables in a document.</p>')

    print '<p class="href"><a href="%s">%s</a></p>' % (pdfurl, pdfurl)
    print '<form id="newpdfdoclink">'
    print '<label for="url">PDF link</label>'
    print ('    <input type="text" name="url" id="url" value="%s" '
           'title="paste in url of document">' % pdfurl)
    if hidden == 1:
        checked = "checked "
    else:
        checked = ""
    print '<br /><label for="hidden">Force hidden text extraction</label>'
    print ('    <input type="checkbox" name="hidden" id="hidden"'
           'value="1" %stitle="force hidden text extraction">' % checked)
    print '<br />    <input type="submit" value="Go">'
    print '</form>'
    ttx = re.sub('<', '&lt;', pdfxml)
    ttx = re.sub('\n', '\r\n', ttx)
    # Does this truncate in case of large PDF?
    print '<textarea class="pdfprev">%s</textarea>' % ttx[:5000]
    print '</div>'

    print '<p>There are %d pages</p>' % len(root)

    pdf_info = {'pdfurl': pdfurl, 'ttx': ttx[:5000], 'total_pages': len(root)}
    # Print each page of the PDF.
    all_pages_data = []
    for page in root:
        printed_output, page_data = pageblock(page)
        print printed_output
        all_pages_data.append(page_data)

    with open('templated.html', 'w') as f:
        f.write(render_template(all_pages_data, fontspecs, pdf_info))


# Global styles for the divs containing the PDF.
styles = {
    "div#info1": ("position:fixed; white-space:pre; background-color:#ffd; "
                  "border: thin red solid; z-index: 50; top:0px;"),
    "div#info2": ("position:fixed; white-space:pre; background-color:#ffd; "
                  "border: thin red solid; z-index: 50; top:20px;"),
    "div.heading": "padding-left:150px;",
    "p.href": "font-size:60%",
    "div.page": ("background-color:#fff; border:thin black solid; "
                 "position:relative; margin:2em;"),
    "div.text": "position:absolute; white-space:pre; background-color:#eee;",
    "textarea.pdfprev":
    "white-space:pre; height:150px; width:80%",
    "div.text:hover": "background-color:#faa; cursor:pointer",
    "div.linev": "background-color:#fcc;",
    "div.lineh": "background-color:#fce;",
}

# Check for a PDF URL and hidden-checkbox entered by the user:
# if none, use our default values:
# urlquery = os.getenv('URLQUERY')

#if urlquery:
#     querydata = urlparse.parse_qsl(urlquery);
#     for pair in querydata:
#        if pair[0] == "url":
#            pdfurl = urllib.unquote(pair[1])
#        if pair[0] == "hidden":
#            hidden = 1
if __name__ == '__main__':
    try:
        pdfurl = sys.argv[1]
    except IndexError:
        print "Enter a valid URL. For example:"
        print ("http://soswy.state.wy.us/Elections/Docs/2004/04Results"
               "/04General/AL_PbP_Candidate_Summary.pdf")
        sys.exit(1)
    hidden = -1
    main(pdfurl, hidden)
