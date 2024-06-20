class Hospitalization:
    def __init__(self, id, pet_id, start_date, end_date, reason, observations, status_hospitalization, status_view=None) -> None:
        self.id = id
        self.pet_id = pet_id
        self.start_date = start_date
        self.end_date = end_date
        self.reason = reason
        self.observations = observations
        self.status_hospitalization = status_hospitalization
        self.status_view = status_view

    def __repr__(self):
        return (f"Hospitalization(id={self.id}, pet_id={self.pet_id}, "
                f"start_date={self.start_date}, end_date={self.end_date}, "
                f"reason='{self.reason}', observations='{self.observations}', "
                f"status_hospitalization='{self.status_hospitalization}', status_view='{self.status_view}')")
