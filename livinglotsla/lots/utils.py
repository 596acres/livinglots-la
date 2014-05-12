from pint import UnitRegistry


ureg = UnitRegistry()


def acres_to_square_feet(acres):
    return (float(acres) * ureg.acre).to(ureg.feet ** 2).magnitude


def square_feet_to_acres(square_feet):
    return (float(square_feet) * (ureg.feet ** 2)).to(ureg.acre).magnitude
