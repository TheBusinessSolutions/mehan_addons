============
NUTS Regions
============

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:de0a0ba4adfbcb8ea3f66adfe66db191ad9a040fc824ffb6950c11d015a2efeb
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fpartner--contact-lightgray.png?logo=github
    :target: https://github.com/OCA/partner-contact/tree/15.0/base_location_nuts
    :alt: OCA/partner-contact
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/partner-contact-15-0/partner-contact-15-0-base_location_nuts
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runboat-Try%20me-875A7B.png
    :target: https://runboat.odoo-community.org/builds?repo=OCA/partner-contact&target_branch=15.0
    :alt: Try me on Runboat

|badge1| |badge2| |badge3| |badge4| |badge5|

This module allows to import NUTS locations.

Creates four new fields in Partner object, one per NUTS level

* NUTS L1: Country level
* NUTS L2: Normally state or big region level
* NUTS L3: Normally substate or state level
* NUTS L4: Normally small region or province level

This module allows to set the flag *Not updatable* in a NUTS region so that it gets no more updated nor deleted by the import wizard.

Usually NUTS regions have to stay updated with the real ones, but the user may want to update a region's field (name, parent, ...) or create a new ones.
With this module, flagging such records as *Not updatable* prevents them from being overwritten or deleted by the import wizard.

**Table of contents**

.. contents::
   :local:

Installation
============

We recommend to install another addon (one for each country) in order to relate
NUTS with states defined by each localization addon, for example:

* l10n_es_location_nuts : Spanish Provinces (NUTS level 4) related to Partner State
* l10n_de_location_nuts : German states (NUTS level 2) related to Partner State
* l10n_nl_location_nuts : Dutch provinces (NUTS level 3 and 4) related to Partner State

Configuration
=============

After installation, you must click at import wizard to populate NUTS items
in Odoo database in:
Contacts > Configuration > Localization > Import NUTS 2013

This wizard will download from Europe RAMON service the metadata to
build NUTS in Odoo. Each localization addon (l10n_es_location_nuts,
l10n_de_location_nuts, ...) will inherit this wizard and
relate each NUTS item with states. So if you install a new localization addon
you must re-build NUTS clicking this wizard again.

Usage
=====

Only Administrator can manage NUTS list (it is not neccesary because
it is an European convention) but any registered user can read them,
in order to allow to assign them to partner object.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/partner-contact/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/OCA/partner-contact/issues/new?body=module:%20base_location_nuts%0Aversion:%2015.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* Tecnativa
* Agile Business Group

Contributors
~~~~~~~~~~~~

* Rafael Blasco <rafael.blasco@tecnativa.com>
* Antonio Espinosa <antonio.espinosa@tecnativa.com>
* Jairo Llopis <jairo.llopis@tecnativa.com>
* David Vidal <david.vidal@tecnativa.com>
* Simone Rubino <simone.rubino@agilebg.com>
* Alexandre Díaz <alexandre.diaz@tecnativa.com>
* Andrea Stirpe <a.stirpe@onestein.nl>

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `OCA/partner-contact <https://github.com/OCA/partner-contact/tree/15.0/base_location_nuts>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
