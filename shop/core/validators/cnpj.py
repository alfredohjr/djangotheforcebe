
class ValidateCNPJ:

    def __init__(self,cnpj):
        if type(cnpj) == str:
            for c in ['.','/','-']:
                cnpj = cnpj.replace(c,'')

            self.cnpj = cnpj.zfill(13)
        elif type(cnpj) == int:
            self.cnpj = str(cnpj).zfill(13)
    
    def run(self):

        reverse_cnpj = list(self.cnpj)
        reverse_cnpj.reverse()
        reverse_cnpj

        if self.notRepeat():

            count = 2
            r = 0
            for n in reverse_cnpj[2:]:
                r += int(n) * count
                count += 1
                if count > 9:
                    count = 2
            pd = 11 - (r % 11)
            pd = 0 if pd > 9 else pd

            count = 2
            r = 0
            for n in reverse_cnpj[1:]:
                r += int(n) * count
                count += 1
                if count > 9:
                    count = 2
            sd = 11 - (r % 11)
            sd = 0 if sd > 9 else sd
            return True if self.cnpj.endswith(str(pd) + str(sd)) else False
        else:
            return False

    def notRepeat(self):

        oldV = self.cnpj[0]
        for v in self.cnpj:
            if v != oldV:
                return True