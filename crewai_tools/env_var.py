class EnvVar:
    def _init_(self, name: str, description: str = "", required: bool = False):
        self.name = name
        self.description = description
        self.required = required

