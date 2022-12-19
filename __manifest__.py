{
    'name': 'Employee Transfer',
    'version': '15.0.1.0.0',
    'sequence': 100,
    'depends': ['base',
                'mail',
                'hr',
                ],
    'data': [
            'data/sequence.xml',
            'security/ir.model.access.csv',
            'view/transfer_view.xml',
            'security/security.xml',
                ],
    'license': 'LGPL-3',
}