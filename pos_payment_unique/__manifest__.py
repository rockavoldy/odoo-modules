{
    'name': "POS Payment Unique",

    'summary': """
        This module add functionality to restrict POS Payment to only have 1 payment methods selected.
        User can only choose 1 CASH, and 1 BANK if they want, but will restrict 2 CASH payment method.
        """,
    'description': """
        v1.0.0:
            * Don't allow to have 2 POS payment line with the same payment method
    """,
    'author': 'Akhmad Maulana Akbar',
    'website': 'https://akhmad.id',
    'category': 'Point of Sale',
    'version': '15.0.1.0.0',
    'depends': ['point_of_sale'],
    'assets': {
        'point_of_sale.assets': [
            'pos_payment_unique/static/src/js/*',
        ],
    }
}
