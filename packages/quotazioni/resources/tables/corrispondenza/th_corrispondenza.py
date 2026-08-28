#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('quotazione_id')
        r.fieldcell('data_comunicazione', width='10em')
        r.fieldcell('tipo')
        r.fieldcell('oggetto', width='auto')
        r.fieldcell('description', width='auto')
        r.fieldcell('mittente', width='auto')
        r.fieldcell('destinatario', width='auto')
        r.fieldcell('stato', width='auto')

    def th_order(self):
        return 'data_comunicazione'

    def th_query(self):
        return dict(column='description', op='contains', val='')


class Form(BaseComponent):
    py_requires="gnrcomponents/attachmanager/attachmanager:AttachManager"

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()
        self.datiQuotReceived(bc.roundedGroupFrame(title='!![en]Quotation received description',region='top',datapath='.record',height='120px', background='lightgrey', splitter=True))
        self.corrispondence_att(bc.contentPane(region='center', title='!![en]Attachments'))
        
    def datiQuotReceived(self,pane):    
        fb = pane.formbuilder(cols=3, border_spacing='4px')
        #fb.field('quotazione_id' )
        fb.field('tipo')
        fb.field('data_comunicazione')
        fb.field('oggetto', width='60em', tag='simpleTextArea')
        fb.field('mittente')
        fb.field('destinatario')
        fb.field('description', width='60em', tag='simpleTextArea')
        fb.field('stato')
    
    def corrispondence_att(self,pane):
        #pane.attachmentGrid(viewResource='ViewFromCorrisponceAtc')
        self.corrispondenceAttachmentGrid(pane)

    def corrispondenceAttachmentGrid(self, pane):

        bc = pane.borderContainer()

        # ============================================================
        # GRIGLIA ALLEGATI
        # ============================================================

        th = bc.contentPane(
            region='left',
            width='350px',
            splitter=True
        ).inlineTableHandler(
            relation='@atc_attachments',
            viewResource='gnrcomponents/attachmanager/attachmanager:AttachManagerView',
            hider=True,
            autoSelect=True,
            addrow=False,
            delrow=True,
            pbl_classes=True,
            semaphore=False,
            searchOn=False,
            datapath='.attachments'
        )

        # ============================================================
        # DRAG & DROP
        # ============================================================

        th.view.bottom.dropUploader(
            label='<div class="atc_galleryDropArea">'
                  '<div>Drop document here</div>'
                  '<div>or double click</div>'
                  '</div>',
            height='40px',
            onUploadingMethod=self.onUploadingAttachment,
            rpc_maintable_id='=#FORM.pkey',
            rpc_attachment_table=th.view.grid.attributes['table'],
            _class='importerPaletteDropUploaderBox',
            cursor='pointer',
            nodeId='%(nodeId)s_uploader' % th.attributes
        )

        # ============================================================
        # VIEWER
        # ============================================================

        viewer = bc.contentPane(
            region='center',
            overflow='auto'
        )

        # ============================================================
        # TOOLBAR
        #
        # contentPane non ha .top, quindi mettiamo il pulsante
        # direttamente dentro un contentPane dedicato.
        # ============================================================

        toolbar = viewer.contentPane(
            height='45px',
            border_bottom='1px solid #ccc',
            background='#f5f5f5'
        )

        toolbar.button(
            'Stampa email',
            iconClass='print',
            hidden='=!^.is_eml',
            action='PUBLISH print_email'
        )

        viewer.dataRpc(
            '.email_pdf',
            self.emailToPdf,
            fileurl='=.eml_fileurl',
            subscribe_print_email=True,
            _onResult="""
                console.log('>>> RISULTATO EMAIL TO PDF:', result);
        
                if(result && result.url){
        
                    console.log(
                        '>>> APRO PDF:',
                        result.url
                    );
        
                    window.open(
                        result.url,
                        '_blank'
                    );
        
                }
                else if(result && result.error){
        
                    alert(
                        'Errore generazione PDF: ' +
                        result.error
                    );
        
                }
            """
        )
        # ============================================================
        # AREA DOCUMENTO NORMALE
        # ============================================================

        viewer.iframe(
            src='^#FORM.reader_url',
            height='calc(100% - 45px)',
            width='100%',
            border=0,
            documentClasses=True,
            avoidCache=True,
            hidden='^.is_eml'
        )

        # ============================================================
        # AREA EML
        # ============================================================

        eml = viewer.contentPane(
            hidden='=!^.is_eml',
            overflow='auto',
            padding='15px',
            height='calc(100% - 45px)',
            box_sizing='border-box'
        )

        # ============================================================
        # HEADER EMAIL
        # ============================================================

        eml.div(
            '^.eml.subject',
            font_size='18px',
            font_weight='bold',
            margin_bottom='15px'
        )

        eml.div(
            '^.eml.from',
            margin_bottom='5px'
        )

        eml.div(
            '^.eml.to',
            margin_bottom='5px'
        )

        eml.div(
            '^.eml.cc',
            margin_bottom='5px'
        )

        eml.div(
            '^.eml.date',
            margin_bottom='15px'
        )

        # ============================================================
        # CORPO EMAIL
        # ============================================================

        bodypane = eml.contentPane(
            border_top='1px solid #ccc',
            padding_top='15px',
            overflow='visible'
        )

        bodypane.div(
            '^.eml.body',
            width='100%',
            overflow='visible'
        )

        # ============================================================
        # ALLEGATI PRESENTI NELL'EMAIL
        # ============================================================

        attpane = eml.contentPane(
            hidden='=!^.eml.attachments_html',
            margin_top='25px',
            border_top='1px solid #ccc',
            padding_top='15px'
        )

        attpane.div(
            'Allegati',
            font_weight='bold',
            font_size='16px',
            margin_bottom='10px'
        )

        attpane.div(
            '^.eml.attachments_html',
            width='100%'
        )

        # ============================================================
        # SELEZIONE FILE
        # ============================================================

        viewer.dataController(
            """
            var filename = fileurl ? fileurl.split('/').pop() : '';

            var ext = filename.indexOf('.') >= 0
                        ? filename.split('.').pop().toLowerCase()
                        : '';

            console.log('FILEURL:', fileurl);
            console.log('FILENAME:', filename);
            console.log('EXT:', ext);

            if(ext == 'eml') {

                SET .is_eml=true;
                SET .eml_fileurl=fileurl;
                SET .reader_url=null;

                console.log('>>> EMAIL SELEZIONATA');
                console.log('>>> EML FILEURL:', fileurl);

            } else {

                SET .is_eml=false;
                SET .eml_fileurl=null;
                SET .eml=null;
                SET .reader_url=fileurl;

            }
            """,
            fileurl='^.attachments.view.grid.selectedId?fileurl'
        )

        # ============================================================
        # LETTURA EML
        # ============================================================

        viewer.dataRpc(
            '.eml',
            self.readEml,
            fileurl='^.eml_fileurl',

            _onResult="""
                console.log('>>> RISULTATO READ EML:', result);

                if(result && !result.error) {

                    SET .eml.subject=result.subject || '';
                    SET .eml.from=result.from || '';
                    SET .eml.to=result.to || '';
                    SET .eml.cc=result.cc || '';
                    SET .eml.date=result.date || '';
                    SET .eml.body=result.body || '';

                    SET .eml.attachments=result.attachments || [];

                    var html = '';

                    if(result.attachments && result.attachments.length){

                        html += '<div style="display:flex;flex-direction:column;gap:8px;">';

                        result.attachments.forEach(function(att){

                            html += '<div style="padding:8px;';
                            html += 'border:1px solid #ddd;';
                            html += 'border-radius:5px;';
                            html += 'background:#f7f7f7;">';

                            html += '<a href="' + att.url + '" target="_blank">';

                            html += '📎 ' + att.filename;

                            html += '</a>';

                            html += '</div>';

                        });

                        html += '</div>';
                    }

                    SET .eml.attachments_html=html;

                } else if(result && result.error) {

                    SET .eml.subject='Errore lettura EML';
                    SET .eml.from='';
                    SET .eml.to='';
                    SET .eml.cc='';
                    SET .eml.date='';
                    SET .eml.body=result.error;
                    SET .eml.attachments=[];
                    SET .eml.attachments_html='';

                }
            """
        )

        # ============================================================
        # APERTURA ALLEGATO DELL'EML
        # ============================================================

        viewer.dataController(
            """
            if(!attachments ||
               index === null ||
               index === undefined){
                return;
            }

            var att = attachments[index];

            if(!att || !att.url){
                return;
            }

            console.log(
                'Apro allegato EML:',
                att.url
            );

            SET .is_eml=false;
            SET .reader_url=att.url;
            """,

            _fired='^eml_attachment_open',

            attachments='^.eml.attachments',

            index='=eml_attachment_open.index'
        )

        # ============================================================
        # STAMPA EMAIL
        #
        # Quando viene premuto "Stampa email":
        #
        # PUBLISH print_email
        #
        # questo controller prende il file EML e chiama
        # il metodo Python emailToPdf().
        # ============================================================

        viewer.dataController(
            """
            var fileurl = genro.getData(
                '.eml_fileurl'
            );

            console.log(
                '>>> PUBLISH STAMPA EMAIL'
            );

            console.log(
                '>>> FILEURL:',
                fileurl
            );

            if(!fileurl){

                alert(
                    'Nessuna email selezionata.'
                );

                return;
            }

            console.log(
                '>>> AVVIO EMAIL TO PDF'
            );

            genro.rpc.remoteCall(
                'emailToPdf',
                {
                    fileurl: fileurl
                },
                function(result){

                    console.log(
                        '>>> RISULTATO EMAIL TO PDF:',
                        result
                    );

                    if(result && result.url){

                        window.open(
                            result.url,
                            '_blank'
                        );

                    } else if(result && result.error){

                        alert(
                            'Errore generazione PDF:\\n' +
                            result.error
                        );

                    } else {

                        alert(
                            'PDF non generato.'
                        );
                    }
                }
            );

            """,

            _fired='^print_email'
        )

        return th

    @public_method
    def emailToPdf(self, fileurl=None, **kwargs):

        if not fileurl:
            return {
                'success': False,
                'error': 'fileurl mancante'
            }

        try:

            import os
            import re
            import html as html_module
            import email

            from email import policy
            from email.header import decode_header, make_header
            from weasyprint import HTML

            # ============================================================
            # RISOLUZIONE STORAGE
            # ============================================================

            storage_url = fileurl.lstrip('/')

            file_sn = self.site.storageNode(
                storage_url
            )

            # ============================================================
            # LETTURA EML
            # ============================================================

            with file_sn.open('rb') as f:
                data = f.read()

            if not data:
                return {
                    'success': False,
                    'error': 'Il file EML è vuoto'
                }

            # ============================================================
            # PARSING EML
            # ============================================================

            msg = email.message_from_bytes(
                data,
                policy=policy.default
            )

            # ============================================================
            # DECODIFICA HEADER
            # ============================================================

            def decode_header_value(value):

                if not value:
                    return ''

                try:
                    return str(
                        make_header(
                            decode_header(value)
                        )
                    )

                except Exception:
                    return str(value)

            # ============================================================
            # HEADER EMAIL
            # ============================================================

            subject = decode_header_value(
                msg.get('subject', '')
            )

            sender = decode_header_value(
                msg.get('from', '')
            )

            recipient = decode_header_value(
                msg.get('to', '')
            )

            cc = decode_header_value(
                msg.get('cc', '')
            )

            date = decode_header_value(
                msg.get('date', '')
            )

            # ============================================================
            # DIRECTORY EML
            # ============================================================

            attachment_dir = os.path.dirname(
                storage_url
            )

            # ============================================================
            # IMMAGINI INLINE
            # ============================================================

            cid_map = {}

            for part in msg.walk():

                content_type = part.get_content_type()

                if not content_type.startswith('image/'):
                    continue

                payload = part.get_payload(
                    decode=True
                )

                if not payload:
                    continue

                content_id = part.get(
                    'Content-ID'
                )

                if not content_id:
                    continue

                content_id = content_id.strip('<>')

                filename = part.get_filename()

                if not filename:

                    extension = (
                        content_type.split('/')[-1]
                    )

                    filename = (
                        'image.%s' %
                        extension
                    )

                filename = os.path.basename(
                    filename
                )

                filename = filename.replace(
                    '/',
                    '_'
                )

                filename = filename.replace(
                    '\\',
                    '_'
                )

                # --------------------------------------------------------
                # CARTELLA INLINE
                # --------------------------------------------------------

                inline_dir = (
                    attachment_dir +
                    '/inline'
                )

                node = self.site.storageNode(
                    inline_dir,
                    filename
                )

                with node.open('wb') as f:
                    f.write(payload)

                cid_map[
                    content_id
                ] = node.url()

            # ============================================================
            # BODY HTML
            # ============================================================

            body = ''
            is_html = False

            for part in msg.walk():

                if part.get_content_type() != 'text/html':
                    continue

                if (
                    part.get_content_disposition()
                    == 'attachment'
                ):
                    continue

                try:

                    body = part.get_content()

                except Exception:

                    payload = part.get_payload(
                        decode=True
                    )

                    if payload:

                        body = payload.decode(
                            part.get_content_charset()
                            or 'utf-8',
                            errors='replace'
                        )

                if body:

                    is_html = True
                    break

            # ============================================================
            # SE NON C'È HTML -> TEXT/PLAIN
            # ============================================================

            if not body:

                for part in msg.walk():

                    if part.get_content_type() != 'text/plain':
                        continue

                    if (
                        part.get_content_disposition()
                        == 'attachment'
                    ):
                        continue

                    try:

                        body = part.get_content()

                    except Exception:

                        payload = part.get_payload(
                            decode=True
                        )

                        if payload:

                            body = payload.decode(
                                part.get_content_charset()
                                or 'utf-8',
                                errors='replace'
                            )

                    if body:

                        is_html = False
                        break

            # ============================================================
            # SOSTITUZIONE CID
            # ============================================================

            if body and cid_map:

                for cid, url in cid_map.items():

                    body = body.replace(
                        'cid:' + cid,
                        url
                    )

                    body = body.replace(
                        'CID:' + cid,
                        url
                    )

            # ============================================================
            # PULIZIA BODY HTML
            # ============================================================

            if is_html and body:

                match = re.search(
                    r'<body[^>]*>(.*?)</body>',
                    body,
                    re.IGNORECASE | re.DOTALL
                )

                if match:
                    body = match.group(1)

                body = re.sub(
                    r'</?html[^>]*>',
                    '',
                    body,
                    flags=re.IGNORECASE
                )

                body = re.sub(
                    r'</?head[^>]*>',
                    '',
                    body,
                    flags=re.IGNORECASE
                )

                body = re.sub(
                    r'</?body[^>]*>',
                    '',
                    body,
                    flags=re.IGNORECASE
                )

            else:

                body = html_module.escape(
                    body or ''
                )

                body = body.replace(
                    '\n',
                    '<br>'
                )

            # ============================================================
            # NOME FILE PDF
            # ============================================================

            filename = subject or 'email'

            filename = re.sub(
                r'[^\w\s.-]',
                '_',
                filename
            )

            filename = re.sub(
                r'\s+',
                '_',
                filename
            )

            filename = filename[:100]

            pdf_filename = (
                filename +
                '.pdf'
            )

            # ============================================================
            # CC
            # ============================================================

            cc_html = ''

            if cc:

                cc_html = """
                    <div class="field">
                        <span class="label">CC:</span>
                        %s
                    </div>
                """ % html_module.escape(cc)

            # ============================================================
            # HTML PDF
            # ============================================================

            pdf_html = """
    <!DOCTYPE html>

    <html>

    <head>

    <meta charset="UTF-8">

    <style>

    @page {
        size: A4;
        margin: 18mm 15mm 18mm 15mm;
    }

    html,
    body {
        margin: 0;
        padding: 0;
    }

    body {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 11pt;
        line-height: 1.4;
        color: #222;
    }

    .email-header {
        border-bottom: 1px solid #cccccc;
        padding-bottom: 12px;
        margin-bottom: 18px;
        page-break-inside: avoid;
    }

    .subject {
        font-size: 16pt;
        font-weight: bold;
        margin-bottom: 12px;
    }

    .field {
        margin-bottom: 4px;
    }

    .label {
        font-weight: bold;
    }

    .email-body {
        width: 100%%;
        overflow: visible;
    }

    .email-body img {
        max-width: 100%%;
        height: auto;
    }

    .email-body table {
        max-width: 100%%;
        border-collapse: collapse;
    }

    .email-body td,
    .email-body th {
        vertical-align: top;
    }

    .email-body pre {
        white-space: pre-wrap;
        word-wrap: break-word;
    }

    .email-body a {
        color: #222;
    }

    </style>

    </head>

    <body>

    <div class="email-header">

        <div class="subject">
            %s
        </div>

        <div class="field">
            <span class="label">Da:</span>
            %s
        </div>

        <div class="field">
            <span class="label">A:</span>
            %s
        </div>

        %s

        <div class="field">
            <span class="label">Data:</span>
            %s
        </div>

    </div>

    <div class="email-body">

    %s

    </div>

    </body>

    </html>
    """ % (
                html_module.escape(subject),
                html_module.escape(sender),
                html_module.escape(recipient),
                cc_html,
                html_module.escape(date),
                body
            )

            # ============================================================
            # PDF NODE
            # ============================================================

            pdf_node = self.site.storageNode(
                attachment_dir,
                pdf_filename
            )

            # ============================================================
            # GENERAZIONE PDF
            # ============================================================

            pdf_data = HTML(
                string=pdf_html
            ).write_pdf()

            # ============================================================
            # SCRITTURA PDF
            # ============================================================

            with pdf_node.open('wb') as f:
                f.write(pdf_data)

            # ============================================================
            # RISULTATO
            # ============================================================

            return {
                'success': True,
                'url': pdf_node.url(),
                'filename': pdf_filename
            }

        except Exception as e:

            import traceback

            traceback.print_exc()

            return {
                'success': False,
                'error': str(e)
            }



    
    
    @public_method
    def readEml(self, fileurl=None, **kwargs):
    
        if not fileurl:
            return {'error': 'fileurl mancante'}
    
        try:
        
            import email
            import os
    
            from email import policy
            from email.header import decode_header, make_header
    
            # ============================================================
            # FUNZIONI DI SUPPORTO
            # ============================================================
    
            def decode_filename(filename):
            
                if not filename:
                    return None
    
                try:
                    return str(
                        make_header(
                            decode_header(filename)
                        )
                    )
                except Exception:
                    return filename
    
            def safe_filename(filename):
            
                filename = decode_filename(filename)
    
                if not filename:
                    return 'attachment'
    
                filename = os.path.basename(filename)
    
                filename = filename.replace('/', '_')
                filename = filename.replace('\\', '_')
    
                return filename
    
            # ============================================================
            # RISOLUZIONE STORAGE
            # ============================================================
    
            storage_url = fileurl.lstrip('/')
    
            file_sn = self.site.storageNode(storage_url)
    
            # ============================================================
            # DIRECTORY DEL FILE EML
            # ============================================================
    
            # Esempio:
            #
            # storage_url:
            #
            # home:quotazioni_corrispondenza/xZauqz5yOxaCU6mkAEQAsw/file.eml
            #
            # attachment_dir:
            #
            # home:quotazioni_corrispondenza/xZauqz5yOxaCU6mkAEQAsw
    
            attachment_dir = os.path.dirname(storage_url)
    
            # ============================================================
            # LETTURA FILE EML
            # ============================================================
    
            with file_sn.open('rb') as f:
                data = f.read()
    
            if not data:
                return {
                    'error': 'Il file EML è vuoto',
                    'fileurl': fileurl
                }
    
            # ============================================================
            # PARSING EML
            # ============================================================
    
            msg = email.message_from_bytes(
                data,
                policy=policy.default
            )
    
            # ============================================================
            # HEADER
            # ============================================================
    
            subject = msg.get('subject', '')
            sender = msg.get('from', '')
            recipient = msg.get('to', '')
            cc = msg.get('cc', '')
            date = msg.get('date', '')
    
            subject = decode_filename(subject)
    
            # ============================================================
            # BODY
            # ============================================================
    
            body = ''
            is_html = False
    
            # ============================================================
            # IMMAGINI INLINE / CID
            # ============================================================
    
            cid_map = {}
    
            for part in msg.walk():
            
                content_type = part.get_content_type()
    
                if not content_type.startswith('image/'):
                    continue
                
                payload = part.get_payload(decode=True)
    
                if not payload:
                    continue
                
                content_id = part.get('Content-ID')
    
                if not content_id:
                    continue
                
                content_id = content_id.strip('<>')
    
                filename = part.get_filename()
    
                if not filename:
                    extension = content_type.split('/')[-1]
                    filename = 'image.%s' % extension
    
                filename = safe_filename(filename)
    
                # --------------------------------------------------------
                # CARTELLA INLINE
                # --------------------------------------------------------
    
                inline_dir = attachment_dir + '/inline'
    
                node = self.site.storageNode(
                    inline_dir,
                    filename
                )
    
                with node.open('wb') as f:
                    f.write(payload)
    
                cid_map[content_id] = node.url()
    
            # ============================================================
            # RICERCA BODY HTML
            # ============================================================
    
            for part in msg.walk():
            
                if part.get_content_type() != 'text/html':
                    continue
                
                if part.get_content_disposition() == 'attachment':
                    continue
                
                try:
                
                    body = part.get_content()
    
                except Exception:
                
                    payload = part.get_payload(decode=True)
    
                    if payload:
                    
                        body = payload.decode(
                            part.get_content_charset() or 'utf-8',
                            errors='replace'
                        )
    
                if body:
                    is_html = True
                    break
                
            # ============================================================
            # SOSTITUZIONE CID
            # ============================================================
    
            if body and is_html and cid_map:
            
                for cid, url in cid_map.items():
                
                    body = body.replace(
                        'cid:' + cid,
                        url
                    )
    
                    body = body.replace(
                        'CID:' + cid,
                        url
                    )
    
            # ============================================================
            # SE NON C'È HTML -> TEXT/PLAIN
            # ============================================================
    
            if not body:
            
                for part in msg.walk():
                
                    if part.get_content_type() != 'text/plain':
                        continue
                    
                    if part.get_content_disposition() == 'attachment':
                        continue
                    
                    try:
                    
                        body = part.get_content()
    
                    except Exception:
                    
                        payload = part.get_payload(decode=True)
    
                        if payload:
                        
                            body = payload.decode(
                                part.get_content_charset() or 'utf-8',
                                errors='replace'
                            )
    
                    if body:
                        is_html = False
                        break
                    
            # ============================================================
            # ALLEGATI
            # ============================================================
    
            attachments_result = []
    
            for part in msg.walk():
            
                disposition = part.get_content_disposition()
                filename = part.get_filename()
    
                # --------------------------------------------------------
                # SOLO ALLEGATI NORMALI
                # --------------------------------------------------------
    
                if disposition != 'attachment':
                    continue
                
                if not filename:
                    continue
                
                payload = part.get_payload(decode=True)
    
                if not payload:
                    continue
                
                filename = safe_filename(filename)
    
                try:
                
                    # ====================================================
                    # SALVA NELLA STESSA CARTELLA DELL'EML
                    # ====================================================
    
                    node = self.site.storageNode(
                        attachment_dir,
                        filename
                    )
    
                    with node.open('wb') as f:
                        f.write(payload)
    
                    # ====================================================
                    # RISULTATO
                    # ====================================================
    
                    attachments_result.append({
                        'filename': filename,
                        'url': node.url(),
                        'content_type': part.get_content_type(),
                        'size': len(payload),
                        'inline': False
                    })
    
                except Exception:
                
                    import traceback
                    traceback.print_exc()
    
            # ============================================================
            # RISULTATO FINALE
            # ============================================================
    
            return {
                'subject': subject or '',
                'from': sender or '',
                'to': recipient or '',
                'cc': cc or '',
                'date': date or '',
                'body': body or '',
                'is_html': is_html,
                'attachments': attachments_result
            }
    
        except Exception as e:
        
            import traceback
            traceback.print_exc()
    
            return {
                'error': str(e),
                'fileurl': fileurl
            }
             
    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
