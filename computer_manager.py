from __future__ import annotations
from computer import Computer

class ComputerManager:

    def __init__(self) -> None:
        self.computers = []

    def add_computer(self, computer: Computer) -> None:
        self.computers.append(computer)

    def remove_computer(self, computer: Computer) -> None:
        self.computers.remove(computer)

    def edit_computer(self, old: Computer, new: Computer) -> None:
        index = self.computers.index(old)
        self.computers[index] = new

    def computers_with_difficulty(self, diff: int) -> list[Computer]:
        return [comp for comp in self.computers if comp.hacking_difficulty == diff]

    def group_by_difficulty(self) -> list[list[Computer]]:
        sorted_computers = sorted(self.computers, key=lambda x: x.hacking_difficulty)
        grouped = []
        current_difficulty = None
        current_group = []
        for computer in sorted_computers:
            if computer.hacking_difficulty != current_difficulty:
                if current_group:
                    grouped.append(current_group)
                    current_group = []
                current_difficulty = computer.hacking_difficulty
            current_group.append(computer)
        if current_group:
            grouped.append(current_group)
        return grouped
