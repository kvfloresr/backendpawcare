class CategoryQuote:
    def __init__(self, id, category_name, status_view=None) -> None:
        self.id = id
        self.category_name = category_name
        self.status_view = status_view

    def __repr__(self):
        return f"CategoryQuote(id={self.id}, category_name='{self.category_name}', status_view='{self.status_view}')"
