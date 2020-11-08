TEMPLATES:=$(shell find -name "*.tmpl")
PYFILES=$(TEMPLATES:.tmpl=.py)

all: $(TEMPLATES) $(PYFILES)

%.py: %.tmpl
	cheetah compile --nobackup $<
