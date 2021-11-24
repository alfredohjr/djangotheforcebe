from io import BytesIO
import pandas as pd
import string
import dotenv

config = dotenv.dotenv_values()

class df2Excel:
    
    def __init__(self,df,destiny):

        if df.index.size > 300000:
            raise Exception('Muito grande para executar a formatação')
        
        self.df = df
        self.destiny = destiny
        self.sheetname = 'Sheet1'
        self.engine = 'xlsxwriter'
        self.datetime_format = 'dd/mm/yyyy'
        self.date_format = 'dd/mm/yyyy'
        self.header = '&L&G'
        self.writer = pd.ExcelWriter(
            destiny,
            engine=self.engine,
            datetime_format=self.datetime_format,
            date_format=self.date_format)
        self._columnsTitle()
        df.to_excel(self.writer,self.sheetname,index=None)

        self.workbook = self.writer.book
        self.worksheet = self.writer.sheets[self.sheetname]

        self.formatNumber = self.workbook.add_format({'num_format': '#,##0.00'})
        self.formatCurrency = self.workbook.add_format({'num_format': 'R$#,##0.00'})
        self.formatCPF = self.workbook.add_format({'num_format': '0##"."###"."###-##'})
        self.formatCNPJ = self.workbook.add_format({'num_format': '00"."###"."###"/"###-##'})
        self.formatTel = self.workbook.add_format({'num_format': '"("##")"####-####'})
        self.formatCel = self.workbook.add_format({'num_format': '"("##")"#####-####'})
        self.formatPercent = self.workbook.add_format({'num_format': '0.00%'})

        # self.image_file = open(config.get('path_home') + '/media/jacomar.jpg','rb')
        # self.image_data = BytesIO(self.image_file.read())

        self.uppercase = string.ascii_uppercase

        self._sizeOfColumns()


    def toNumber(self,column):
        self.worksheet.set_column('{column}:{column}'.format(column=column.upper()),None,self.formatNumber)
        self.updateSizeColumns(column,5)

    def toCurrency(self,column):
        for c in column:
            self.worksheet.set_column('{column}:{column}'.format(column=c.upper()),None,self.formatCurrency)
            self.updateSizeColumns(c,7)

    def toCPF(self,column):
        for c in column:
            self.worksheet.set_column('{column}:{column}'.format(column=c.upper()),None,self.formatCPF)
            self.updateSizeColumns(c,4)

    def toCNPJ(self,column):
        for c in column:
            self.worksheet.set_column('{column}:{column}'.format(column=c.upper()),None,self.formatCNPJ)
            self.updateSizeColumns(c,6)

    def toTel(self,column):
        for c in column:
            self.worksheet.set_column('{column}:{column}'.format(column=c.upper()),None,self.formatTel)
            self.updateSizeColumns(c,6)

    def toCel(self,column):
        for c in column:
            self.worksheet.set_column('{column}:{column}'.format(column=c.upper()),None,self.formatCel)
            self.updateSizeColumns(c,6)

    def toPercent(self,column):
        for c in column:
            self.worksheet.set_column('{column}:{column}'.format(column=c.upper()),None,self.formatPercent)
            self.updateSizeColumns(c,4)

    def updateSizeColumns(self,column,newSize):
        index = self.uppercase.find(column)
        key = self.df.keys()[index]
        self.obj[key] += newSize

    def _sizeOfColumns(self):
        self.obj = {}
        for k in self.df.keys():
        
            size = 0
            for i in self.df[k]:
                i = len(str(i))
                if i > size:
                    size = i

            self.obj[k] = size

    def _formatExcel(self):
        
        for k,v in self.obj.items():
        
            if v < len(k):
                v = len(k)

            column_width = v + 2
            col_idx = self.df.columns.get_loc(k)
            self.writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_width)

    def _columnsUpercase(self):
        columnMap = {}
        for k in self.df.keys():
            columnMap[k] = str(k).capitalize()
        self.df.rename(columns=columnMap,inplace=True)
        
        
    def _columnsTitle(self):
        columnMap = {}
        for k in self.df.keys():
            columnMap[k] = str(k).title()
        self.df.rename(columns=columnMap,inplace=True)

    def _addHeader(self):
        self.worksheet.set_margins(top=1)
        # self.worksheet.set_header('&C&G',
        #                         {'image_center':'media/jacomar.jpg',
        #                         'image_data_left': self.image_data})
        # self.worksheet.insert_image('A1','media/jacomar.jpg')
    
    def _addFooter(self):
        self.worksheet.set_footer('&CPagina &P de &N')

    def _addProperties(self):
        self.workbook.set_properties({
            'title': self.destiny.split('/')[-1].split('.')[0],
            'author': 'Supermercado Jacomar LTDA',
            'comments': 'Criado através da engine XlsxWriter com python'
        })

    def _readOnly(self):
        self.workbook.read_only_recommended()

    def _protect(self):
        self.worksheet.protect('senhaContraAlteracao',{
            'objects':               True,
            'scenarios':             True,
            'format_cells':          True,
            'format_columns':        True,
            'format_rows':           True,
            'insert_columns':        True,
            'insert_rows':           False,
            'insert_hyperlinks':     True,
            'delete_columns':        True,
            'delete_rows':           False,
            'select_locked_cells':   True,
            'sort':                  True,
            'autofilter':            True,
            'pivot_tables':          True,
            'select_unlocked_cells': True,
        })

    def save(self):
        self._addProperties()
        self._formatExcel()
        self._addHeader()
        self._addFooter()
        # self._protect()
        # self._readOnly()
        self.writer.save()