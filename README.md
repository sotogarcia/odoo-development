# Odoo modules

https://doc.odoo.com/trunk/server/03_module_dev/
https://doc.odoo.com/trunk/web/web_controllers/
https://www.odoo.com/documentation/8.0/reference.html

## Module tree

Odoo modules must be built according to MVC architecture, its models, views and controllers must be stored in their respective folders: models, views, controllers.

All static files and web resources must be stored in folder named static, in which there will be specific folders for each type of resource.

Other types of resources also have their own folders, like the wizards, reports, translations, etc...

Below is the most common folder structure: 

```
├───controllers         # MVC controllers, included for web, that will be added
├───data                # ??
├───demo				# Demo and unit test population data
├───doc                 # reStructuredText for technical documentation.
├───i18n                # Translation files
├───models              # MVC models that will be added to ERP
├───report              # Report definitions, their views and source codes
├───security            # Declaration of groups and access rights
├───static              # Static files used in module
│   ├───description     # Description shown on module configuration screen 
│   ├───lib             # Files from others used in module 
│   └───src             # Web design resource files
│       ├───css         # Cascade Style Sheets
│       ├───img         # Images used in web design
│       ├───js          # Javascript files
│       └───xml         # XML templates used in web design
├───test                # Automated YAML Tests
├───tests               # Test files written in Python
├───views               # MVC views (forms,lists), menus and actions
└────wizard             # Wizards to interactive sessions with the user
```

Module structure also include next two files:

```
├───__openerp__.py		# Module manifest file
└───__init__.py			# Module entry point
```

### i18n

Stores Portable object files (.po) as used by php gettext 

### secutity

Folder named *security* usually have two files:

* **ir.model.access.csv**
* **[*module_name*]_security.xml**

> Read more in [http://toolkt.com/site/security-in-openerp/](http://toolkt.com/site/security-in-openerp/)

### static/description

Usually have at least two files:

* **index.html** contains module description shown on setup screen.
* **icon.png** 128x128x32 png image shown as module icon.

## Manifest file

The manifest file serves to both declare a python package as an Odoo module, and to specify a number of module metadata.

> Read more in [http://odoo-80.readthedocs.org/en/latest/reference/module.html](http://odoo-80.readthedocs.org/en/latest/reference/module.html)

It is a file called __openerp__.py and contains a single Python dictionary, each dictionary key specifying a module metadatum.

```
# -*- coding: utf-8 -*-
{
	'name' : 'module_name',
	'summary' : 'short_description',
	'version' : '1.0',
	'description' : "reStructuredText_description",
	'author' : 'author_name',
	'website' : 'author_website',
	'license' : 'AGPL-3',
	'category' : 'Uncategorized',
	'depends' : [ 'base' ],
	'data' : [
		'security/module_name.xml',
		'security/ir.model.access.csv'
	],
	'demo' : ['demo/demo.xml'],
	'auto_install' : False,
}
```
> **Not documented fields:** *'installable'* and *'application'*

### Manifest fields

* **name** *(str, required)*: The human-readable name of the module.
* **version** *(str)*: This module’s version, should follow semantic versioning rules.
* **description** *(str)*: Extended description for the module, in reStructuredText.
* **author** *(str)*: Name of the module author.
* **website** *(str)*: Website URL for the module author.
* **license** *(str, defaults: AGPL-3)*: Distribution license for the module.
* **category** *(str, default: Uncategorized)*: Classification category within Odoo, rough business domain for the module. 
	- Red more in [about odoo categories](https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml).
* **depends** *(list(str))*: Odoo modules which must be loaded before this one, either because this module uses features they create or because it alters resources they define.
	* When a module is installed, all of its dependencies are installed before it. Likewise during modules loading.
* **data** *(list(str))*: List of data files which must always be installed or updated with the module. A list of paths from the module root directory
* **demo** *(list(str))*: List of data files which are only installed or updated in demonstration mode.
* **auto_install** *(bool, default: False)*: If True, this module will automatically be installed if all of its dependencies are installed.
	* It is generally used for “link modules” implementing synergic integration between two otherwise independent modules.
	* For instance sale_crm depends on both sale and crm and is set to auto_install. When both sale and crm are installed, it automatically adds CRM campaigns tracking to sale orders without either sale or crm being aware of one another

