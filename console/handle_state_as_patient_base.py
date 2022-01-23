from abc import ABC
from datetime import datetime
import time
from healthcare import appointment

from healthcare.patient import Patient
from healthcare.clinic import Clinic
from console.state import State
from healthcare.receptionist import Receptionist

from .console_utility import ConsoleUtility
from .handle_state import StateHandler

class StateAsPatientBaseHandler(StateHandler, ABC):

    def __init__(self, quick:bool=False):
        self._quick = quick

    def _register_new_patient(self, clinic:Clinic, receptionist:Receptionist, name = None, surname = None, patient:Patient=None):
        if patient is None:
            patient = self._identify_user(name, surname)
        else:
            # handle prefilled configuration
            ConsoleUtility.print_conversation('Do you have an id?') 
            self._pause()
            ConsoleUtility.print_light('Here it is!')
            self._pause()
            ConsoleUtility.print_conversation('I see... {}'.format(patient))
            self._pause()
        receptionist.register_patient(clinic, patient)
        ConsoleUtility.print_conversation('Thank you, now you are one of our patients')
        return patient

    def _default_or_input(self, default):
        if default is None:
            return ConsoleUtility.prompt_user_for_input()
        else:
            ConsoleUtility.print_light(default)
            return default

    def _identify_user(self, name=None, surname=None):
        ConsoleUtility.print_conversation('Can I have your surname, please?')
        if surname is None:
            surname = ConsoleUtility.prompt_user_for_input()
        else:
            ConsoleUtility.print_light(surname)
        ConsoleUtility.print_conversation('...and your first name?')
        if name is None :
            name = ConsoleUtility.prompt_user_for_input()
        else:
            ConsoleUtility.print_light(name)
        ConsoleUtility.print_conversation('What is your address?')
        address = ConsoleUtility.prompt_user_for_input()
        ConsoleUtility.print_conversation('What is your phone number?')
        # TODO validation
        phone = ConsoleUtility.prompt_user_for_input()
        return Patient(name, surname, address, phone)

    def _make_an_appointment(self, clinic:Clinic, receptionist:Receptionist, user:Patient, surname = None, name = None):
        if user is None:
            if surname is None:
                ConsoleUtility.print_conversation('Can I have your surname, please?')
                surname = ConsoleUtility.prompt_user_for_input()
            if name is None:
                ConsoleUtility.print_conversation('Can I have your first name, please?')
                name = ConsoleUtility.prompt_user_for_input()
        else:
            # handle prefilled configuration
            ConsoleUtility.print_conversation('Do you have an id?') 
            self._pause()
            ConsoleUtility.print_light('Here my id')
            self._pause()
            ConsoleUtility.print_conversation('I see... {}'.format(user))
            self._pause()
            name = user.firstname
            surname = user.surname
        patient = receptionist.lookup_patient(clinic, name, surname)
        if patient == None:
            ConsoleUtility.print_conversation('You are not yet in the system, I need to register you as a patient')
            patient = self._register_new_patient(clinic, receptionist, name, surname)
        ConsoleUtility.print_conversation('With whom do you need an appointment?')
        index = 0
        options = []
        for doctor in clinic.doctors:
            options.append(doctor)
            ConsoleUtility.print_option('[{}] Doctor {}'.format(index +1, doctor.name))
            index = index + 1
        for nurse in clinic.nurses:
            options.append(nurse)
            ConsoleUtility.print_option('[{}] Nurse {}'.format(index + 1, nurse.name))
            index = index + 1
        staff = options[int(ConsoleUtility.prompt_user_for_input(validation = lambda i: int(i)>0 and int(i)<=index)) - 1]
        ConsoleUtility.print_conversation('Is it urgent?')
        ConsoleUtility.print_option('[Y]es')
        ConsoleUtility.print_option('[N]o')
        urgent = ConsoleUtility.prompt_user_for_input(['Y', 'N']) == 'Y'
        accepted = False
        next_timeslot = datetime.now()
        while not accepted:
            next_timeslot = receptionist.find_next_free_timeslot(clinic.appointment_schedule, staff, urgent, next_timeslot)
            ConsoleUtility.print_conversation('{} would be ok for you?'.format(next_timeslot))
            ConsoleUtility.print_option('[Y]es')
            ConsoleUtility.print_option('[N]o')
            accepted = ConsoleUtility.prompt_user_for_input(['Y', 'N']) == 'Y'
        receptionist.make_appointment(clinic.appointment_schedule, staff, patient, next_timeslot, urgent)
        ConsoleUtility.print_conversation('Thank you, the appointment has been registered')

    def _cancel_an_appointment(self, clinic:Clinic, receptionist:Receptionist, patient:Patient):
        appointments = self._print_appointments(clinic, receptionist, patient)
        ConsoleUtility.print_conversation('Which one do you want to cancel?')
        input = ConsoleUtility.prompt_user_for_input(options = range(1, len(appointments)))
        appointment = appointments[int(input)-1]
        receptionist.cancel_appointment(clinic.appointment_schedule, appointment)
        ConsoleUtility.print_conversation('The appointment {} has been cancelled'.format(appointment))

    def _find_next_appointment(self, clinic:Clinic, receptionist:Receptionist, patient:Patient):
        receptionist.find_patient_appointments(clinic.appointment_schedule, patient)

    def _print_appointments(self, clinic, receptionist, patient):
        appointments = receptionist.find_patient_appointments(clinic.appointment_schedule, patient)
        ConsoleUtility.print_conversation('Currently, you have {} appointment{}'.format(len(appointments),'s' if len(appointments)>1 else ''))
        for idx, appointment in enumerate(appointments):
            ConsoleUtility.print_light('{} with {}'.format(idx+1, appointment.date, appointment.staff))
        return appointments

    def _pause(self):
        time.sleep(0.5 if self._quick else 1.5)
