# PDF to HTML Preview
Helps you scrape PDFs with scraperwiki.pdftoxml() by giving you a HTML
preview that shows where content is located on the page. It highlights
text in the same column or row if you click on text in the displayed
page layouts.

## This is mostly not my code. [Mostly.](http://www.youtube.com/watch?v=wKdocYeSqTA)

I've grabbed it from a copy on [ScraperWiki Classic](https://classic.scraperwiki.com/editor/raw/pdf-to-html-preview-1)
and threw it onto GitHub.

That was the case when I first made this repo. Since then, I tidied up
the code slightly, pulled out the JS into a separate file, used Jinja
templates to generate the HTML, and made it both a command line utility
and Flask app. Whew!

I've also used it to [scrape a PDF](http://stackoverflow.com/a/23835697/1678416).
It's useful!

[Info link](https://blog.scraperwiki.com/2010/12/scraping-pdfs-now-26-less-unpleasant-with-scraperwiki/)

Original code at this commit:
[f4ed75b005efd5c8716e6784634d740571ad774c](https://github.com/StevenMaude/pdf_to_html_preview/blob/f4ed75b005efd5c8716e6784634d740571ad774c/pdf_to_html.py)

Since ScraperWiki Classic was deprecated, this tool was no longer
available.

I never used this when it was on the site, but it seems to mostly work
locally. [Mostly.](http://www.youtube.com/watch?v=wKdocYeSqTA) 

## Licence?

I'm hoping the original author, Julian Todd, doesn't mind me doing this.
There was no obvious licence attached to the [original code](https://classic.scraperwiki.com/views/pdf-to-html-preview-1/).

I'm assuming it's in the public domain.

## Install

On Linux, it may well just work if you install requirements using
`pip install -r requirements.txt`

There may be other dependencies that you need to search how to fix.
`lxml` can be a stumbling block.

If you get stuck, post errors or fixes as issues and I'll try to figure
them out and update.

On Windows, it's more problematic. Install guide with version based on the
initial fixed commits is [here](https://gist.github.com/StevenMaude/88def892b0cbfa8ae818).

## Usage
### Command line
Run as:

    pdf_to_html.py http://link.to.pdf

It will create a HTML file: `output.html`. View it in a browser. The
**download button in this HTML doesn't work**; you can't use the
generated page to then download another PDF.

Instead, run the script again with new input PDF and new output
filename.

### Flask
Run local_run.py - this is fine for local use only.

Visit http://127.0.0.1:5000 in your browser. The download form works
here.

**Do not use Flask's debug server in production.**
