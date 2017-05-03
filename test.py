import execute as ex
import os

ex.execute(os.path.split(__file__)[0], 'grammar.tx', 'example.test', True, True)