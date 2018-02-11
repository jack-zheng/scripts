class TestCase:
	def __init__(self, id, status=False):
		self.id = id
		self.status = status
	
	def __eq__(self, other):
		return self.id == other.id
