class Species:
    def __init__(self, id, name, description=None, status_view=None) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.status_view = status_view

    def __repr__(self):
        return f"Species(id={self.id}, name='{self.name}', description='{self.description}', status_view='{self.status_view}')"
