# -*- coding: utf-8 -*-
{
    'name': "Academy Tests",

    'summary': """
        Store and manage questions to build random academy tests""",

    'description': """
        If you have thousands of questions about the same topic, you can
        mix them many often to build hundreds of tests.
    """,

    'author': "Jorge Soto Garcia",
    'website': "https://github.com/sotogarcia",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'mail'
    ],

    # always loaded
    'data': [
        'data/at_level_data.xml',

        'views/academy_tests.xml',

        'views/at_question_view.xml',
        'views/at_tag_view.xml',
        'views/at_test_view.xml',
        'views/at_topic_view.xml',
        'views/at_category_view.xml',
        'views/at_answer_view.xml',
        'views/at_level_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/at_topic_demo.xml',
        'demo/at_category_demo.xml',
        'demo/at_tag_demo.xml',
        'demo/at_question_demo.xml',
        'demo/at_answer_demo.xml'
    ],
    'js': [
        'static/src/js/academy_tests.js'
    ],
    'css': [
        'static/src/css/styles-backend.css'
    ],
}
