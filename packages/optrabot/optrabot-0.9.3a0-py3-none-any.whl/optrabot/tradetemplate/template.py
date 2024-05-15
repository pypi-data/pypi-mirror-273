from optrabot.stoplossadjuster import StopLossAdjuster
from optrabot.tradetemplate.templatetrigger import TemplateTrigger

class TemplateType:
	IronFly = "Iron Fly"
	PutSpread = "Put Spread"

class Template:
	def __init__(self, name: str) -> None:
		self._type = None
		self.name = name
		self._trigger = None
		self.account = None
		self.takeProfit = None
		self.stopLoss = None
		self.amount = 1
		self.minPremium = None
		self.adjustmentStep = 0.05
		self.stopLossAdjuster = None
		self.strategy = ''
		self.wing = None

	def setTrigger(self, trigger: TemplateTrigger):
		""" Defines the trigger for this template
		"""
		self._trigger = trigger

	def getTrigger(self) -> TemplateTrigger:
		""" Returns the trigger of the template
		"""
		return self._trigger
	
	def setAccount(self, account: str):
		""" Sets the account which the template is traded on 
		"""
		self.account = account
	
	def setTakeProfit(self, takeprofit: int):
		""" Sets the take profit level in % of the template
		"""
		self.takeProfit = takeprofit

	def setStopLoss(self, stoploss: int):
		""" Sets the stop loss level in % of the template
		"""
		self.stopLoss = stoploss

	def setAmount(self, amount: int):
		""" Sets the amount of contracts to be traded with this template
		"""
		self.amount = amount
	
	def setMinPremium(self, minPremium: float):
		""" Sets the minimum premium which must be received from broker in order to execute a trade
		of this template.
		"""
		self.minPremium = minPremium

	def setAdjustmentStep(self, adjustmentStep: float):
		""" Sets the price adjustment step size for the entry order adjustment
		"""
		self.adjustmentStep = adjustmentStep
	
	def setStopLossAdjuster(self, stopLossAdjuster: StopLossAdjuster):
		""" Sets the Stop Loss Adjuster for this strategy, if configured
		"""
		self.stopLossAdjuster = stopLossAdjuster
	
	def setStrategy(self, strategy: str):
		""" Sets the strategy name of this template
		"""
		self.strategy = strategy
	
	def setWing(self, wing: int):
		""" Set the wing size for Iron Fly strategies
		"""
		self.wing = wing
	
	def resetStopLossAdjuster(self):
		"""
		Resets the Stop Loss Adjuster if there is one defined
		"""
		if self.stopLossAdjuster:
			self.stopLossAdjuster.resetTrigger()

	def toDict(self):
		""" Returns a dictionary representation of the Template which is used for
		the config file.
		"""
		returnDict = {'type': self._type, 'strategy': self.strategy, 'adjustmentstep': self.adjustmentStep, 'wing': self.wing,
				'account': self.account, 'takeprofit': self.takeProfit, 'stoploss': self.stopLoss, 'amount': self.amount,
				'minpremium': self.minPremium}
		returnDict.update({'trigger':self._trigger.toDict()})
		if self.stopLossAdjuster:
			returnDict.update({'adjuststop':self.stopLossAdjuster.toDict()})
		return returnDict
	
	def __str__(self) -> str:
		""" Returns a string representation of the strategy
		"""
		templateString = ('Name: ' + self.name + ' Type: ' + self._type + ' Trigger: (' + self._trigger.type + ', ' + str(self._trigger.value) + ')' +
		' Account: ' + self.account + ' Amount: ' + str(self.amount) + ' Take Profit (%): ' + str(self.takeProfit) + ' Stop Loss (%): ' + str(self.stopLoss) +
		' Min. Premium: ' + str(self.minPremium) + ' Entry Adjustment Step: ' + str(self.adjustmentStep) + ' Wing size: ' + str(self.wing) + ' Stop Loss Adjuster: ()' + 
		str(self.stopLossAdjuster) + ')')
		return templateString