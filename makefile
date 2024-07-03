CC = g++
CFLAGS = -g -Wall
SRC_DIR = src
TEST_DIR = test
LIB_DIR = include
OBJ_DIR = obj
BIN_DIR = bin

SRC = $(shell find $(SRC_DIR) -name '*.cpp')
TEST = $(shell find $(TEST_DIR) -name '*.cpp')
OBJ = $(SRC:$(SRC_DIR)/%.cpp=$(OBJ_DIR)/%.o)
TEST_OBJ = $(filter-out $(OBJ_DIR)/main.o, $(SRC:$(SRC_DIR)/%.cpp=$(OBJ_DIR)/%.o) $(TEST:$(TEST_DIR)/%.cpp=$(OBJ_DIR)/%.o))
COMPILE_OBJ = $(CC) $(CFLAGS) -c $< -o $@ -I $(LIB_DIR)

NAME = 👍-compiler
EXECUTABLE = $(BIN_DIR)/$(NAME)
TEST_EXECUTABLE = $(BIN_DIR)/$(NAME)_test

default: makedir main

makedir:
	mkdir -p $(BIN_DIR)
	mkdir -p $(OBJ_DIR)

main: $(OBJ)
	$(CC) $(CFLAGS) -o $(EXECUTABLE) $(OBJ)

test: $(TEST_OBJ)
	$(CC) $(CFLAGS) -o $(TEST_EXECUTABLE) $(TEST_OBJ)

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	mkdir -p $(@D)
	$(COMPILE_OBJ)

$(OBJ_DIR)/%.o: $(TEST_DIR)/%.cpp
	mkdir -p $(@D)
	$(COMPILE_OBJ)

clean:
	rm -rf $(OBJ_DIR)/* $(BIN_DIR)/*
