"""
Compilador.
"""

import sys
from sys import argv

from lexical_analyzer import LexicalAnalyzer
from sdt_processor import SDTProcessor
from return_status import LexicalReturnStatus, ReturnStatus

def main() -> None:
    if len(argv) < 2:
        print('Usage: lexical_test "source_file.txt"')
        sys.exit()

    try:
        with open(argv[1], 'r', encoding='utf-8') as source_file:
            source = source_file.read()
    except IOError:
        sys.exit()

    return_code, pos, tokens, symbol_table = LexicalAnalyzer.analyze(source)

    status = ReturnStatus(return_code, None, pos)

    if status.has_errors():
        print(status.get_message())
        return

    print('Token list contents: ')

    for token in tokens:
        print(f'{token} ', end='')

    print('\n\n')
    print(symbol_table)

    return_code, token = SDTProcessor.process(tokens, symbol_table)
    print('\n')

    status = ReturnStatus(return_code, token)

    print(status.get_message())
    if status.has_errors():
        return

if __name__ == "__main__":
    main()
