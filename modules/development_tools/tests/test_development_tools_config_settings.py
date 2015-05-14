# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################


from openerp.tests.common import TransactionCase
from logging import getLogger


_logger = getLogger(__name__)


class DevelopmentToolsConfigSettings(TransactionCase):
    """ This class contains the unit tests for 'development_tools.config.settings'.

        Tests:
          - all_implied: Checks all relationships between groups
    """

    _model_name = 'development_tools.config.settings'

    def setUp(self):
        super(DevelopmentToolsConfigSettings, self).setUp()

    def test__iterable(self):
        """ Checks if the _iterable works properly
        """

        model_obj = self.env[self._model_name]

        _logger.warning('test_iterable')
        items = self._values + self._types
        for item in items:
            result = model_obj._iterable(item)
            self.assertTrue(
                hasattr(result, '__iter__') and len(result) > 0,
                u'_iterable({}) is not iterable'.format(item)
            )

    def test__safe_eval(self):
        """ Checks if the _safe_eval works properly
        """

        model_obj = self.env[self._model_name]

        for item in self._to_eval:
            string = unicode(item)
            result = model_obj._safe_eval(string, type(item))
            self.assertEqual(
                item,
                result,
                'Fail on _safe_eval {}'.format(item)
            )

    # ----------------------------- NEDDED DATA -------------------------------

    _types = [
        int,
        float,
        complex,
        str,
        unicode,
        list,
        tuple,
        bytearray,
        buffer,
        xrange,
        set,
        frozenset,
        dict,
        type,
        bool
    ]

    _values = [
        -1, 0, 1,
        -1.1, 0.0, 1.1,
        'texto',
        u'text',
        [], [None], [1, 'a', None, False],
        (), (None,), (1, 'a', None, False,),
        set((1, 'a', None, False)),
        frozenset((1, 'a', None, False)),
        {}, {'key': 'value'}, {'key': None},
        True, False,
        None
    ]

    _to_eval = [
        True,
        False,
        1,
        0,
        1.0,
        None,
        [],
        [1.0, 'text', True],
        {},
        {'number': 1.0, 'text': 'text', 'bool': True},
        [('a', '=', 'b')]
    ]
