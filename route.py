from __future__ import annotations
from dataclasses import dataclass

from computer import Computer

from branch_decision import BranchDecision

from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from virus import VirusType


@dataclass
class RouteSplit:
    """
    A split in the route.
       _____top______
      /              \
    -<                >-following-
      \____bottom____/
    """

    top: Route
    bottom: Route
    following: Route

    def remove_branch(self) -> RouteStore:
        """Removes the branch, should just leave the remaining following route."""
        raise NotImplementedError()

@dataclass
class RouteSeries:
    """
    A computer, followed by the rest of the route

    --computer--following--

    """

    computer: Computer
    following: Route

    def remove_computer(self) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Removing the computer at the beginning of this series.
        """
        raise NotImplementedError()

    def add_computer_before(self, computer: Computer) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding a computer in series before the current one.
        """
        raise NotImplementedError()

    def add_computer_after(self, computer: Computer) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding a computer after the current computer, but before the following route.
        """
        raise NotImplementedError()

    def add_empty_branch_before(self) -> RouteStore:
        """Returns a route store which would be the result of:
        Adding an empty branch, where the current routestore is now the following path.
        """
        raise NotImplementedError()

    def add_empty_branch_after(self) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding an empty branch after the current computer, but before the following route.
        """
        raise NotImplementedError()


RouteStore = Union[RouteSplit, RouteSeries, None]


@dataclass
class Route:

    store: RouteStore = None

    def add_computer_before(self, computer: Computer) -> Route:
        """
        Returns a *new* route which would be the result of:
        Adding a computer before everything currently in the route.
        """
        raise NotImplementedError()

    def add_empty_branch_before(self) -> Route:
        """
        Returns a *new* route which would be the result of:
        Adding an empty branch before everything currently in the route.
        """
        raise NotImplementedError()

    def follow_path(self, virus_type: VirusType) -> None:
        current_route = self.store
        while current_route:
            if isinstance(current_route, RouteSeries):
                if isinstance(current_route.computer, Computer):
                    virus_type.add_computer(current_route.computer)
                current_route = current_route.following
            elif isinstance(current_route, RouteSplit):
                decision = virus_type.select_branch(current_route.top, current_route.bottom)
                current_route = current_route.top if decision == BranchDecision.TOP else current_route.bottom
            elif isinstance(current_route, Route):
                current_route = current_route.store 
            else:
                break

    def add_all_computers(self) -> list[Computer]:
        """Returns a list of all computers on the route."""
        computers = []
        if isinstance(self.store, RouteSeries):
            computers.append(self.store.computer)
            if self.store.following:
                computers.extend(self.store.following.add_all_computers())
        elif isinstance(self.store, RouteSplit):
            computers.extend(self.store.top.add_all_computers())
            computers.extend(self.store.bottom.add_all_computers())
            if self.store.following:
                computers.extend(self.store.following.add_all_computers())
        return computers
        
