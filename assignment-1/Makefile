# Compiler and flags
CC = g++
FLAGS = -g -Wall
OBJS = main.o merge_join.o set_operators.o groupby_aggregate.o

# Detect the operating system
ifeq ($(OS),Windows_NT)
    RM = del /F /Q
else
    RM = rm -f
endif

# Targets
all: main

main: $(OBJS)
	$(CC) $(FLAGS) -o $@ $^

%.o: %.cc %.h
	$(CC) $(FLAGS) -c $<

clean:
	@echo "Cleaning up..."
	$(RM) main.exe $(OBJS)

.PHONY: clean
