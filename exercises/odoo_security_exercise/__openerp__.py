{
    'name': 'Odoo security exercise',
    'version': '0.1',
    'category': 'Uncategorized',
    'description': """
        Exercise that attempts to demonstrate how the Odoo security elements
        work.
    """,
    'author': 'Jorge Soto Garcia',
    'website': 'http://www.github.com/sotogarcia',
    'license': 'AGPL-3',

    'depends': [
        'odoo_inheritance_exercise'
    ],

    'data': [
        'data/ir_module_category.xml',

        'demo/exercise_extended_model.xml',

        'security/res_groups.xml',
        'security/ir_model_access.xml',
        'security/ir_rule.xml',

        'views/menu_odoo_inheritance_exercise.xml',
        'views/exercise_extended_model.xml',
        'views/exercise_delegated_model.xml',
        'views/exercise_inherited_model.xml'
    ],

    'demo': [],

    'installable': True,
    'application': False,
    'auto_install': False,
}
