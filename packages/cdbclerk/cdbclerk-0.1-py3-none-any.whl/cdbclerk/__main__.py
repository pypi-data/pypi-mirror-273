import asyncio
import sys
import argparse

from .store_fields import store_fields


def main():
    # Prepare the command line arguments
    parser = argparse.ArgumentParser(
        prog='cdbclerk',
        description='Save and restore IOC record fields to/from the APS component database',
    )
    parser.add_argument("command", choices=["store", "recall"], help="The operation to perform, either 'store' to save current settings to the database, or 'recall' to read field values from the database and apply to the IOC.")
    parser.add_argument("prefix", help="The PV prefix for the given record. E.g. '255idcVME:m1'")
    args = parser.parse_args()
    # Perform the requested operation
    if args.command == "store":
        runner = store_fields(prefix=args.prefix)
    asyncio.run(runner)


if __name__ == "__main__":
    sys.exit(main())
