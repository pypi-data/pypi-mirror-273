import unittest
from rouskinhf import list_datapoints, util
class TestDataDump(unittest.TestCase):
    def test(self):
        listdata = list_datapoints.ListofDatapoints(
            [list_datapoints.Datapoint(sequence='ACACAUCUG', reference='1', dotbracket='.........'),
            list_datapoints.Datapoint(sequence='ACACAUCUU', reference='2', dotbracket='(.......)')]
        )
        listdata.datapoints = list_datapoints.ListofDatapoints(verbose=False).from_pandas(listdata.to_pandas())

        util.dump_json(
            listdata.to_dict(),
            "test.json"
        )