# Makefile for source rpm: gnome-terminal
# $Id$
NAME := gnome-terminal
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
