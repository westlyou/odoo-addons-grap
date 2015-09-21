.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

=================================
Change some default data for GRAP
=================================

Product Datas
-------------
Disable some unwished data by xml_id;
* Disable product.product_category_1;

Accouting Datas
---------------
Change French Account Chart Template:
* Disable 4011, 4017; make 401 a 'normal' account;
* Disable 4111, 4117; make 411 a 'normal' account;

* Create 5312;

* Disable 6011, 6012, 6017; make 601 a 'normal' account;

* Make 658 a 'view' account; Create 6581 and 6582;

* Disable 7011, 7012; make 701 a 'normal' account;
* Disable 7071, 7072, 7073; make 707 a 'normal' account;

* Make 758 a 'view' account; Create 7581 and 7582;

* Change name of some accounts;

Technical Information:
----------------------
For that, add an 'active' field on models:
* product.category;
* account.account.template;

Credits
=======

Contributors
------------

* Sylvain LE GAL (https://twitter.com/legalsylvain);
