from dataclasses import dataclass

from shared.utils.duplicates import Duplicates


@dataclass
class QuickDoc:
	name: str
	path: str


class QuickDocs:

	def __init__(self, docs):

		self.docs = docs
		self.docs_by_name = {}

		for doc in docs:
			self.docs_by_name[doc.name] = doc

		self.duplicates = self._duplicates()

	def __iter__(self):
		return iter(self.docs)

	def get(self, value):

		if type(value) == str:
			return self.docs_by_name[value]

		return self.docs[value]

	def has(self, value):
		return value in self.docs_by_name

	def _duplicates(self):

		duplicates = Duplicates()

		for doc in self.docs:
			duplicates.add (doc.name, doc)

		return duplicates

