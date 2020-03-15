#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
svgcenter.py

Copyright (c) 2013 Simon Kågedal Reimer

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

import argparse
import subprocess
import cairo
import gi
gi.require_version('Rsvg', '2.0')
gi.require_foreign("cairo")
from gi.repository import Rsvg

def query_svg(svgfile):
    """Parses the output from inkscape --query-all"""
    def parse_line(line):
        split = line.split(',')
        return [split[0]] + [float(x) for x in split[1:]]
    output = subprocess.check_output(["inkscape", "--query-all", svgfile])
    lines = output.decode("utf-8").split('\n')
    return [parse_line(line) for line in lines]

def get_bounding_box(svgfile):
    all = query_svg(svgfile)
    # The first line seems to always be the full drawing
    return all[0]

def clip(inputfile, outputfile):
    name, x, y, width, height = get_bounding_box(inputfile)

    bigger_size = max(width, height)
    width_diff = (bigger_size-width)/2
    height_diff = (bigger_size-height)/2

    handle = Rsvg.Handle()
    svg = handle.new_from_file(inputfile)
    surface = cairo.SVGSurface(outputfile, 
                               bigger_size, 
                               bigger_size)
    ctx = cairo.Context(surface)
    ctx.translate(-x + width_diff, -y + height_diff)
    svg.render_cairo(ctx)
    surface.finish()

def arg_parser():
    parser = argparse.ArgumentParser(description=
                                     'Center SVG.')
    parser.add_argument('input', 
                        help="SVG file to read")
    parser.add_argument('output',
                        help="SVG file to write")
    return parser

if __name__ == "__main__":
    args = arg_parser().parse_args()
    if args.output is None:
        print_info(args.input, args.output)
    else:
        clip(args.input, args.output)
