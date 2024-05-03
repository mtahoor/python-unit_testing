from __future__ import annotations
from abc import ABC, abstractmethod
from computer import Computer
from route import Route, RouteSeries
from branch_decision import BranchDecision


class VirusType(ABC):

    def __init__(self) -> None:
        self.computers = []
        

    def add_computer(self, computer: Computer) -> None:
        self.computers.append(computer)
        print(computer)
        print(self.computers)

    @abstractmethod
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        pass


class TopVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        # Always select the top branch
        return BranchDecision.TOP


class BottomVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        # Always select the bottom branch
        return BranchDecision.BOTTOM


class LazyVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        Try looking into the first computer on each branch,
        take the path of the least difficulty.
        """
        top_route = type(top_branch.store) == RouteSeries
        bot_route = type(bottom_branch.store) == RouteSeries

        if top_route and bot_route:
            top_comp = top_branch.store.computer
            bot_comp = bottom_branch.store.computer

            if top_comp.hacking_difficulty < bot_comp.hacking_difficulty:
                return BranchDecision.TOP
            elif top_comp.hacking_difficulty > bot_comp.hacking_difficulty:
                return BranchDecision.BOTTOM
            else:
                return BranchDecision.STOP
        # If one of them has a computer, don't take it.
        # If neither do, then take the top branch.
        if top_route:
            return BranchDecision.BOTTOM
        return BranchDecision.TOP


class RiskAverseVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        This virus is risk averse and likes to choose the path with the lowest risk factor.
        """
        return BranchDecision.BOTTOM


class FancyVirus(VirusType):
    CALC_STR = "7 3 + 8 - 2 * 2 /"

    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        This virus has a fancy-pants and likes to overcomplicate its approach.
        """
        # Split the expression into tokens
        tokens = self.CALC_STR.split()

        # Evaluate the expression
        result = self.evaluate_expression(tokens)

        # Make the decision based on the result
        if result >= 0:
            return BranchDecision.TOP
        else:
            return BranchDecision.BOTTOM

    def evaluate_expression(self, tokens):
        stack = []
        for token in tokens:
            if token.isdigit():
                stack.append(int(token))
            else:
                if token == '+':
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a + b)
                elif token == '-':
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a - b)
                elif token == '*':
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a * b)
                elif token == '/':
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a / b)
        return stack[0] if stack else 0
