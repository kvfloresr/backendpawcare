class Users:
    def __init__(self, id, email, password, first_name, last_name, phone, role_id=None, status_view=None, license_identity=None) -> None:
        self.id = id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.role_id = role_id
        self.status_view = status_view
        self.license_identity = license_identity

    def __repr__(self):
        return (f"Users(id={self.id}, email='{self.email}', password='{self.password}', "
                f"first_name='{self.first_name}', last_name='{self.last_name}', phone='{self.phone}', "
                f"role_id={self.role_id}, status_view='{self.status_view}', license_identity='{self.license_identity}')")
