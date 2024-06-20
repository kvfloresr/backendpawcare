class Pet:
    def __init__(self, id, owner_id, name, species_id, breed, sex, birth_date, status_view=None) -> None:
        self.id = id
        self.owner_id = owner_id
        self.name = name
        self.species_id = species_id
        self.breed = breed
        self.sex = sex
        self.birth_date = birth_date
        self.status_view = status_view

    def __repr__(self):
        return (f"Pet(id={self.id}, owner_id={self.owner_id}, name='{self.name}', species_id={self.species_id}, "
                f"breed='{self.breed}', sex='{self.sex}', birth_date={self.birth_date}, status_view='{self.status_view}')")
