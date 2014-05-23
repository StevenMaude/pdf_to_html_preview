#!/usr/bin/env python
# encoding: utf-8
from app import app

from flask import render_template, request
import pdf_to_html


@app.route('/')
def index():
    url = request.args.get('url')
    if url:
        pages_data, fontspecs, pdf_info = pdf_to_html.main(url)
        return render_template('output_template.html',
                               pages_data=pages_data,
                               fontspecs=fontspecs,
                               pdf_info=pdf_info)
    else:
        return render_template('start_template.html')
