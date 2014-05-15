# PDF to HTML Preview

## This is mostly not my code. [Mostly.](http://www.youtube.com/watch?v=wKdocYeSqTA)

I've grabbed it from a copy on [ScraperWiki Classic](https://classic.scraperwiki.com/editor/raw/pdf-to-html-preview-1)
and threw it onto GitHub with very small changes.

[Info link](https://blog.scraperwiki.com/2010/12/scraping-pdfs-now-26-less-unpleasant-with-scraperwiki/)

Original code at this commit: f4ed75b005efd5c8716e6784634d740571ad774c

Since ScraperWiki Classic was deprecated, this tool was no longer
available.

I never used this when it was on the site, but it seems to mostly work
locally. [Mostly.](http://www.youtube.com/watch?v=wKdocYeSqTA) 

## Licence?

I'm hoping the original author, Julian Todd, doesn't mind me doing this.
There was no obvious licence attached to the [original code](https://classic.scraperwiki.com/views/pdf-to-html-preview-1/).

I'm assuming it's in the public domain.

## Install

Install requirements using `pip install -r requirements.txt`

## Usage
Since this isn't running on ScraperWiki's site, the usage is a little
unconventional. (Comment on the issues if you find this useful and want to
remind me to try to fix this.)

    pdf_to_html.py http://link.to.pdf > some_output.html

Then open `some_output.html` in a browser. The **download button in
this HTML doesn't work**; you can't use the generated page to then
download another PDF.

Instead, run the script again with new input PDF and new output
filename.
