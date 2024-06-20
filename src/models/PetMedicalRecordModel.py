class PetMedicalRecord:
    def __init__(self, id, pet_id, doctor_id, date, treatment, diagnosis, notes, status_petmedical, status_view=None) -> None:
        self.id = id
        self.pet_id = pet_id
        self.doctor_id = doctor_id
        self.date = date
        self.treatment = treatment
        self.diagnosis = diagnosis
        self.notes = notes
        self.status_petmedical = status_petmedical
        self.status_view = status_view

    def __repr__(self):
        return (f"PetMedicalRecord(id={self.id}, pet_id={self.pet_id}, doctor_id={self.doctor_id}, "
                f"date='{self.date}', treatment='{self.treatment}', diagnosis='{self.diagnosis}', "
                f"notes='{self.notes}', status_petmedical='{self.status_petmedical}' status_view='{self.status_view}')")
