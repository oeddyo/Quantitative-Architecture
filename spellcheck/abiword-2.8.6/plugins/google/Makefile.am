
SUBDIRS = xp

if GOOGLE_BUILTIN
noinst_LTLIBRARIES = google.la

else

plugindir = $(ABIWORD_PLUGINSDIR)
plugin_LTLIBRARIES = google.la

endif

google_la_LIBADD = \
	xp/libxp.la

google_la_LDFLAGS = \
	$(GOOGLE_LIBS) \
	-avoid-version \
	-module \
	-no-undefined

google_la_SOURCES = 
nodist_EXTRA_google_la_SOURCES = dummy.cpp

EXTRA_DIST = \
	plugin.m4

