.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

=============================================
Change the precisions of some fields for GRAP
=============================================

Functionality
-------------

* Add a new precision 'GRAP Purchase Unit Price' of 4 digits, used in:
    * stock_move.unit_price;
    * account_invoice_line.price_unit;
    * purchase_order_line.price_unit;
    * product_template.standard_price;
    * product_template.standard_price_vat_included;

REALLY ?
* Add a new precision 'GRAP Purchase Unit Discount', used in:
    * account_invoice_line.discount;

* Use 'Product UoS' for
    * pos_order_line.qty field;


Credits
=======

Contributors
------------

* Sylvain LE GAL (https://twitter.com/legalsylvain);
* Julien WESTE;
