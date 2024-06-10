

lexical_test:
	g++ -I include test/lexical_test.cpp src/lexical_analyzer.cpp src/data/token_list.cpp src/data/symbol_table.cpp -o lexical_test