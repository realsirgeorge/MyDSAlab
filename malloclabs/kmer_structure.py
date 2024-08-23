"""
Skeleton for COMP3506/7505 A1, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

MallocLabs K-mer Querying Structure
"""

from typing import Any

"""
You may wish to import your data structures to help you with some of the
problems. Or maybe not.
"""
#from structures.bit_vector import BitVector
from structures.dynamic_array import DynamicArray
#from structures.linked_list import DoublyLinkedList, Node


class KmerStore:
    """
    A data structure for maintaining and querying k-mers.
    You may add any additional functions or member variables
    as you see fit.
    At any moment, the structure is maintaining n distinct k-mers.
    """

    def __init__(self, k: int) -> None:
        self.k = k
        self.kmers = DynamicArray()  # Using DynamicArray to store k-mers
        self.frequency = DynamicArray()  # Parallel array to store frequencies
        self.prefix_count = {}  # Dictionary to keep track of prefix counts



    def read(self, infile: str) -> None:
        """
        Given a path to an input file, break the sequences into
        k-mers and load them into your data structure.
        """
        with open(infile, "r") as file:
            for line in file:
                line = line.strip()  # Remove any trailing newline or spaces
                for i in range(len(line) - self.k + 1):
                    kmer = line[i:i + self.k]
                    self._insert_kmer(kmer)

    def _insert_kmer(self, kmer: str) -> None:
        """
        Helper function to insert a k-mer into the DynamicArray
        and update its frequency.
        """
        """ Insert kmer into the sorted DynamicArray and maintain frequency. """
        index = self._binary_search_insert_position(kmer)

        if index < self.kmers.get_size() and self.kmers.get_at(index) == kmer:
            self.frequency.set_at(index, self.frequency.get_at(index) + 1)
        else:
            self._insert_at_position(index, kmer)

        prefix = kmer[:2]
        if prefix in self.prefix_count:
            self.prefix_count[prefix] += 1
        else:
            self.prefix_count[prefix] = 1

    def batch_insert(self, kmers: list[str]) -> None:
        """
        Given a list of m k-mers, delete the matching ones
        (including all duplicates).
        [V2: Correction]
        If the data structure contains n elements, and the input kmer list
        contains m elements, the targeted time complexity is:
        O(m log m) + O(n + m) amortized time (or better, of course!)
        """
        for kmer in kmers:
            self._insert_kmer(kmer)

    def batch_delete(self, kmers: list[str]) -> None:
        """
        Given a list of m k-mers, delete the matching ones
        (including all duplicates).
        [V2: Correction]
        If the data structure contains n elements, and the input kmer list
        contains m elements, the targeted time complexity is:
        O(m log m) + O(n + m) amortized time (or better, of course!)
 
        """
        new_kmers = DynamicArray()
        for i in range(self.kmers.get_size()):
            kmer = self.kmers.get_at(i)
            if kmer in kmers:
                self.frequency[kmer] -= 1
                if self.frequency[kmer] == 0:
                    self.frequency[kmer] = None 
            else:
                new_kmers.append(kmer)
        self.kmers = new_kmers

    def freq_geq(self, m: int) -> list[str]:
        """
        Given an integer m, return a list of k-mers that occur
        >= m times in your data structure.
        Time complexity for full marks: O(n)
        """
        result = []
        for i in range(self.kmers.get_size()):
            freq = self.frequency.get_at(i)
            if freq is not None and freq >= m:
                result.append(self.kmers.get_at(i))
        return result

    def _insert_at_position(self, index: int, kmer: str) -> None:
        """
        Insert the k-mer at the given index and shift elements accordingly.
        """
        self.kmers.append(None)
        self.frequency.append(0)

        for i in range(self.kmers.get_size() - 1, index, -1):
            self.kmers.set_at(i, self.kmers.get_at(i - 1))
            self.frequency.set_at(i, self.frequency.get_at(i - 1))

        self.kmers.set_at(index, kmer)
        self.frequency.set_at(index, 1)

    def _binary_search_insert_position(self, kmer: str) -> int:
        """Find the correct position to insert kmer to keep the array sorted."""
        low, high = 0, self.kmers.get_size() - 1
        while low <= high:
            mid = (low + high) // 2
            mid_kmer = self.kmers.get_at(mid)
            if mid_kmer < kmer:
                low = mid + 1
            else:
                high = mid - 1
        return low

    def count(self, kmer: str) -> int:
        """
        Given a k-mer, return the number of times it appears in
        your data structure.
        Time complexity for full marks: O(log n)
        """
        index = self._binary_search_insert_position(kmer)
        if index < self.kmers.get_size() and self.kmers.get_at(index) == kmer:
            return self.frequency.get_at(index)
        return 0

    def count_geq(self, kmer: str) -> int:
        """
        Given a k-mer, return the total number of k-mers that
        are lexicographically greater or equal.
        Time complexity for full marks: O(log n)
        """
        index = self._binary_search_insert_position(kmer)
        count = 0
        for i in range(index, self.kmers.get_size()):
            count += self.frequency.get_at(i)
        return count

    def compatible(self, kmer: str) -> int:
        """
        Given a k-mer, return the total number of compatible
        k-mers. You will be using the two suffix characters
        of the input k-mer to compare against the first two
        characters of all other k-mers.
        Time complexity for full marks: O(1) :-)
        """
        last_two = kmer[-2:]
        complement_map = {"A": "T", "T": "A", "C": "G", "G": "C"}
        first_two_complement = complement_map[last_two[0]] + complement_map[last_two[1]]
        return self.prefix_count.get(first_two_complement, 0)
    # Any other functionality you may need
