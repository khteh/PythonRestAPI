import pytest, logging, os, re
from re import Match
"""
$ pipenv run python -m test.value_reference_test

Python uses a mechanism often described as "pass-by-object-reference," which can be a bit confusing. Here's a breakdown:
How it Works:
Everything is an Object:
In Python, everything, including integers, strings, lists, and custom objects, is an object. Variables hold references (pointers) to these objects in memory.
Pass by Value of the Reference:
When you pass a variable to a function, Python passes the value of the reference to the object. It's not passing the object itself, but a copy of the reference.
Mutable vs. Immutable Objects:
Mutable Objects: If the object is mutable (like a list or dictionary), the function can modify the object through the passed reference. Both the function and the caller have references to the same object, so changes made inside the function will be visible outside.
Immutable Objects: If the object is immutable (like a number, string, or tuple), any attempt to modify it creates a new object. The original object is unchanged, and the function's variable will point to the new object.
Key Points:
Not Pass by Reference:
Python does not pass by reference in the traditional sense, where changes to the parameter variable directly affect the original variable.
Not Pure Pass by Value:
It's not pure pass by value because the reference itself is passed, allowing modifications to mutable objects.
Pass by Assignment:
Some call it pass by assignment because the reference is assigned to a local variable.
The Illusion of Pass by Reference:
For mutable objects, it might seem like pass by reference because changes inside the function persist outside, but it's actually because both the function and the caller share a reference to the same object in memory.
Example:
Python

def modify_list(my_list):
    my_list.append(4)  # Modifies the original list

def reassign_list(my_list):
    my_list = [5, 6, 7]  # Creates a new list, does not affect original

original_list = [1, 2, 3]
modify_list(original_list)
print(original_list)  # Output: [1, 2, 3, 4]

reassign_list(original_list)
print(original_list)  # Output: [1, 2, 3, 4] (still the modified list)
In the example, modify_list changes the original list because it's using the reference to the same object. reassign_list, however, creates a new list and reassigns its local variable, leaving the original unchanged.
"""
i:float = 123.456

def modify_input_integral(j:float):
    print(f"j: {id(j)}, {j}")
    assert id(i) == id(j)
    assert i == j
    j = 456.789
    print(f"j: {id(j)}, {j}")
    assert id(i) != id(j)
    assert i != j

print(f"i: {id(i)}, {i}")
modify_input_integral(i)