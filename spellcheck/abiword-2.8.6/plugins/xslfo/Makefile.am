
SUBDIRS = xp

if XSLFO_BUILTIN
noinst_LTLIBRARIES = xslfo.la

else

plugindir = $(ABIWORD_PLUGINSDIR)
plugin_LTLIBRARIES = xslfo.la

endif

xslfo_la_LIBADD = \
	xp/libxp.la

xslfo_la_LDFLAGS = \
	$(XSLFO_LIBS) \
	-avoid-version \
	-module \
	-no-undefined

xslfo_la_SOURCES = 
nodist_EXTRA_xslfo_la_SOURCES = dummy.cpp

EXTRA_DIST = \
	plugin.m4

