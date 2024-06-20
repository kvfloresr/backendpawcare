class Doctor:
    def __init__(self, id, first_name, last_name, phone, specialty_id=None, status_view=None, license_identity=None) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.specialty_id = specialty_id
        self.status_view = status_view
        self.license_identity = license_identity

    def __repr__(self):
        return (f"Doctor(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}', "
                f"phone='{self.phone}', specialty_id={self.specialty_id}, status_view='{self.status_view}', "
                f"license_identity='{self.license_identity}')")
