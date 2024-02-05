#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class ViewFromQuotRecAtc(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('filepath')
        r.fieldcell('external_url')
        r.fieldcell('description', edit=True)
        r.fieldcell('mimetype')
        r.fieldcell('text_content')
        r.fieldcell('is_foreign_document')
        r.fieldcell('maintable_id')

    def th_order(self):
        return 'filepath'

    def th_query(self):
        return dict(column='description', op='contains', val='')

