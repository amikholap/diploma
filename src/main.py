#!/usr/bin/env python
import threading

import wx

from gui import App
from scanner import Scanner


def main():
    app = App(scanner=Scanner())
    app.MainLoop()


if __name__ == '__main__':
    main()
