{
    'name': 'Odoo inheritance exercise',
    'version': '0.1',
    'category': 'Uncategorized',
    'description': """
        Exercise that attempts to demonstrate how the Odoo inheritance elements
        work.
    """,
    'author': 'Jorge Soto Garcia',
    'website': 'http://www.github.com/sotogarcia',
    'license': 'AGPL-3',

    'depends': [
        'base',
        'mail'
    ],

    'data': [
        'demo/exercise_extended_model.xml',
        'demo/exercise_inherited_model.xml',
        'demo/exercise_delegated_model.xml',

        'security/ir_model_access.xml',

        'views/menu_odoo_inheritance_exercise.xml',
        'views/exercise_base_model.xml',
        'views/exercise_extended_model.xml',
        'views/exercise_inherited_model.xml',
        'views/exercise_delegated_model.xml'
    ],

    'demo': [],

    'installable': True,
    'application': False,
    'auto_install': False,
}
