import random

from .employee_role import EmployeeRole
from .healthcare_professional import HealthcareProfessional
from .patient import Patient

class Nurse(HealthcareProfessional):
    """
    Models a nurse
    """
    def __init__(self, name:str, employee_number:str):
        """creates the instance
        
        Args:
            name: employee's name
            employee_number: employee's number
        Returns:
            None
        """
        super().__init__(name, employee_number, EmployeeRole.NURSE)

    # results of the consultation
    _consultation_results = [
        'Medical history and symptoms of {} were recorded',
        'Planned patient care for {}',
        'Gave advice to {} about health and wellbeing',
        'Health and record signs of {} were recorded',
        'Medications and treatments were administered to {}',
        'Medical procedure performed on {}',
        'Diagnostic tests were performed on {}',
        'Gave instructions about management of illnesses to {}',
        'Provided support and advice to {}'
    ]

    def consultation(self, patient:Patient) -> str:
        """performs a consultation
        
        Args:
            patient: Patient
        Returns:
            consultation result
        """
        return self._consultation_results[random.randint(0, len(self._consultation_results)-1)].format(patient.firstname+' '+patient.surname)
    