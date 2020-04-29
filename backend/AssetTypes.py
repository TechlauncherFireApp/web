class Asset(object):
    def __init__(self, name,advancedNo,basicNo):
        self.name = name
        self.advancedNo=advancedNo
        self.basicNo=basicNo
        def getName(self):
            return name

class LightUnit(Asset):
    def __init__(self,name):
        super().__init__(name)
        self.name = name
        self.advancedNo = 2
        self.basicNo = 1

