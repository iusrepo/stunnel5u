# Makefile for source rpm: stunnel
# $Id$
NAME := stunnel
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
