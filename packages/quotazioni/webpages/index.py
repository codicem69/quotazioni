# -*- coding: utf-8 -*-

class GnrCustomWebPage(object):
    py_requires = 'plainindex'

    @property
    def index_url(self):
        return None

    def index_dashboard(self, root):
        port_id = self.db.currentEnv.get('current_port')
        agency_id = self.db.currentEnv.get('current_agency_id')
        agency_name = ''
        if agency_id:
            agency_name = self.db.table('agz.agency').readColumns(
                where='$id=:agency_id',
                agency_id=agency_id,
                columns='$agency_name'
            ) or ''

        port_name = ''
        if port_id:
            port_name = self.db.table('unlocode.place').readColumns(
                where='$id=:port_id',
                port_id=port_id,
                columns='$descrizione'
            ) or ''

        wrapper = root.div(width='100%', height='100%',
                           text_align='center', background='white',
                           padding_top='30px')
        wrapper.img(src='/_pkg/quotazioni/resources/html_pages/images/Ranalli_Logo.svg',
                    style='width:20%;margin-top:30px;')

        titlebox = wrapper.div(display='flex',
                               justify_content='center',
                               align_items='center',
                               gap='20px',
                               margin_top='20px',
                               margin_bottom='30px')

        #titlebox.img(src='/_pkg/acc/resources/html_pages/images/accounting.svg',
        #             style='width:100px;height:100px;')

        titlebox.div(
                'QUOTATION',
                font_size='60px',
                font_weight='bold',
                color='#384D63',
                text_shadow='2px 2px 4px rgba(0,0,0,0.15)')

        titlebox.img(src='/_pkg/quotazioni/resources/html_pages/images/Quotation.svg',
                     style='width:100px;height:100px;')
        #titlebox.div('Shipsteps', font_size='100px', color='#384D63')

        wrapper.div(agency_name + ' - ' + port_name,
                    font_size='70px', color='#1d3355ff',font_weight='bold',
                    margin_top='20px', margin_bottom='30px')
        wrapper.img(src='/_rsrc/common/html_pages/images/splash_logo.png',
                    style='width:20%;margin-top:30px;')
