
# Target

TARGET = exec

# Directories

SRCDIR := src
INCDIR := src
OBJDIR := obj

# Extensions

SRCEXT := c
OBJEXT := o

# Files

SRCFILES := $(foreach D, $(SRCDIR), $(wildcard $(D)/*.$(SRCEXT)))
OBJFILES := $(patsubst %.$(SRCEXT), $(OBJDIR)/%.$(OBJEXT), $(SRCFILES))

# Compiler

CC := gcc

# Flags

CFLAGS 	:= -Wall -Wextra -pedantic
LDFLAGS := $(foreach $D, $(INCDIR), $(wildcard -I$(D)))
LDLIBS	:=

#
# Build Rules
#

.PHONY: all buildmsg build done

all: buildmsg build done

buildmsg:
	@echo "compiling..."

build: $(TARGET)

$(TARGET): $(OBJFILES)
	@mkdir -p '$(@D)'
	@$(CC) $(CFLAGS) -o $@ $^ $(LDLIBS)

$(OBJDIR)/%.$(OBJEXT): %.$(SRCEXT)
	@mkdir -p '$(@D)'
	@$(CC) $(CFLAGS) -c $< -o $@ $(LDFLAGS)


#
# Clean Rules
#

.PHONY: clean cleanmsg cleanfonts done

clean: cleanmsg cleanfonts done

cleanmsg:
	@echo "cleaning..."

cleanfonts:
	@rm -rf $(OBJDIR) $(TARGET)

done:
	@echo "done"

