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
        # Module needed data files
        'data/at_level_data.xml',

        # Module general settings
        'views/academy_tests.xml',

        # Module model views
        'views/at_question_view.xml',
        'views/at_tag_view.xml',
        'views/at_test_view.xml',
        'views/at_topic_view.xml',
        'views/at_category_view.xml',
        'views/at_answer_view.xml',
        'views/at_level_view.xml',

        # Overriden external model views
        'views/ir_attachment_view.xml',

        # Model security files
        'security/at_answer.xml',
        'security/at_category.xml',
        'security/at_level.xml',
        'security/at_question.xml',
        'security/at_tag.xml',
        'security/at_test.xml',
        'security/at_topic.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
    'js': [
        'static/src/js/academy_tests.js'
    ],
    'css': [
        'static/src/css/styles-backend.css'
    ],
}

