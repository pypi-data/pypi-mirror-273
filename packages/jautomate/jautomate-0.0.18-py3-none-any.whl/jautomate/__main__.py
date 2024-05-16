#!/usr/bin/env python
"""Jautomate entry point script."""


from jautomate import cli, __app_name__


def main():
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
