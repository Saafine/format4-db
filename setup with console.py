#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(console=["main.py"],
	options = {
		"py2exe": {
			"packages": ["fdb"],
			"compressed": True,
		}
	},
	zipfile = None,
)