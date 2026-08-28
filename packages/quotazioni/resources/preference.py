# preference.py

class AppPref(object):

    def prefpane_quotazioni(self,parent,**kwargs):
        tc = parent.tabContainer(margin='2px',**kwargs)
        self.dati(tc.borderContainer(title='!!Dati'))
        self.privacy(tc.borderContainer(title='!!Email Privacy'))
        self.accettazione(tc.borderContainer(title='!!Accettazione'))

    def dati(self,pane):
        fb = pane.formbuilder(cols=2, border_spacing='4px')   
        fb.br()
        fb.dbSelect(value='^.tpl.template_id', lbl='Template',
                        table='adm.userobject', hasDownArrow=True, condition='$objtype=:tpl', condition_tpl='template',
                        rowcaption='$code,$description', auxColumns='$description,$userid', selected_tbl='^.tpl.tbl')

    def privacy(self,pane):
        fb = pane.formbuilder(cols=1)
        fb.div('', width='100em')
        fb.simpleTextArea('^.privacy_email',lbl='Email Privacy',width='100em', height='200px',editor=True)


    def accettazione(self,pane):
        fb = pane.formbuilder(cols=1)
        fb.div('', width='100em')
        fb.simpleTextArea('^.accettazione',lbl='Accettazione',width='100em', height='200px',editor=True)
        fb.div("""Con la variabile ${cliente} il sistema ci sotituirà automaticamente la variabile con il relativo nomi del cliente.<br><br>
                  ACCETTAZIONE OFFERTA<br>
                  Con la sottoscrizione della presente offerta, ${cliente} dichiara di accettare integralmente ed incondizionatamente le condizioni in essa contenute.
                  Ai sensi degli artt. 1341 e 1342 c.c., ${cliente}, dichiara di approvare espressamente le limitazioni di responsabilità di cui al N.B. sopra indicato.
                  Firma aggiuntiva richiesta.<br><br>

                  DATA E LUOGO                                                FIRMA AUTORIZZATA""")
