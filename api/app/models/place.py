from base import *
from user import User
from city import City

class Place(BaseModel):
    owner = ForeignKeyField(rel_model=User, related_name="places")
    city = ForeignKeyField(rel_model=City, related_name="places")
    name = CharField(max_length=128, null=False)
    description = TextField()
    number_rooms = IntegerField(default=0)
    number_bathrooms = IntegerField(default=0)
    max_guest = IntegerField(default=0)
    price_by_night = IntegerField(default=0)
    latitude = FloatField()
    longitude = FloatField()

    def to_hash(self):
        data = {}
        data['id'] = self.id
        data['created_at'] = self.created_at
        data['updated_at'] = self.updated_at
        data['owner_id'] = self.email
        data['city_id'] = self.first_name
        data['name'] = self.last_name
        data['description'] = self.is_admin
        data['number_rooms'] = self.number_rooms
        data['number_bathrooms'] = self.number_bathrooms
        data['max_guest'] = self.max_guest
        data['price_by_night'] = self.max_guest
        data['latitude'] = self.latitude
        data['longitude'] = self.longitude
        return data
