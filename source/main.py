"""
Compilador.
"""

import sys
from sys import argv

from lexical_analyzer import LexicalAnalyzer

if len(argv) < 2:
    print('Usage: lexical_test "source_file.txt"')
    sys.exit()

try:
    with open(argv[1], 'r', encoding='utf-8') as source_file:
        source = source_file.read()
except IOError:
    sys.exit()

return_code, char, tokens, symbol_table = LexicalAnalyzer.analyze(source)

print(f'Status: {return_code}, {char}')
print('Token list contents: ')

while len(tokens) > 0:
    token = tokens.pop(0)
    print(f'{token} ', end='')

print('\n\n')
print(symbol_table)
