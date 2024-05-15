##########################################################################################
# textkernel/tests/__init__.py
##########################################################################################

import unittest

from tests.test_name_grammar  import *
from tests.test_value_grammar import *
from tests.test_from_text     import *
from tests.test_from_file     import *

##########################################################################################
# Perform unit testing if executed from the command line
##########################################################################################

if __name__ == '__main__':
    unittest.main()

##########################################################################################
