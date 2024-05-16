import asyncio

from caproto.asyncio.client import Context

from typing import Sequence

async def read_record(prefix: str, fields: Sequence, ctx: Context = None) -> dict:
    """Read the PV values for a given record.

    Parameters
    ==========
    prefix
      The PV prefix for the record. E.g. ``"255idcVME:m1"``
    fields
      A sequence of the fields to read values for. E.g. ``[".VELO",
      ".S"]``
    ctx
      A caproto asyncio client context to use. If ``None`` a new
      context will be created.
    
    Returns
    =======
    result
      A dictionary where the entries in *fields* are the keys, which
      map to the corresponding PV values.

    """
    # Create a caproto context if needed
    if ctx is None:
        ctx = Context()
    # Create the PVs to read
    pvs = [f"{prefix}{field}" for field in fields]
    pvs = await ctx.get_pvs(*pvs)
    # Read the PVs
    values = await asyncio.gather(*[pv.read() for pv in pvs])
    values = [res.data[0] for res in values]
    result = {field: val for field, val in zip(fields, values)}
    return result
