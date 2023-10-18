# -*- coding: utf-8 -*-
{
    'name': 'Import Payments',
    'version': '1.0',
    'author': 'SIMI Technologies',
    'website': 'https://simitechnologies.co.ke',
    'category': 'Tools',
    'summary': 'Import payments data from CSV files',
    'depends': ['base', 'account_payment', ],
    'data': [
        'security/ir.model.access.csv',
        'views/payment_import_view.xml',
        'wizard/payment_import_wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
    'app': True
}

