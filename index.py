from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

from flask_cors import CORS

from src.routes.UsersRoutes import auth_blueprint
from src.routes.PetsRoutes import pets_blueprint
from src.routes.DoctorsRoutes import doctors_blueprint
from src.routes.SpecialtiesRoutes import specialties_blueprint
from src.routes.RolesRoutes import roles_blueprint
from src.routes.SpeciesRoutes import species_blueprint
from src.routes.AppointmentsRoutes import appointments_blueprint
from src.routes.CategoryQuotesRoutes import category_quotes_blueprint
from src.routes.HospitalizationsRoutes import hospitalization_blueprint
from src.routes.PetMedicalRecordRoutes import medical_records_blueprint
from src.routes.PaymentsRoutes import payment_blueprint

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

jwt = JWTManager(app)


#Users
app.register_blueprint(auth_blueprint, url_prefix='/auth')
#Pets
app.register_blueprint(pets_blueprint, url_prefix='/pets')
#Doctors
app.register_blueprint(doctors_blueprint, url_prefix='/doctors')
#Specialties
app.register_blueprint(specialties_blueprint, url_prefix='/specialties')
#Roles
app.register_blueprint(roles_blueprint, url_prefix= '/roles')
#Species
app.register_blueprint(species_blueprint, url_prefix= '/species')
#Appointments
app.register_blueprint(appointments_blueprint, url_prefix= '/appointments')
#CategoryQuotes
app.register_blueprint(category_quotes_blueprint, url_prefix= '/categoryquotes')
#Hospitalizations
app.register_blueprint(hospitalization_blueprint, url_prefix= '/hospitalization')
#PetMedical
app.register_blueprint(medical_records_blueprint, url_prefix= '/medicalrecord')
#Payment
app.register_blueprint(payment_blueprint, url_prefix= '/payment' )

@app.route('/')
def home():
    return "Bienvenido a mi API de veterinaria!"

if __name__ == '__main__':
    app.run(debug=True)

