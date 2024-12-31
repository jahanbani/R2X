"""Model related to branches."""

from r2x.models.core import Device, MinMax
from r2x.models.topology import Bus, ACBus, DCBus, Area
from typing import Annotated, Any
from pydantic import Field, NonNegativeFloat, NonPositiveFloat, field_serializer
from r2x.units import ActivePower, Percentage


class Branch(Device):
    """Class representing a connection between components."""

    @classmethod
    def example(cls) -> "Branch":
        return Branch(name="ExampleBranch")


class ACBranch(Branch):
    """Class representing an AC connection between components."""

    # arc: Annotated[Arc, Field(description="The branch's connections.")]
    from_bus: Annotated[ACBus, Field(description="Bus connected upstream from the arc.")]
    to_bus: Annotated[ACBus, Field(description="Bus connected downstream from the arc.")]
    r: Annotated[float | None, Field(description=("Resistance of the branch"))] = None
    x: Annotated[float | None, Field(description=("Reactance of the branch"))] = None
    primary_shunt: Annotated[float | None, Field(description=("Primary shunt of the branch"))] = None
    rating: Annotated[ActivePower, Field(ge=0, description="Thermal rating of the line.")] | None = None
    active_power_flow: Annotated[ActivePower, Field(ge=0, description="Active power flow of the line.")] | None = None
    reactive_power_flow: Annotated[ActivePower, Field(ge=0, description="Reactive power flow of the line.")] | None = None
    angle_limits: Annotated[
        MinMax | None, Field(description="Maximum and minimum angles of the branch.")
    ] = None

    @field_serializer("angle_limits")
    def serialize_angle_limits(self, min_max: MinMax) -> dict[str, Any]:
        if min_max is not None:
            return {"min": min_max.min, "max": min_max.max}


class MonitoredLine(ACBranch):
    """Class representing an AC transmission line."""

    rating_up: Annotated[ActivePower, Field(ge=0, description="Forward rating of the line.")] | None = None
    rating_down: Annotated[ActivePower, Field(le=0, description="Reverse rating of the line.")] | None = None
    losses: Annotated[Percentage, Field(description="Power losses on the line.")] | None = None

    @classmethod
    def example(cls) -> "MonitoredLine":
        return MonitoredLine(
            name="ExampleMonitoredLine",
            from_bus=ACBus.example(),
            to_bus=ACBus.example(),
            losses=Percentage(10, "%"),
            rating_up=ActivePower(100, "MW"),
            rating_down=ActivePower(-100, "MW"),
            rating=ActivePower(100, "MW"),
        )


class Line(ACBranch):
    """Class representing an AC transmission line."""

    @classmethod
    def example(cls) -> "Line":
        return Line(
            name="ExampleLine",
            from_bus=ACBus.example(),
            to_bus=ACBus.example(),
            rating=ActivePower(100, "MW"),
        )


class Transformer2W(ACBranch):
    """Class representing a 2-W transformer."""

    @classmethod
    def example(cls) -> "Transformer2W":
        return Transformer2W(
            name="Example2WTransformer",
            rating=ActivePower(100, "MW"),
            from_bus=ACBus.example(),
            to_bus=ACBus.example(),
        )


class DCBranch(Branch):
    """Class representing a DC connection between components."""

    from_bus: Annotated[Bus, Field(description="Bus connected upstream from the arc.")]
    to_bus: Annotated[Bus, Field(description="Bus connected downstream from the arc.")]
    active_power_flow: Annotated[ActivePower, Field(ge=0, description="Active power flow of the line.")] | None = None
    active_power_limits_from: Annotated[
        MinMax | None, Field(description="Maximum and minimum 'from' active power flow of the line.")
    ] = None
    active_power_limits_to: Annotated[
        MinMax | None, Field(description="Maximum and minimum 'to' active power flow of the line.")
    ] = None
    reactive_power_limits_from: Annotated[
        MinMax | None, Field(description="Maximum and minimum 'from' reactive power flow of the line.")
    ] = None
    reactive_power_limits_to: Annotated[
        MinMax | None, Field(description="Maximum and minimum 'to' reactive power flow of the line.")
    ] = None

    @field_serializer("active_power_limits_from")
    def serialize_active_power_limits_from(self, min_max: MinMax) -> dict[str, Any]:
        if min_max is not None:
            return {"min": min_max.min, "max": min_max.max}
    @field_serializer("active_power_limits_to")
    def serialize_active_power_limits_to(self, min_max: MinMax) -> dict[str, Any]:
        if min_max is not None:
            return {"min": min_max.min, "max": min_max.max}
    @field_serializer("reactive_power_limits_from")
    def serialize_reactive_power_limits_from(self, min_max: MinMax) -> dict[str, Any]:
        if min_max is not None:
            return {"min": min_max.min, "max": min_max.max}
    @field_serializer("reactive_power_limits_to")
    def serialize_reactive_power_limits_to(self, min_max: MinMax) -> dict[str, Any]:
        if min_max is not None:
            return {"min": min_max.min, "max": min_max.max}


class AreaInterchange(Branch):
    """Collection of branches that make up an interfece or corridor for the transfer of power."""

    max_power_flow: Annotated[ActivePower, Field(ge=0, description="Maximum allowed flow.")]
    min_power_flow: Annotated[ActivePower, Field(le=0, description="Minimum allowed flow.")]
    from_area: Annotated[Area, Field(description="Area containing the bus.")] | None = None
    to_area: Annotated[Area, Field(description="Area containing the bus.")] | None = None

    @classmethod
    def example(cls) -> "AreaInterchange":
        return AreaInterchange(
            name="ExampleAreaInterchange",
            max_power_flow=ActivePower(100, "MW"),
            min_power_flow=ActivePower(-100, "MW"),
            from_area=Area.example(),
            to_area=Area.example(),
        )


class TModelHVDCLine(DCBranch):
    """Class representing a DC transmission line."""

    rating_up: Annotated[NonNegativeFloat, Field(description="Forward rating of the line.")] | None = None
    rating_down: Annotated[NonPositiveFloat, Field(description="Reverse rating of the line.")] | None = None
    losses: Annotated[NonNegativeFloat, Field(description="Power losses on the line.")] = 0
    resistance: Annotated[NonNegativeFloat, Field(description="Resistance of the line in p.u.")] | None = 0
    inductance: Annotated[NonNegativeFloat, Field(description="Inductance of the line in p.u.")] | None = 0
    capacitance: Annotated[NonNegativeFloat, Field(description="Capacitance of the line in p.u.")] | None = 0

    @classmethod
    def example(cls) -> "TModelHVDCLine":
        return TModelHVDCLine(
            name="ExampleDCLine",
            from_bus=DCBus.example(),
            to_bus=DCBus.example(),
            rating_up=100,
            rating_down=80,
        )
