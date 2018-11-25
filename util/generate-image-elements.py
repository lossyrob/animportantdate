#!/bin/python

"""
Generates image elements from a directory and prints them to console.
Run from repo root.
"""

import os


IMAGE_DIR = 'animportantdate/static/images/shoot/'


if __name__ == '__main__':
    files = os.listdir(IMAGE_DIR)
    elements = []
    for f in files:
        if f.endswith('.jpg'):
            elements.append(
                """<p><img class="photoshoot" src="/static/images/shoot/{}"/></p>""".format(f)
            )

    for e in elements:
        print(e)
