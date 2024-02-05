from gnr.web.batch.btcprint import BaseResourcePrint
from gnr.core.gnrstring import slugify

caption = 'Stampa Quotazione'

class Main(BaseResourcePrint):
    batch_title = 'Stampa Quotazione'
    batch_immediate='print'
    #Con batch_immediate='print' viene immediatamente aperta la stampa alla conclusione
    html_res = 'html_res/quotazione'
    #pdf_service = "wk"

    def pre_process(self):
        ag_id = self.db.currentEnv.get('current_agency_id')

        tbl_agency =  self.db.table('agz.agency')
        htmltemplate_id = tbl_agency.readColumns(columns='htmltemplate_id',
                  where='$id=:ag_id',
                    ag_id=ag_id)
        tbl_htmltemplate = self.db.table('adm.htmltemplate')
        carta_intestata = tbl_htmltemplate.readColumns(columns='name',
                            where='$id=:htmltemplate_id', htmltemplate_id=htmltemplate_id)
        #templates = 'Ranalli_st'
        self.templates = carta_intestata
        self.htmlMaker = self.page.site.loadTableScript(page=self.page, table='quotazioni.quotazione',
                                                        respath='html_res/quotazione', class_name='Main')

