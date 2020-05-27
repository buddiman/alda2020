###################################
#   Christopher Höllriegl, Marvin Schmitt
#   Blatt 3 Aufgabe 2
#   Mittwoch 14 Uhr, Felix Lübbe
###################################

###################################
# Aufgabe 2a
#
# Bei _test wird eine Methode getestet bzw. ausgeführt
# _check überprüft Daten, ob diese korrekt sind, ohne zu testende Methoden auszuführen.
#
# Fixtures werden benutzt, um die Testumgebung (meistens garantiert gleiche Daten) einzurichten. So kann eine Fixture für mehrere Testmethoden benutzt werden und man spart sich doppelten Code (-> Redundanz).
#
# Warum benutzt man Fixtures:
#   gleiche Daten für mehrere Tests
#   gleiche Daten für einen Test der mehrmals wiederholt wird
#   dadurch Redundanz -> Weniger Code
###################################

###################################
# Aufgabe 2f    Zeile: 77   die Werte müssen gegen <= verglichen werden, sonst werden gleiche Werte nicht richtig einsortiert.
#                           mit <= bleiben gleiche Elemente in der Reihenfolge, in der sie ursprünglich waren.
###################################


import pytest
from pytest import raises
from random import randint
from collections import Counter


class Student:
    def __init__(self, name, mark):
        '''Construct new Student object with given 'name' and 'mark'.'''
        self._name = name
        self._mark = mark

    def get_name(self):
        '''Access the name.'''
        return self._name

    def get_mark(self):
        '''Access the mark.'''
        return self._mark

    def __repr__(self):
        '''Convert Student object to a string.'''
        return "%s: %3.1f" % (self._name, self._mark)

    def __eq__(self, other):
        '''Check if two Student objects are equal.'''
        return self._name == other._name and self._mark == other._mark

##################################################################

def insertion_sort_1(a, key=lambda x: x):
    '''
    Sort the array 'a' in-place.

    Parameter 'key' must hold a function that, given a complicated
    object, extracts the property to sort by. By default, this
    is the object itself (useful to sort integers). To sort Students
    by name, you call:
        insertion_sort_1(students, key=Student.get_name)
    whereas to sort by mark, you use
        insertion_sort_1(students, key=Student.get_mark)
    This corresponds to the behavior of Python's built-in sorting functions.
    
    NOTE: THIS IMPLEMENTATION INTENTIONALLY CONTAINS A BUG, 
    WHICH YOUR TESTS ARE SUPPOSED TO DETECT.
    '''
    for i in range(1, len(a)):
        current = a[i]
        j = i
        while j > 0:
            if key(a[j-1]) < key(current):      # Note: Fehler hier!
                break
            else:
                a[j] = a[j-1]
            j -= 1
        a[j] = current


def insertion_sort(a, key=lambda x: x):
    '''
    Sort the array 'a' in-place.

    Parameter 'key' must hold a function that, given a complicated
    object, extracts the property to sort by. By default, this
    is the object itself (useful to sort integers). To sort Students
    by name, you call:
        insertion_sort_1(students, key=Student.get_name)
    whereas to sort by mark, you use
        insertion_sort_1(students, key=Student.get_mark)
    This corresponds to the behavior of Python's built-in sorting functions.

    NOTE: THIS IMPLEMENTATION INTENTIONALLY CONTAINS A BUG,
    WHICH YOUR TESTS ARE SUPPOSED TO DETECT.
    '''
    for i in range(1, len(a)):
        current = a[i]
        j = i
        while j > 0:
            if key(a[j - 1]) <= key(current):
                break
            else:
                a[j] = a[j - 1]
            j -= 1
        a[j] = current

##################################################################
# mergeSort from AlDa Wiki, modified for key
def merge(left, right, key=lambda x: x):
    res = []
    i, j = 0, 0

    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
             res.append(left[i])
             i += 1
        else:
             res.append(right[j])
             j += 1

    while i < len(left):
       res.append(left[i])
       i += 1

    while j < len(right):
       res.append(right[j])
       j += 1

    return res

