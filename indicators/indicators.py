from core.abstractindicators import AbstractIndicators

class Indicators(AbstractIndicators):

    MAX_PERIOD = 400
    PERIODS = [20,50,100,200]
    
    def setIndicators(historic):
        AbstractIndicators.setIndicators(historic)
