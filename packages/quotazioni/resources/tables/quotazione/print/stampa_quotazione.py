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

    # DEFINIAMO IL PATH DEL SALVATAGGIO E IL NOME DEL FILE
    def result_handler_pdf(self, resultAttr):

        if not self.results:
            return '{btc_name} completed'.format(btc_name=self.batch_title), dict()
        save_as = slugify(self.print_options.get('save_as') or self.batch_parameters.get('save_as') or '')

        if not save_as:
            if len(self.results)>1:
                save_as = 'multiple_quotation' #slugify(self.batch_title)
            else:
                save_as =  self.page.site.storageNode(self.results['#0']).cleanbasename[0:]
                #aggiunto [9:] per avere il record -9 caratteri iniziali

        outputFileNode=self.page.site.storageNode('home:quotation', save_as,autocreate=-1)
        #outputFileNode=self.page.site.storageNode('/home/tommaso/Documenti/Agenzia/PROFORMA', save_as,autocreate=-1)
        #self.print_options.setItem('zipped', True) # settando il valore zipped a True ottengo un file zippato
        zipped =  self.print_options.get('zipped')
        immediate_mode = self.batch_immediate
        if immediate_mode is True:
            immediate_mode = self.batch_parameters.get('immediate_mode')
        if immediate_mode and zipped:
            immediate_mode = 'download'
        if zipped:
            outputFileNode.path +='.zip'
            self.page.site.zipFiles(list(self.results.values()), outputFileNode)
        else:
            outputFileNode.path +='.pdf'
            self.pdf_handler.joinPdf(list(self.results.values()), outputFileNode)
        self.fileurl = outputFileNode.url(nocache=True, download=True)
        inlineurl = outputFileNode.url(nocache=True)
        resultAttr['url'] = self.fileurl
        resultAttr['document_name'] = save_as
        resultAttr['url_print'] = 'javascript:genro.openWindow("%s","%s");' %(inlineurl,save_as)
        if immediate_mode:
            resultAttr['autoDestroy'] = 600
        if immediate_mode=='print':
            self.page.setInClientData(path='gnr.clientprint',value=inlineurl,fired=True)
        elif immediate_mode=='download':
            self.page.setInClientData(path='gnr.downloadurl',value=inlineurl,fired=True)
