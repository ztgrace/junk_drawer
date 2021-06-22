#!/usr/bin/env python

from secrets import choice
import argparse
import string

parser = argparse.ArgumentParser(description='Generate a secure password')
parser.add_argument('--all', '-a', action='store_true', default=True,
                    help="All printable ascii characters")
parser.add_argument('--length', '-n', type=int, default=10,
                    help='Length of password')
parser.add_argument('--letters', '-l', action='store_true',
                    help='Upper and lower case letters')
parser.add_argument('--digits', '-d', action='store_true', help='Digits')
parser.add_argument('--quiet', '-q', action='store_true',
                    help='Supress extraneous output')
parser.add_argument('--special', '-s', action='store_true',
                    help='Special (punctuation) characters')

args = parser.parse_args()

chars = ""
if args.all and not (args.letters or args.digits or args.special):
    chars = string.ascii_letters + string.digits + string.punctuation

if args.letters:
    chars += string.ascii_letters

if args.digits:
    chars += string.digits

if args.special:
    chars += string.digits


if not args.quiet:
    print(f"length: {args.length}")
    print(f"keyspace: {chars}")
    print('*' * args.length)

print(''.join(choice(chars) for i in range(args.length)))
