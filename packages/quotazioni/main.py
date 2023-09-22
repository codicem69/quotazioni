#!/usr/bin/env python
# encoding: utf-8
from gnr.app.gnrdbo import GnrDboTable, GnrDboPackage

class Package(GnrDboPackage):
    def config_attributes(self):
        return dict(comment='quotazioni package',sqlschema='quotazioni',sqlprefix=True,
                    name_short='Quotazioni', name_long='quotazioni', name_full='Quotazioni')
                    
    def config_db(self, pkg):
        pass
        
class Table(GnrDboTable):
    pass
