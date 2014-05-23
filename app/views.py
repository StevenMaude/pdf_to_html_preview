#!/usr/bin/env python
# encoding: utf-8
from app import app

from flask import render_template, request
import requests
import pdf_to_html


@app.route('/')
def index():
    url = request.args.get('url')
    if url:
        try:
            pages_data, fontspecs, pdf_info = pdf_to_html.main(url)
        except requests.exceptions.RequestException:
            return render_template('error_template.html',
                                   url=url)
        return render_template('output_template.html',
                               pages_data=pages_data,
                               fontspecs=fontspecs,
                               pdf_info=pdf_info)
    else:
        return render_template('start_template.html')
