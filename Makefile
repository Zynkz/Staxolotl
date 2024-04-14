#Made with chatgpt3.5
# Need to test if
# export LD_LIBRARY_PATH=/home/zynkz/repositories/space/C/lib:$LD_LIBRARY_PATH
# is still needed.

CC = gcc
CFLAGS = -Wall -Wextra -pedantic -std=c11 -I./include
LDFLAGS = -L./lib
LIBS = -lcfitsio -lm -lnsl
LIBRARY_PATH = /mnt/c/Users/Zynkz/Desktop/repositories/staxalotl/lib

SRCS = staxolotl.c
OBJS = $(SRCS:.c=.o)
EXEC = staxolotl

all: $(EXEC)

$(EXEC): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(EXEC) $(LDFLAGS) $(LIBS) -Wl,-rpath=$(LIBRARY_PATH)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	$(RM) $(EXEC) $(OBJS)