def mergeSort(a, key=lambda x: x):
    N = len(a)
    if N <= 1:
        return a
    else:
        left  = a[0:N//2]

        right = a[N//2:N]
        leftSorted  = mergeSort(left, key)
        rightSorted = mergeSort(right, key)
        return merge(leftSorted, rightSorted, key)

##################################################################

@pytest.fixture
def arrays():
    '''Create a dictionary holding test data.'''

    data = dict()
    
    # integer arrays
    data['int_arrays'] = [
        [],           # empty array
        [1],          # one element
        [2,1],        # two elements
        [3,2,3,1],    # the array from the exercise text
        [randint(0, 4) for k in range(10)], # 10 random ints
        [randint(0, 4) for k in range(10)]  # another 10 random ints
    ]

    # Student arrays
    data['student_arrays'] = [
       [Student('Adam', 1.3),
        Student('Bert', 2.0),
        Student('Elsa', 1.0),
        Student('Greg', 1.7),
        Student('Jill', 2.7),
        Student('Judy', 3.0),
        Student('Mike', 2.3),
        Student('Patt', 5.0)], # without replicated marks

       [Student('Adam', 1.3),
        Student('Bert', 2.0),
        Student('Elsa', 1.3),
        Student('Greg', 1.0),
        Student('Jill', 1.7),
        Student('Judy', 1.0),
        Student('Mike', 2.3),
        Student('Patt', 1.3)], # with replicated marks, alphabetic

       [Student('Bert', 2.0),
        Student('Mike', 2.3),
        Student('Elsa', 1.3),
        Student('Judy', 1.0),
        Student('Patt', 2.0),
        Student('Greg', 1.0),
        Student('Jill', 1.7),
        Student('Adam', 1.3)] # with replicated marks, random order
    ]
    
    return data

##################################################################

@pytest.mark.xfail
def test_checks():
    # test that the check_ functions actually find the desired errors
    # expecting to fail

    # check_integer_sorting, Aufgabe b
    # Be careful, because the first check fails the others don't get tested. Tried with out-commenting
    check_integer_sorting([1, 2, 3], [1, 2, 3, 4])      # length error
    check_integer_sorting([1, 2, 3, 4], [1, 3, 2, 4])   # sort error
    check_integer_sorting([1, 2, 3, 3, 4, 5], [1, 2, 2, 3, 4, 5])   # same elements error
    return


def test_builtin_sort(arrays):

    # test the integer arrays
    for original in arrays['int_arrays']:
        original_copy = list(original)  # make sure to temp copy the original list to compare
        check_integer_sorting(original_copy,
                              sorted(original))  # sorted() as parameter, because it returns the sorted list

    # test the Student arrays
    for original in arrays['student_arrays']:
        original_copy = list(original)  # make sure to temp copy the original list to compare
        check_student_sorting(original_copy, sorted(original, key=Student.get_name), key=Student.get_name)
        check_student_sorting(original_copy, sorted(original, key=Student.get_mark), key=Student.get_mark)


def test_insertion_sort(arrays):
    # test the integer arrays
    for original in arrays['int_arrays']:
        original_copy = list(original)  # make sure to temp copy the original list to compare
        insertion_sort_1(original)
        check_integer_sorting(original_copy, original)

    # test the Student arrays
    for original in arrays['student_arrays']:
        original_copy = list(original)  # make sure to temp copy the original list to compare

        insertion_sort_1(original, key=Student.get_name)
        check_student_sorting(original, original, key=Student.get_name)

        insertion_sort_1(original_copy, key=Student.get_mark)   # make the copy before name sorting... lmao

        with pytest.raises(AssertionError):
            check_student_sorting(original_copy, original, key=Student.get_mark)

    # test the Student arrays with correct insertion sort
    for original in arrays['student_arrays']:
        original_copy = list(original)  # make sure to temp copy the original list to compare
        original_copy_2 = list(original)

        insertion_sort(original, key=Student.get_name)
        check_student_sorting(original_copy, original, key=Student.get_name)

        insertion_sort(original_copy_2, key=Student.get_mark)
        check_student_sorting(original_copy, original_copy_2, key=Student.get_mark)


def test_merge_sort(arrays):
    for original in arrays['int_arrays']:
        original_copy = list(original)  # make sure to temp copy the original list to compare
        check_integer_sorting(original_copy, mergeSort(original))

    for original in arrays['student_arrays']:
        original_copy = list(original)  # make sure to temp copy the original list to compare
        original_copy_2 = list(original)
        check_student_sorting(original_copy, mergeSort(original, key=Student.get_name), key=Student.get_name)
        check_student_sorting(original_copy, mergeSort(original_copy_2, key=Student.get_mark), key=Student.get_mark)


def check_integer_sorting(original, result):
    '''Parameter 'original' contains the array before sorting,
    parameter 'result' contains the output of the sorting algorithm.'''

    assert len(result) == len(original), "E: different size found"     # assert same size/length

    # assert list is sorted
    flag_sorted = 1
    i = 1
    while i < len(result):
        if (result[i] < result[i - 1]):
            flag_sorted = 0
        i += 1
    assert flag_sorted, "E: result is not sorted"

    # assert same elements (should work this way with duplicates)
    assert Counter(result) == Counter(original), "E: result and original do not contain the same elements"


def check_student_sorting(original, result, key=lambda x: x):
    '''Parameter 'original' contains the array before sorting,
    parameter 'result' contains the output of the sorting algorithm.
    'key' is the attribute defining the order.
    '''
    assert len(result) == len(original), "E: different size found"  # assert same size/length. Wasn't necessary

    # Better name for the function: I don't like Lambda
    for j in range(len(result) - 1):
        assert key(result[j]) <= key(result[j+1]), "E: result is not sorted correctly"
        # check for stable
        if key(result[j]) == key(result[j+1]):
            # compare original elem position
            if not (original.index(result[j]) < original.index(result[j + 1])):
                raise AssertionError("E: sorted data is not stable")
