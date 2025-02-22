import logging

class Logger:
	def __init__(self):
		self.logger = None

	def getlogger(self, name):
		self.logger = logging.getLogger(name)
		
		self.logger.setLevel(logging.INFO)

		# create a file handler
		self.handler = logging.FileHandler('app.log')
		self.handler.setLevel(logging.INFO)

		# create a logging format
		self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
		self.handler.setFormatter(self.formatter)

		# add the file handler to the logger
		self.logger.addHandler(self.handler)
		return self.logger