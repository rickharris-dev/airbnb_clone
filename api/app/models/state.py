from base import *

class State(BaseModel):
    name = CharField(max_length=128, null=False, unique=True)

    def to_hash(self):
        data = {}
        data['name'] = self.name
        return super(User, self).to_hash(self, data)
