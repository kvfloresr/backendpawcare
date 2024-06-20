class Appointment:
    def __init__(self, id, user_id, pet_id, doctor_id, date, time, description, status_appointments, category_id, status_view=None) -> None:
        self.id = id
        self.user_id = user_id
        self.pet_id = pet_id
        self.doctor_id = doctor_id
        self.date = date
        self.time = time
        self.description = description
        self.status_appointments = status_appointments
        self.category_id = category_id
        self.status_view = status_view

    def __repr__(self):
        return (f"Appointment(id={self.id}, user_id={self.user_id}, pet_id={self.pet_id}, "
                f"doctor_id={self.doctor_id}, date={self.date}, time={self.time}, "
                f"description='{self.description}', status_appointments='{self.status_appointments}', "
                f"category_id={self.category_id}, status_view='{self.status_view}')")
