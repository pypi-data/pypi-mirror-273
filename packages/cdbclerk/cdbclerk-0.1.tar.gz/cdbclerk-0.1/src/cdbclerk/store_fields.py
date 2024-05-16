from .ioc_io import read_record

async def store_fields(prefix: str):
    fields = ['.VELO', '.S']
    values = await read_record(prefix=prefix, fields=fields)
    # Send the PV field values to the database
    # For now just print them to the command line
    max_len = max([len(s) for s in values.keys()])
    for field, value in values.items():
        lside = f"\"{field:}\":".ljust(max_len+4)
        print(f"{lside}{value}")
