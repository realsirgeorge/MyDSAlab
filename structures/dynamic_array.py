"""
Skeleton for COMP3506/7505 A1, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""

from typing import Any


class DynamicArray:
    def __init__(self) -> None:
        self._capacity = 1  # Initial capacity of the dynamic array
        self._size = 0       # Number of elements currently in the array
        self._data = self._make_array(self._capacity)
        self._start = 0  # Start index of the buffer
        self._start_index = 0  # Points to the start of valid data in the array
        self._reversed = False  # Flag to indicate if the array is reversed


        

    def __str__(self) -> str:
        """
        A helper that allows you to print a DynamicArray type
        via the str() method.
        """
        result = "["
        for i in range(self._size):
            result += str(self._data[i])
            if i < self._size - 1:
                result += ", "
        result += "]"
        return result

    def __resize(self, new_capacity) -> None:
        new_data = self._make_array(new_capacity)
        for i in range(self._size):
            new_data[i] = self._data[(self._start_index + i) % self._capacity]
        self._data = new_data
        self._capacity = new_capacity
        self._start_index = 0

    def get_at(self, index: int) -> Any | None:
        """
        Get element at the given index.
        Return None if index is out of bounds.
        Time complexity for full marks: O(1)
        """
        if 0 <= index < self._size:
            if self._reversed:
                return self._data[(self._start_index + self._size - 1 - index) % self._capacity]
            else:
                return self._data[(self._start_index + index) % self._capacity]
        return None

    def __getitem__(self, index: int) -> Any | None:
        """
        Same as get_at.
        Allows to use square brackets to index elements.
        """
        return self.get_at(index)

    def set_at(self, index: int, element: Any) -> None:
        """
        Get element at the given index.
        Do not modify the list if the index is out of bounds.
        Time complexity for full marks: O(1)
        """
        if 0 <= index < self._size:
            if self._reversed:
                self._data[(self._start_index + self._size - 1 - index) % self._capacity] = element
            else:
                self._data[(self._start_index + index) % self._capacity] = element


    def __setitem__(self, index: int, element: Any) -> None:
        """
        Same as set_at.
        Allows to use square brackets to index elements.
        """
        self.set_at(index, element)

    def append(self, element: Any) -> None:
        """
        Add an element to the back of the array.
        Time complexity for full marks: O(1*) (* means amortized)
        """
        if self._size == self._capacity:
            self.__resize(2 * self._capacity)
        if self._reversed:
            self._start_index = (self._start_index - 1) % self._capacity
            self._data[self._start_index] = element
        else:
            self._data[(self._start_index + self._size) % self._capacity] = element
        self._size += 1

    def prepend(self, element: Any) -> None:
        """
        Add an element to the front of the array.
        Time complexity for full marks: O(1*)
        """
        if self._size == self._capacity:
            self.__resize(2 * self._capacity)
        if self._reversed:
            self._data[(self._start_index + self._size) % self._capacity] = element
        else:
            self._start_index = (self._start_index - 1) % self._capacity
            self._data[self._start_index] = element
        self._size += 1


    def reverse(self) -> None:
        """
        Reverse the array.
        Time complexity for full marks: O(1)
        """
        self._reversed = not self._reversed


    def remove(self, element: Any) -> None:
        """
        Remove the first occurrence of the element from the array.
        If there is no such element, leave the array unchanged.
        Time complexity for full marks: O(N)
        """
        for i in range(self._size):
            if self._data[i] == element:
                # Shift elements to the left to fill the gap
                for j in range(i, self._size - 1):
                    self._data[j] = self._data[j + 1]
                self._data[self._size - 1] = None  # Remove reference
                self._size -= 1
                break

    def remove_at(self, index: int) -> Any | None:
        """
        Remove the element at the given index from the array and return the removed element.
        If there is no such element, leave the array unchanged and return None.
        Time complexity for full marks: O(N)
        """
        if 0 <= index < self._size:
            removed_element = self._data[index]
            # Shift elements to the left to fill the gap
            for i in range(index, self._size - 1):
                self._data[i] = self._data[i + 1]
            self._data[self._size - 1] = None  # Remove reference
            self._size -= 1
            return removed_element
        return None

    def is_empty(self) -> bool:
        """
        Boolean helper to tell us if the structure is empty or not
        Time complexity for full marks: O(1)
        """
        return self._size == 0

    def is_full(self) -> bool:
        """
        Boolean helper to tell us if the structure is full or not
        Time complexity for full marks: O(1)
        """
        return self._size == self._capacity

    def get_size(self) -> int:
        """
        Return the number of elements in the list
        Time complexity for full marks: O(1)
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the total capacity (the number of slots) of the list
        Time complexity for full marks: O(1)
        """
        return self._capacity

    def sort(self) -> None:
        """
        Sort elements inside _data based on < comparisons.
        Time complexity for full marks: O(NlogN)
        """
        if self._size > 1:
            self._merge_sort(0, self._size - 1)

    def _merge_sort(self, left: int, right: int) -> None:
        if left < right:
            middle = (left + right) // 2
            self._merge_sort(left, middle)
            self._merge_sort(middle + 1, right)
            self._merge(left, middle, right)

    def _merge(self, left: int, middle: int, right: int) -> None:
        # Create temporary arrays
        left_half = self._data[left:middle + 1]
        right_half = self._data[middle + 1:right + 1]

        i = j = 0
        k = left

        # Merge the temp arrays back into the original array
        while i < len(left_half) and j < len(right_half):
            if left_half[i] <= right_half[j]:
                self._data[k] = left_half[i]
                i += 1
            else:
                self._data[k] = right_half[j]
                j += 1
            k += 1

        # Copy the remaining elements of left_half, if any
        while i < len(left_half):
            self._data[k] = left_half[i]
            i += 1
            k += 1

        # Copy the remaining elements of right_half, if any
        while j < len(right_half):
            self._data[k] = right_half[j]
            j += 1
            k += 1
    def _make_array(self, capacity):
        # Returns a new array with the given capacity
        return [0] * capacity