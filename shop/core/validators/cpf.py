
class ValidateCPF:

    def __init__(self,cpf):
        if type(cpf) == str:
            cpf = cpf.replace('.','')
            cpf = cpf.replace('-','')
            self.cpf = cpf.zfill(11)
        elif type(cpf) == int:
            self.cpf = str(cpf).zfill(11)

    def run(self):
        if self.notRepeat():
            count = 10
            r = 0
            for n in self.cpf[:-2]:    
                r += int(n) * count
                count -= 1
            pd = 11 - (r % 11)
            pd = 0 if pd > 9 else pd

            count = 11
            r = 0
            for n in self.cpf[:-1]:    
                r += int(n) * count
                count -= 1
            sd = 11 - (r % 11)
            sd = 0 if sd > 9 else sd

            return True if self.cpf.endswith(str(pd) + str(sd)) else False

    def notRepeat(self):
        oldV = self.cpf[0]
        for v in self.cpf:
            if v != oldV:
                return True