#pragma once

enum LexicalReturnCode {
    LEX_OK,
    INVALID_CHAR,
    INVALID_NUMBER_FORMAT,
    UNCLOSED_STRING
};