#!/usr/bin/python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from os.path import splitext, basename
from lib import *

parser = ArgumentParser(
    description='Generate JLCPCB bom and cpl files from a Kicad PCB project')
parser.add_argument('project', type=str, help='Kicad PCB board file')
parser.add_argument('-u', '--update', action='store_true',
                    help='Update JLCPCB component database')
parser.add_argument('-o', '--offline', action='store_true',
                    help='Use offline database')
parser.add_argument('-m', '--match', action='store_true',
                    help='Only use LCSC attribute')
parser.add_argument('-n', '--nostock', action='store_true',
                    help='Select part even if no stock')
parser.add_argument('-i', '--ignore', type=str,
                    help='Ignored parts (regex)')

if __name__ == '__main__':

    args = parser.parse_args()
    db = None

    if args.update:
        jlc.update_db()

    if args.offline:
        db = jlc.load_db()

    base_name = splitext(basename(args.project))[0]

    for layer in ('top', 'bottom'):
        print('**', layer, 'layer **')
        components = kicad.get_components(args.project, layer, args.ignore)
        parts = jlc.search(components, database=db, nostock=args.nostock, match=args.match)
        
        jlc.make_bom(parts, '{0}-{1}-bom.xlsx'.format(base_name, layer))
        jlc.make_cpl(parts, '{0}-{1}-cpl.xlsx'.format(base_name, layer))
