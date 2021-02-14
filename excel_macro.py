# Copyright (c) 2021 CatPy
#
# Python stdlib imports
# package imports
import catpy as cty


def run_macro():
    cty.get_riser()

#
# This is for debugging purposes
#
if __name__ == '__main__':
    import os
    import xlwings as xw
    # Expects the Excel file next to this source file, adjust accordingly.
    file_name = 'CatPy_dbx.xlsm'
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), file_name))
    xw.Book(path).set_mock_caller()
    cty.get_riser()
