This project contains several Odoo projects in which I have been working, these are distributed in folders by topic:

```bash
├───exercises   # Exercises which have been used to learn about Odoo
│   ├───odoo_inheritance_exercise
│   └───odoo_security_exercise
│
├───modules     # Modules to extend the Odoo funcionality
│   ├───soccer_sweepstake
│   └───development_tools
│
├───scaffolds   # Scaffold templates which can be used whith odoo.py scaffold -t
│   ├───common_scaffolding
│   └───enterprise_name
│
├───tools       # Some usefull  tools and scripts to work with Odoo
│   ├───batch
│   └───python
│
└───_assets_    # Resources used in this project (images, icons, fonts, etc...)
```

## Exercises

Sometimes, it's not possible to find required information about a searched topic in the Odoo documentation, forums, etc. I this case, the only way to resolve the raised question is try it for yourself.

### odoo_inheritance_exercise

Module to illustrate the different possibilities of inheritance in Odoo. It have a basic model which will be the parent of an an extended model, an inherited model and a delegate model.

### odoo_security_exercise

Module to illustrate how to use res.groups, ir.model.access and ir.rule in Odoo to set the security access rights.

## Modules

Odoo is an extensible system which can be extended adding new modules to it, the following are available in this project:

### soccer_sweepstake

- Module which can be used to bet based on results of football matches.

### development_tools

This module provides some technical reports listed below:

- **Groups implied**: pivot table which shows the dependencies between the existing groups.
- **Users by groups**: pivot table which shows which users belong to each group.
- **Modules by groups** pivot table which shows model access rules to each group.

This module also provides some test tools listed below:

- **Domain tester**: wizard which allows user to test domains over any existing model.
- **Code tester**: wizard which allows user to entered python code and test it.

## Scaffolds

The Odoo command line allows to create new modules starting from existing scaffolding templates, the following are available in this project:

### common_scaffolding

- Common directory structure and manifest file.
- A sample of a model, a view and a controller.

### enterprise_name

- Common directory structure and manifest file.
- Data files to overwrite:
    - The main company
	- The main company partner
	- The administrator user
	- The administrator partner
- Empty files to ovewrite access rights and translation terms.
