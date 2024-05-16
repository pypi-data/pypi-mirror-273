from typing import Any, Self

class Break(Exception):
    """Custom exception to signal a break from the Switch context."""
    pass

class Switch:
    def __init__(self, value):
        self.value = value
        self.is_match = False

        self._default = False

    def case(self, condition) -> bool:
        '''
        Executes condition, if True sets is_match to True
        if is_match is True then allows for multiple cases to be executed

        @parameter condition: conditional statement that returns True or False
        '''
        if condition or self.is_match:
            self.is_match = True
            return True
        return False
    
    @property
    def default(self) -> bool:
        '''Only runs if no match has been found'''
        return not self.is_match

    def __enter__(self) -> Self:
        '''Establish Switch context'''
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Exit Switch context'''
        if exc_type is Break:
            return True
        return False


if __name__ == '__main__':
    with Switch(1) as s:
        if s.case(s.value == 1):
            pass
        if s.case(s.value == 2):
            pass
        if s.case(s.value == 3):
            print("1, 2, 3!!")
            raise Break()  # Exit the Switch context
        if s.case(s.value == 4):
            print("Won't see this... :(")
        if s.default:
            print('default')
