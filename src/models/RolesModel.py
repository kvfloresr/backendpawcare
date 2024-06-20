class Roles:
    def __init__(self, id=None, role_name=None, description=None, status_view=None):
        self.id = id
        self.role_name = role_name
        self.description = description
        self.status_view = status_view

    def __repr__(self):
        return f"Roles(id={self.id}, role_name='{self.role_name}', description='{self.description}', status_view='{self.status_view}')"
