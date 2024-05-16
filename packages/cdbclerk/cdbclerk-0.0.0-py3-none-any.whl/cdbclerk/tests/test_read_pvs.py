from unittest import mock
import pytest

from cdbclerk.ioc_io import read_record

@pytest.mark.asyncio
async def test_record():
    ctx = mock.AsyncMock()
    ctx.get_pvs.side_effect = lambda pvs: [mock.AsyncMock() for pv in pvs]
    # Run the function under test
    fields = [".VELO"]
    result = await read_record(prefix="255idcVME:m1", fields=fields, ctx=ctx)
    # Check that the right data was stored in the results dictionary
    assert ".VELO" in result.keys()
