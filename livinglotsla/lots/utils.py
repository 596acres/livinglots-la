from pint import UnitRegistry


ureg = UnitRegistry()


def acres_to_square_feet(acres):
    return (float(acres) * ureg.acre).to(ureg.feet ** 2).magnitude
