class Dependency:
	def __init__(self, name, kind):
		self._name = name
		self._kind = kind

	def __getattr__(self, name):
		if name == 'name':
			return self._name

		raise AttributeError(f'No such attribute: {name}')

class Dependencies:
	def __init__(self, deps):
		self._deps = deps
   
	def from_map(deps):  # map: kind -> [Dependency]
		for key in deps.keys():
			if not key in ['normal', 'dev', 'build']:
				raise ValueError(f'Unexpected map key {key}')

		ret = []
		for kind, deps in deps.items():
			for dep in deps:
				ret.append(Dependency(dep, kind))
		return Dependencies(ret)
   
	def __len__(self):
		return len(self._deps)

	def find_by(self, pred):
		for dep in self._deps:
			if pred(dep):
				return dep

		return None

	def find_by_name(self, name):
		return self.find_by(lambda d: d.name == name)
  