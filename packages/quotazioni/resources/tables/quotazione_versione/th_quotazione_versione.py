#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from datetime import datetime
import io
from docx import Document
from docx.shared import Inches
import base64
from bs4 import BeautifulSoup
from docxtpl import DocxTemplate
from gnrpkg.quotazioni.quotation_docx import QuotationDocxBuilder
import os
from gnr.core.gnrbag import Bag

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('quotazione_id')
        r.fieldcell('version', width='3em', name='Vers.')
        r.fieldcell('data',width='5em')
        r.fieldcell('oggetto', width='auto')
        r.fieldcell('firma')
        #r.fieldcell('body_in', width='auto')
        r.fieldcell('note_vers')
        r.fieldcell('data_invio', width='10em')
        r.fieldcell('pathtopdf')
        r.cell('apri tab', name="Proforma", width='5em', cellClasses='cellbutton',
               format_buttonclass='icnBaseLens buttonIcon',
               format_isbutton=True, format_onclick=f"""var row = this.widget.rowByIndex($1.rowIndex);
               genro.childBrowserTab('/_storage/home/stampe_template/'+row['pathtopdf'].trim());""")

    def th_order(self):
        return 'version'

    def th_query(self):
        return dict(column='version', op='contains', val='')



class Form(BaseComponent):
    py_requires='gnrcomponents/pagededitor/pagededitor:PagedEditor'
    def th_form(self, form):
        #pane = form.record
        form.store.handler('load',virtual_columns='$quot_no')
        tc_m = form.center.tabContainer(title='!![en]Quotation Version')
        
        bc = tc_m.borderContainer(title='!![en]Quotation Version')
        self.datiQuot_vers(bc.borderContainer(region='center',datapath='.record',height='auto', splitter=True))
        tc = bc.tabContainer(region='bottom', height='70%', splitter=True)
        self.bodyFirst(tc.contentPane(title='!![en]First description', datapath='.record'))
        self.description(tc.contentPane(title='!![en]Costs'))
        self.extra(tc.contentPane(title='!![en]Extra details'))
        self.servIncl(tc.contentPane(title='!![en]Services included'))
        self.note(tc.contentPane(title='!![en]Notes'))
        self.specCond(tc.contentPane(title='!![en]Specific conditions'))
        self.servExcl(tc.contentPane(title='!![en]Services excluded'))
        self.surcharges(tc.contentPane(title='!![en]Surcharges'))
        self.workTimes(tc.contentPane(title='!![en]Working times'))
        self.paymentCond(tc.contentPane(title='!![en]Payment conditions'))

        self.editQuotation(tc_m.framePane(title='!![EN]Edit PDF Quotation', datapath='#FORM.editPagine'))
        #form.store.handler('load',virtual_columns='$quot_no')
        #bc = form.center.borderContainer(title='!![en]Quotation Version')
        #self.datiQuot_vers(bc.borderContainer(region='center',datapath='.record',height='auto', splitter=True))
        #tc = bc.tabContainer(region='bottom', height='70%', splitter=True)
        #self.bodyFirst(tc.contentPane(title='!![en]First description', datapath='.record'))
        #self.description(tc.contentPane(title='!![en]Costs'))
        #self.extra(tc.contentPane(title='!![en]Extra details'))
        #self.servIncl(tc.contentPane(title='!![en]Services included'))
        #self.surcharges(tc.contentPane(title='!![en]Surcharges'))
        #self.specCond(tc.contentPane(title='!![en]Specific conditions'))
        #self.servExcl(tc.contentPane(title='!![en]Services excluded'))
        #self.workTimes(tc.contentPane(title='!![en]Working times'))
        #self.note(tc.contentPane(title='!![en]Notes'))
        #self.paymentCond(tc.contentPane(title='!![en]Payment conditions'))

    def datiQuot_vers(self,bc):
        center = bc.roundedGroup(title='!![en]Quotation version',region='center',width='100%', splitter=True)
        fb = center.formbuilder(cols=3, border_spacing='4px', width='90%')
        fb.field('quotazione_id' )
        fb.field('data' )
        fb.field('version' )
        fb.field('oggetto', colspan=3, width='98%',height='100%', tag='simpleTextArea')
        fb.field('note_vers', colspan=3, width='98%',height='100%', tag='simpleTextArea')
        fb.field('firma' )
        fb.field('accettazione' )
        fb.field('data_invio' )
        fb.dataController("""if(msg=='modifica'){alert('pdf già modificato in Modifica PDF Quotazione');}""",msg='^nome_temp')

    def bodyFirst(self,frame):
        frame.simpleTextArea(value='^.body_in',title='body_in', editor=True)

    def description(self,pane):
        pane.inlineTableHandler(relation='@description_quot',viewResource='ViewFromDescription',delrow=True)
        
    def extra(self,pane):
        pane.inlineTableHandler(relation='@quotazione_extra',viewResource='ViewFromExtracost')
    
    def servIncl(self,pane):
        pane.inlineTableHandler(relation='@servincl_quot',viewResource='ViewFromServIncl')

    def servExcl(self,pane):
        pane.inlineTableHandler(relation='@serviexcl_quot',viewResource='ViewFromServExcl')

    def specCond(self,pane):
        pane.inlineTableHandler(relation='@specific_quot',viewResource='ViewFromSpecificCond')    

    def surcharges(self,pane):
        pane.inlineTableHandler(relation='@surcharge_quot',viewResource='ViewFromSurcharges') 

    def workTimes(self,pane):
        pane.inlineTableHandler(relation='@times_quot',viewResource='ViewFromTimesWork')

    def note(self,pane):
        pane.inlineTableHandler(relation='@note_quot',viewResource='ViewFromNote')

    def paymentCond(self,pane):
        pane.inlineTableHandler(relation='@paym_quot',viewResource='ViewFromPaymCond')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )

    def th_bottom_custom(self, bottom):
            bar = bottom.slotBar('10,email_quotazione,5,stampa_quot_template,5,quotazione_doc,*,10')
            btn_email =  bar.email_quotazione.button('!![en]Email Quotation')
            btn_email.dataRpc('#FORM/parent/#FORM.email_creata',self.invioEmail,record='=#FORM.record',
                                         _ask=dict(title='!![en]Select the attachments',
                                        fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                                table='quotazioni.quotazione_atc', columns='$descrizione',condition="$maintable_id =:cod",condition_cod='=#FORM.record.quotazione_id',
                                cols=4,popup=True,colspan=2),dict(name='eng',lbl='!![en]English message', tag='checkbox')]),_onResult="""
            if (result.getItem('email_creata')) {genro.publish('floating_message',{message:result.getItem('email_creata'), messageType:result.getItem('msg_type')})};
            if (result.getItem('pdf_quot')) {genro.publish('floating_message',{message:result.getItem('pdf_quot'), messageType:result.getItem('msg_type')})};""")
    
           # btn_quot_print=bar.stampa_quot_template.button('!![en]Print quotation template')
            btn_quot = bar.quotazione_doc.button('!![en]Quotanion doc.')
            btn_quot_print=bar.stampa_quot_template.button('!![en]Print quotation template', action="""
                if(html_out){genro.dlg.ask(
                "!![en]Warning",
                "!![en]<strong>PDF già modificato in Modifica PDF Quotazione. La stampa comunque sovrascrive il file pdf salvato precdentemente.</strong><br><br>"+
                "'Print PDF Originale' Stampa template originale<br>"+
                "'Print PDF Modificato' stampa PDF già modificato.",
                {cancel: 'Cancel',
                 continue: 'Print PDF Originale',
                 print_temp: 'Print PDF Modificato'},
                {cancel: function(){
                 null;},
                 continue: function(){
                 genro.publish('quot_temp', {html:null});},
                 print_temp: function(){
                 genro.publish('quot_temp', {html:html_out});}});} 
                 else {
                 genro.publish('quot_temp', {html:html_out});}""", html_out='=#FORM.record.htmlbag_quot.output')
            
            bar.dataRpc('nome_temp', self.print_quotation,record='=#FORM.record',nome_template = 'quotazioni.quotazione_versione:quotation',format_page='A4',subscribe_quot_temp=True)
                   
           # btn_quot_print.dataRpc('nome_temp', self.print_quotation,record='=#FORM.record',nome_template = 'quotazioni.quotazione_versione:quotation',format_page='A4')
            btn_quot.dataRpc('nome_temp', self.print_quotation_docx,record='=#FORM.record',nome_form='quotazione',agency_name='=#FORM.record.@agency_id.agency_name',
                             workport='=#FORM.record.@agency_id.@port.descrizione',_virtual_column='$cliente,$cliente_br')

    def editQuotation(self, frame):
            bar = frame.top.slotBar('10, lett_select,*',height='20px',border_bottom='1px solid silver')
            fb = bar.lett_select.formbuilder(cols=2,datapath='#FORM.record.htmlbag_quot')
            fb.dbselect('^.letterhead_id',table='adm.htmltemplate',lbl='carta intestata',hasDownArrow=True)
            fb.button('Get Html Quotation Doc').dataRpc('#FORM.record.htmlbag_quot.source',self.db.table('quotazioni.quotazione_versione').getHTMLDoc,
                                                quot_id='=#FORM.pkey',
                                                record_template='quotation',
                                                letterhead='.letterhead_id')
            fb.button('Stampa e Salva PDF',iconClass='iconbox save').dataRpc(self.save_quotation_pdf,record='=#FORM.record',
                                                                         html='=#FORM.record.htmlbag_quot.output',_onResult='this.form.save();')
            frame.pagedEditor(value='^#FORM.record.htmlbag_quot.source',pagedText='^#FORM.record.htmlbag_quot.output',
                              border='1px solid silver',
                              letterhead_id='^#FORM.record.htmlbag_quot.letterhead_id',
                              datasource='#FORM.record',printAction=True)

    @public_method
    def save_quotation_pdf(self,record, html=None, **kwargs):
        if not html:
            return

        record_id = record['id']

        tbl_quotv = self.db.table('quotazioni.quotazione_versione')

        # -------------------------------------------------
        # Numero quotazione
        # -------------------------------------------------

        quot_n = (
            record.getItem('quot_no')
            or ''
        )
        quot_n = quot_n.replace('/','_').replace(' ','')

        # -------------------------------------------------
        # Nome file
        # -------------------------------------------------

        filename = (
            'quotation_%s.pdf'
            % (
                quot_n
            )
        )

        # -------------------------------------------------
        # Path destinazione
        # -------------------------------------------------
        
        output = self.site.storageNode(
            'home:stampe_template',
            filename
        )

        # -------------------------------------------------
        # Destinazione
        # -------------------------------------------------

        pdfnode = self.site.storageNode(
            'home:stampe_template',
            filename
        )

        # -------------------------------------------------
        # Generazione PDF
        # -------------------------------------------------

        pdf_path = self.getService(
            'htmltopdf'
        ).htmlToPdf(
            html,
            pdfnode
        )

        # -------------------------------------------------
        # StorageNode del risultato
        # -------------------------------------------------

        result = self.site.storageNode(
            pdf_path
        )
        # stampa client
        self.setInClientData(
            path='gnr.clientprint',
            value=result.url(
                timestamp=datetime.now()
            ),
            fired=True
        )
        # -------------------------------------------------
        # URL
        # -------------------------------------------------

       #result = self.site.storageNode(
       #    pdf_path
       #)

       #return result.url(
       #    timestamp=datetime.now()
       #)

            
    @public_method
    def print_quotation(self, record, resultAttr=None, nome_template=None, format_page=None,html=None, **kwargs):
        #msg_special=None
       
        record_id=record['id']
        #html = record.getItem('htmlbag_quot.output')
        if html:
            self.save_quotation_pdf(record, html)
            nome_temp = 'modifica'
            return nome_temp
            
       #if selId is None:
       #    msg_special = 'yes'
       #    return msg_special
        tbl_quotv = self.db.table('quotazioni.quotazione_versione')
        builder = TableTemplateToHtml(table=tbl_quotv)
        quot_n = record.getItem('quot_no').replace('/', '_').replace(' ','')
        nome_temp = nome_template.replace('quotazioni.quotazione_versione:','')
        nome_file = '{cl_id}_{quot}.pdf'.format(
                    cl_id=nome_temp,quot=quot_n)
     
        template = self.loadTemplate(nome_template)  # nome del template
        #path dove salvare il file
        pdfpath = self.site.storageNode('home:stampe_template', nome_file)
        #print(X)
        #INSERIAMO IL PATH DEL FILE NELLA TABELLA QUOTAZIONE_VERSIONE
        pathfile=pdfpath.internal_path
        rec_updated=tbl_quotv.batchUpdate(dict(pathtopdf=nome_file),
                                            where='$id=:r_id', r_id=record_id)           
        self.db.commit()
        #preleviamo l'id della carta intestata dalla table agency da passare nel builder di stampa
        ag_id = self.db.currentEnv.get('current_agency_id')
        tbl_agency =  self.db.table('agz.agency')
        htmltemplate_id = tbl_agency.readColumns(columns='htmltemplate_id',
                  where='$id=:ag_id',
                    ag_id=ag_id)
        #print(x)
        #builder(record=selId, template=template)
        builder(record=record_id, template=template)#, letterhead_id=htmltemplate_id)
        #print(x)
        #selezioniamo il service di stampa
        #builder.pdf_service='wk'
        if format_page=='A3':
            builder.page_format='A3'
            builder.page_width=427
            builder.page_height=290
        result = builder.writePdf(pdfpath=pdfpath)
        
        self.setInClientData(path='gnr.clientprint',
                              value=result.url(timestamp=datetime.now()), fired=True)

    @public_method
    def print_quotation_docx(self, record, **kwargs):

        builder = QuotationDocxBuilder(
            self.db,
            self.site)
        node = self.site.storageNode(
            'home:stampe_template',
            'test.docx')
        
        result = builder.build(record['id'])
        
        self.setInClientData(
            path='gnr.clientprint',
            value=result.url(timestamp=datetime.now()),
            fired=True)  

    @public_method
    def invioEmail(self, record=None, allegati=None,eng=None,**kwargs):
        rec_id=record['id']
        #lettura degli attachment
        attcmt=[]
        dati_invio = Bag()
        if allegati:
            lista_pkeys_att = allegati.split(",")
            len_allegati = len(lista_pkeys_att) #verifichiamo la lunghezza della lista pkeys tabella allegati
            file_url=[]
            tbl_att =  self.db.table('quotazioni.quotazione_atc') #definiamo la variabile della tabella allegati
            #ciclo for per la lettura dei dati sulla tabella allegati ritornando su ogni ciclo tramite la pkey dell'allegato la colonna $fileurl e alla fine
            #viene appesa alla variabile lista file_url
            for pkeys_att in lista_pkeys_att:
                
                fileurl = tbl_att.readColumns(columns='$fileurl',
                      where='$id=:att_id',
                        att_id=pkeys_att)
                if fileurl is not None and fileurl !='':
                    file_url.append(fileurl)
        
            ln = len(file_url)
            for r in range(ln):
                fileurl = file_url[r]
                file_path = fileurl.replace('/home','site')
                fileSn = self.site.storageNode(file_path)
                attcmt.append(fileSn.internal_path)

        quot_n = record.getItem('quot_no').replace('/', '_').replace(' ','')
        nome_file = '{cl_id}_{quot}.pdf'.format(
                            cl_id='quotation',quot=quot_n)
        pdfpath = self.site.storageNode('home:stampe_template', nome_file)
        pathfile=pdfpath.internal_path
        
        if os.path.isfile(pdfpath.internal_path):
            attcmt.append(pathfile)
        else:
            dati_invio['pdf_quot']='Missing PDF Quotation. You have to print before the Quotation'
            dati_invio['msg_type']='error'
            return dati_invio

        quotazione = self.db.table('quotazioni.quotazione').record(record['quotazione_id'], ignoreDuplicate=True, ignoreMissing=True).output('bag')
        email_cliente = quotazione['@cliente_id'].getItem('email')
        emailcc_cliente = quotazione['@cliente_id'].getItem('email_cc')
        ragsoc_cliente = quotazione['@cliente_id'].getItem('rag_sociale')
        oggetto = record.getItem('oggetto')
        # Lettura degli account email predefiniti all'interno di Agency e Staff
        tbl_staff =  self.db.table('agz.staff')
        account_email,email_mittente,agency_name,user_fullname,agency_fullstyle,bank,iban,bic = tbl_staff.readColumns(columns='$email_account_id,@email_account_id.address,@agency_id.agency_name,$fullname,@agency_id.fullstyle,@agency_id.bank,,@agency_id.iban,@agency_id.bic',
                  where='$agency_id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))
        
        #Impostiamo i dati per il saluto
        now = datetime.now()
        cur_time = now.strftime("%H:%M:%S")    
        if cur_time < '13:00:00':
            if eng==True:
                sal='Good day,'
            else:
                sal='Buongiorno,'  
        elif cur_time < '17:00:00':
            if eng==True:
                sal='Good afternoon,'
            else:
                sal='Buon pomeriggio,'
        elif cur_time < '24:00:00':
            if eng==True:
                sal='Good evening,'
            else:
                sal = 'Buonasera,' 
        elif cur_time < '04:00:00':
            if eng==True:
                sal='Good night,'
            else:
                sal = 'Buona notte,' 

        # Costruisci le righe HTML
        righe_html = ''
        if eng==True:
            int_email='Quotation'
            testo_html='here attached our quotation.<br>Should you need any further clarification, please don’t hesitate to contact us.<br>Brgds'
        else:
            int_email='Quotazione'
            testo_html='qui in allegato nostra quotazione.<br>Restiamo a Vs. disposizione per qualsiasi chiarimento.<br>Cordiali saluti.'
        body_html = f"""
                <div style="font-family:Arial,sans-serif;font-size:14px;color:#333;max-width:780px;">

                    <div style="background:#2c3e50;color:#ffffff;padding:12px 32px;border-radius:6px 6px 0 0;">
                        <h2 style="margin:0;font-weight:normal;">{int_email}</h2>
                    </div>

                    <div style="background:#ffffff;padding:28px 32px;">
                        <p style="font-size:15px;">
                            to: <strong>{ragsoc_cliente}</strong>
                        </p>
                        <p style="color:#555;line-height:1.6;">
                            {sal}<br>
                            {testo_html}.<br>
                        </p>
                        <p style="color:#555;font-size:13px;">{user_fullname}</p>
                        <p style="color:#555;font-size:13px;">{agency_fullstyle}</p>
                        
                    </div>
                </div>
                    <div style="max-width:780px;border-top:1px solid #ddd;margin:0;font-size:10px;text-align:justify;">
                    <div style="padding:12px 24px;">
                        {self.getPreference('privacy_email', pkg='quotazioni')}
                    </div>
                    </div>      
                """
        self.db.table('email.message').newMessage(account_id=account_email,
                    from_address=email_mittente,
                    to_address=email_cliente,
                    cc_address=emailcc_cliente,
                    subject=f'{int_email} {oggetto}',
                    body=body_html, html=True,attachments=attcmt)
        self.db.commit()
        dati_invio['email_creata']='Email ready to be sent'
        dati_invio['msg_type']='message'
        return dati_invio