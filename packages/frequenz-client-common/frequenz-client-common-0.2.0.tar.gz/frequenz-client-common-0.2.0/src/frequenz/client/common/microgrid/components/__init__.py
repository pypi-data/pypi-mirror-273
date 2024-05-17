# License: MIT
# Copyright © 2022 Frequenz Energy-as-a-Service GmbH

"""Defines the components that can be used in a microgrid."""
from __future__ import annotations

from enum import Enum

# pylint: disable=no-name-in-module
from frequenz.api.common.v1.microgrid.components.components_pb2 import (
    ComponentCategory as PBComponentCategory,
)

# pylint: enable=no-name-in-module


class ComponentCategory(Enum):
    """Possible types of microgrid component."""

    UNSPECIFIED = PBComponentCategory.COMPONENT_CATEGORY_UNSPECIFIED
    """An unknown component category.

    Useful for error handling, and marking unknown components in
    a list of components with otherwise known categories.
    """

    GRID = PBComponentCategory.COMPONENT_CATEGORY_GRID
    """The point where the local microgrid is connected to the grid."""

    METER = PBComponentCategory.COMPONENT_CATEGORY_METER
    """A meter, for measuring electrical metrics, e.g., current, voltage, etc."""

    INVERTER = PBComponentCategory.COMPONENT_CATEGORY_INVERTER
    """An electricity generator, with batteries or solar energy."""

    BATTERY = PBComponentCategory.COMPONENT_CATEGORY_BATTERY
    """A storage system for electrical energy, used by inverters."""

    EV_CHARGER = PBComponentCategory.COMPONENT_CATEGORY_EV_CHARGER
    """A station for charging electrical vehicles."""

    CHP = PBComponentCategory.COMPONENT_CATEGORY_CHP
    """A heat and power combustion plant (CHP stands for combined heat and power)."""

    @classmethod
    def from_proto(
        cls, component_category: PBComponentCategory.ValueType
    ) -> ComponentCategory:
        """Convert a protobuf ComponentCategory message to ComponentCategory enum.

        Args:
            component_category: protobuf enum to convert

        Returns:
            Enum value corresponding to the protobuf message.
        """
        if not any(t.value == component_category for t in ComponentCategory):
            return ComponentCategory.UNSPECIFIED
        return cls(component_category)

    def to_proto(self) -> PBComponentCategory.ValueType:
        """Convert a ComponentCategory enum to protobuf ComponentCategory message.

        Returns:
            Enum value corresponding to the protobuf message.
        """
        return self.value
