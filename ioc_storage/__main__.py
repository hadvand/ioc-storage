"""IOC storage's entry point script."""
# ioc_storage/__main__.py

from ioc_storage import cli, __app_name__


def main():
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
