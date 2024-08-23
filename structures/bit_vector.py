"""
Skeleton for COMP3506/7505 A1, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""
from typing import Any
from structures.dynamic_array import DynamicArray
class BitVector:
    """
    A compact storage for bits that uses DynamicArray under the hood.
    Each element stores up to 64 bits, making BitVector 64 times more memory-efficient
    for storing bits than plain DynamicArray.
    """
    BITS_PER_ELEMENT = 64

    def __init__(self) -> None:
        """
        We will use the dynamic array as our data storage mechanism
        """
        self._data = DynamicArray()
        self._size = 0  # Total number of bits in the vector
        self._start_index = 0  # Initialize the start index for logical indexing
        self._flipped = False  # Flag to indicate if the bits are logically flipped
        self._reversed = False  # Flag to indicate if the vector is logically reversed

    def __str__(self) -> str:
        """
        A helper that allows you to print a BitVector type
        via the str() method.
        """
        result = ""
        for i in range(self._size):
            result += "1" if self.get_at(i) else "0"
        return result

    def __resize(self) -> None:
        pass

    def _ensure_capacity(self, index: int):
        """Ensure the bit vector has enough capacity to handle the given index."""
        required_size = (index // self.BITS_PER_ELEMENT) + 1
        while self._data.get_size() < required_size:
            self._data.append(0)  # Initialize with 0 to avoid NoneType errors
    
    def get_at(self, index: int) -> int | None:
        """
        Get bit at the given index.
        Return None if index is out of bounds.
        Time complexity for full marks: O(1)
        """
        if index < 0 or index >= self._size:
            return None
        # Adjust the index based on whether the vector is reversed
        if self._reversed:
            index = self._size - 1 - index
        # Calculate the logical index taking the start index into account
        logical_index = (self._start_index + index) % (self.BITS_PER_ELEMENT * self._data.get_size())
        element_index = logical_index // self.BITS_PER_ELEMENT
        bit_index = logical_index % self.BITS_PER_ELEMENT
        bit_value = (self._data[element_index] >> bit_index) & 1
        # If the vector is logically flipped, invert the bit value
        return bit_value ^ self._flipped

    def __getitem__(self, index: int) -> int | None:
        """
        Same as get_at.
        Allows to use square brackets to index elements.
        """
        return self.get_at(index)

    def set_at(self, index: int) -> None:
        """
        Set bit at the given index to 1.
        Do not modify the vector if the index is out of bounds.
        Time complexity for full marks: O(1)
        """
        if index < 0:
            return
        self._ensure_capacity(index)

        # Adjust the index based on whether the vector is reversed
        if self._reversed:
            index = self._size - 1 - index

        logical_index = (self._start_index + index) % (self.BITS_PER_ELEMENT * self._data.get_size())
        element_index = logical_index // self.BITS_PER_ELEMENT
        bit_index = logical_index % self.BITS_PER_ELEMENT

        if self._flipped:
            # If the vector is logically flipped, we need to clear the bit
            self._data[element_index] &= ~(1 << bit_index)
        else:
            # Normal operation: set the bit
            self._data[element_index] |= (1 << bit_index)

    def unset_at(self, index: int) -> None:
        """
        Set bit at the given index to 0.
        Do not modify the vector if the index is out of bounds.
        Time complexity for full marks: O(1)
        """
        if index < 0 or index >= self._size:
            return

        # Adjust the index based on whether the vector is reversed
        if self._reversed:
            index = self._size - 1 - index
        logical_index = (self._start_index + index) % (self.BITS_PER_ELEMENT * self._data.get_size())
        element_index = logical_index // self.BITS_PER_ELEMENT
        bit_index = logical_index % self.BITS_PER_ELEMENT
        if self._flipped:
            # If the vector is logically flipped, we need to set the bit
            self._data[element_index] |= (1 << bit_index)
        else:
            # Normal operation: clear the bit
            self._data[element_index] &= ~(1 << bit_index)

    def __setitem__(self, index: int, state: int) -> None:
        """
        Set bit at the given index.
        Treat the integer in the same way Python does:
        if state is 0, set the bit to 0, otherwise set the bit to 1.
        Do not modify the vector if the index is out of bounds.
        Time complexity for full marks: O(1)
        """
        if state == 0:
            self.unset_at(index)
        else:
            self.set_at(index)

    def append(self, state: int) -> None:
        """
        Add a bit to the back of the vector.
        Treat the integer in the same way Python does:
        if state is 0, set the bit to 0, otherwise set the bit to 1.
        Time complexity for full marks: O(1*)
        """
        if self._size % self.BITS_PER_ELEMENT == 0:
            self._data.append(0)
        self._size += 1
        self.__setitem__(self._size - 1, state)

    def prepend(self, state: Any) -> None:
        """
        Add a bit to the front of the vector.
        Treat the integer in the same way Python does:
        if state is 0, set the bit to 0, otherwise set the bit to 1.
        Time complexity for full marks: O(1*)
        """
        # Increase size of the bit vector
        self._size += 1
        # Ensure the bit vector has enough capacity
        self._ensure_capacity(self._size - 1)
        # Adjust the logical start position by moving it left
        # If _start_index goes below 0, wrap it around using modulo operation
        self._start_index = (self._start_index - 1) % (self.BITS_PER_ELEMENT * self._data.get_size())
        # Set the first element in the logical bit vector to the new state
        self.__setitem__(0, state)

    def reverse(self) -> None:
        """
        Reverse the bit-vector.
        Time complexity for full marks: O(1)
        """
        self._reversed = not self._reversed

    def flip_all_bits(self) -> None:
        """
        Flip all bits in the vector.
        Time complexity for full marks: O(1)
        """
        self._flipped = not self._flipped

    def shift(self, dist: int) -> None:
        """
        Make a bit shift.
        If dist is positive, perform a left shift by `dist`.
        Otherwise perform a right shift by `dist`.
        Time complexity for full marks: O(N)
        """
        if dist == 0:
            return

        if dist > 0:  # Left shift
            for i in range(self._size):
                if i + dist < self._size:
                    self.__setitem__(i, self.get_at(i + dist))
                else:
                    self.__setitem__(i, 0)  # Fill with 0s

        else:  # Right shift
            dist = abs(dist)
            for i in range(self._size - 1, -1, -1):
                if i - dist >= 0:
                    self.__setitem__(i, self.get_at(i - dist))
                else:
                    self.__setitem__(i, 0)  # Fill with 0s

    def rotate(self, dist: int) -> None:
        """
        Make a bit rotation.
        If dist is positive, perform a left rotation by `dist`.
        Otherwise perform a right rotation by `dist`.
        Time complexity for full marks: O(N)
        """
        if self._size == 0 or abs(dist) % self._size == 0:
            return  # No need to rotate if the distance is zero or a multiple of size

        dist = dist % self._size  # Normalize the distance to within the size of the vector
        if dist < 0:
            dist += self._size  # Convert negative rotations to positive equivalent

        def get_bit_vector() -> str:
            return ''.join(str(self.get_at(i)) for i in range(self._size))

        # Perform the rotation by shifting twice: once for the initial rotation, and once to correct the remaining bits
        rotated_bits = [self.get_at((i - dist) % self._size) for i in range(self._size)]
        
        for i in range(self._size):
            self.__setitem__(i, rotated_bits[i])

    def get_size(self) -> int:
        """
        Return the number of *bits* in the list
        Time complexity for full marks: O(1)
        """
        return self._size
