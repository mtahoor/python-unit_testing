from __future__ import annotations

from typing import Dict, List, Tuple

from computer import Computer


class ComputerOrganiser: 
    def __init__(self) -> None:
        self.computers: List[Tuple[Computer, int]] = []

    def cur_position(self, computer: Computer) -> int:
        """
        Returns the current position of the given computer.
        Raises a KeyError if the computer is not found.
        """ 
        for idx, (comp, _) in enumerate(self.computers):
            if comp == computer:
                return idx
        raise KeyError(f"Computer {computer.name} not found in the organiser.")

    def add_computers(self, computers: List[Computer]) -> None:
        """
        Adds a list of computers to the organiser.
        The position of each computer is determined by its index in the list.
        """
        # Sort the computers in ascending order based on hacking difficulty
        computers.sort(key=lambda c: c.hacking_difficulty)

        # Insert the sorted computers into the organizer at the correct position
        for computer in computers:
            idx = self._binary_search(computer.hacking_difficulty)
            self.computers.insert(idx, (computer, computer.hacking_difficulty))

    def _binary_search(self, target: int) -> int:
        """
        Perform binary search to find the index where the target should be inserted.
        """
        low, high = 0, len(self.computers)
        while low < high:
            mid = (low + high) // 2
            if self.computers[mid][1] < target:
                low = mid + 1
            elif self.computers[mid][1] == target:
                # Check if there are more elements with the same hacking difficulty
                while mid < len(self.computers) and self.computers[mid][1] == target:
                    mid += 1
                return mid
            else:
                high = mid
        return low
