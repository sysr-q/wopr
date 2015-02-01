#!/usr/bin/env python2
from __future__ import print_function
import curses
import locale
import time

locale.setlocale(locale.LC_ALL, "")
code = locale.getpreferredencoding()


def main_loop(cls, *args, **kwargs):
	def inner(stdscr):
		# y, x = stdscr.getmaxyx()
		curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
		curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
		curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
		curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)

		kwargs.setdefault("enc", code)
		w = cls(stdscr, *args, **kwargs)

		while True:
			c = stdscr.getch(0, 0)
			w.paint()

			if c == ord('q'):
				break
			elif c == curses.KEY_RESIZE:
				# y, x = stdscr.getmaxyx()
				pass

			time.sleep(30000/1e6)
	curses.wrapper(inner)
