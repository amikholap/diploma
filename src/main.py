#!/usr/bin/env python3
import sys

from diploma.gui import App


def main():
    app = App(sys.argv)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
