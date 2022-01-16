from abc import ABC, abstractmethod

from healthcare.state import State
from .clinic import Clinic
from .console_utility import ConsoleUtility

class StateFireStaff(ABC):
    
    def __init__(self, next_state:State, type):
        self._next_state = next_state
        self._type = type

    def handle(self, clinic:Clinic):
        ConsoleUtility.print_option('Please insert employee number')
        employee_number = ConsoleUtility.prompt_user_for_input()
        fired, message = clinic.fire(employee_number, self._type)
        if not fired:
            ConsoleUtility.print_error('There was an error: {}'.format(message))
        return self._next_state
