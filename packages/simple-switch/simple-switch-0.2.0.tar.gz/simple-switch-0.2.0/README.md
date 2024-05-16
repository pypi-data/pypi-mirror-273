# Switch

## Introduction

Switch is a Python library that provides a simple and flexible switch statement implementation. It allows you to write cleaner and more readable code by eliminating the need for long chains of if-else statements.

## Usage
The switch library provides a Switch class that can be used to create switch statements. The Switch class takes a value as an argument, which is the value to be compared against the cases.

The case method takes a condition as an argument. If the condition evaluates to True, the corresponding function is executed. The default method is executed if no match is found.

### Here is an example of how to use the Switch class:
```rb
from switch import Switch

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
```

## Features:
  - Simple and intuitive syntax
  - Flexible conditions
  - Support for multiple cases
  - Default case handling
  - Exception handling for breaking out of the switch statement
  
## Benefits:
  - Improved code readability
  - Reduced code complexity
  - Easier to maintain and debug
  
## Conclusion:
The switch library is a valuable tool for any Python developer who wants to write cleaner and more readable code. It is a simple and flexible way to implement switch statements in Python.
