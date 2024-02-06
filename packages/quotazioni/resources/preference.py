# preference.py

class AppPref(object):

    def prefpane_quotazioni(self,parent,**kwargs):
        tc = parent.tabContainer(margin='2px',**kwargs)
        self.dati(tc.borderContainer(title='!!Dati'))
        self.privacy(tc.borderContainer(title='!!Email Privacy'))

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
