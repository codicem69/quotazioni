from gnr.web.batch.btcprint import BaseResourcePrint
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from gnr.core.gnrstring import slugify
from gnr.core.gnrdecorator import public_method
from gnr.app.gnrapp import GnrApp

caption = 'Email Quotazione'

class Main(BaseResourcePrint):
    batch_title = 'Email Quotazione'
    batch_immediate='download'
    #Con batch_immediate='print' viene immediatamente aperta la stampa alla conclusione
    html_res = 'html_res/quotazione'
    batch_print_modes = ['pdf','mail_deliver']
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

    def onRecordPrinted(self, record, filepath=None):

        tbl_quotazione = self.db.table('quotazioni.quotazione')
        if not record:
            return

        builder = TableTemplateToHtml(table=tbl_quotazione)
        builder(record=record)
        prot_quot = record['quot_n']
        prot_quot = prot_quot.replace("/", "")
        nome_file = str.lower('{cl_id}.pdf'.format(
                    cl_id=prot_quot[0:]))#record[0:])

        pdfpath = self.page.site.storageNode('home:quotation', nome_file)
        #pdfpath = self.page.site.storageNode('/home/tommaso/Documenti/Agenzia/PROFORMA', nome_file)
        #result = builder.writePdf(pdfpath=pdfpath)
        #self.setInClientData(path='gnr.clientprint',
        #                     value=result.url(timestamp=datetime.now()), fired=True)
        page = self.page
        #slugify(self.print_options.get('save_as') or self.batch_parameters.get('save_as') or '')
        #self.outputFileNode(page)
        id_record = record['id']
        percorso_pdf = pdfpath.internal_path

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

        if outputFileNode:

            path_pdf = outputFileNode.internal_path
        #dal path_pdf del file in stampa verifichiamo la posizione di site in modo che quando preleviamo l'url degli attachments
        #possiamo aggiungere il path iniziale
        pos_site=str.find(path_pdf,"site")

        attcmt=[]
        file_url=[]
        #aggiungiamo agli attachments il file che andiamo a stampare
        attcmt.append(path_pdf)
        #verifichiamo il secondo allegato info port nella tabella quotazione_atc
        tbl_file =  self.db.table('quotazioni.quotazione_atc') #definiamo la variabile della tabella allegati
        att = tbl_file.query(columns="$filepath", where='$maintable_id=:main_id',main_id=self.selectedPkeys[0]).fetch()
        len_att=len(att)
        for r in range(len_att):
            url_allegato=att[r][0]
            attcmt.append(url_allegato)#appendiamo agli attcmt l'url_allegato aggiungendoci il path iniziale

        # Lettura degli account email predefiniti all'interno di Agency e Staff
        tbl_staff =  self.db.table('agz.staff')
        account_email,email_mittente,user_fullname = tbl_staff.readColumns(columns='$email_account_id,@email_account_id.address,$fullname',
                  where='$agency_id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))

        tbl_agency =  self.db.table('agz.agency')
        agency_name,ag_fullstyle,account_emailpec,emailpec_mitt = tbl_agency.readColumns(columns='$agency_name,$fullstyle,$emailpec_account_id, @emailpec_account_id.address',
                  where='$id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))

        email_template_id = self.db.application.getPreference('tpl.template_id',pkg='quotazioni')
        record_id=list(self.records)[0]
        self.db.table('email.message').newMessageFromUserTemplate(
                                                      record_id=record_id,
                                                      table='quotazioni.quotazione',
                                                      attachments=attcmt,
                                                      account_id = account_email,
                                                      template_id=email_template_id)
        self.db.commit()
