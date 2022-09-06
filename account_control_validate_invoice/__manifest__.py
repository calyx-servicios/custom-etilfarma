# pylint: disable=missing-module-docstring,pointless-statement
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    ##################################
    # Account Control Validate Invoice
    ##################################
    "name": "Account Control Validate Invoice",
    "summary": """
        Summary of the module's purpose
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["<Github Username/s>"],
    "website": "https://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Technical Settings",
    "version": "11.0.1.0.0",
    # see https://odoo-community.org/page/development-status
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    # any module necessary for this one to work correctly
    "depends": ["stock"],
    ### XML Data files
    'data': [
         'views/product_logistics_form_view.xml',],
    ### XML Demo files
    # only loaded in demo mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    ###########################
    # Delete all the commented lines after editing the module
    ###########################
}
