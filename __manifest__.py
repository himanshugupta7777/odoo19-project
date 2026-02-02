{
    'name': 'Students',
    'version': '19.0.1.0.1',
    'category': 'sales',
    'author': 'Himanshu',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'security/security_groups.xml',
        'security/record_rules.xml',
        'views/views.xml',
        'views/templates.xml',
        'data/student.info.csv',
        'data/student_category.xml',
        'demo/demo_data.xml',
    ],
    'installable': True,
    'application': True,
}
