import unittest


class TestImport(unittest.TestCase):
    def test_import(self):
        from src import GridIO, FlowIO

        grd = GridIO(filename='../data/plate_data/plate.sp.x')
        flw = FlowIO('../data/plate_data/sol-0000010.q')

        import src

        grd = src.io.GridIO(filename='../data/plate_data/plate.sp.x')
        flw = src.io.FlowIO('../data/plate_data/sol-0000010.q')


if __name__ == '__main__':
    unittest.main()
