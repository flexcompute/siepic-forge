import photonforge as pf
import photonforge.typing as pft
import tidy3d as td

from ._layers import _layers

# References:
# https://www.appliednt.com/nanosoi-fabrication-service/
# https://www.appliednt.com/nanosoi/sys/


@pf.parametric_technology
def ebeam(
    *,
    sin_thickness: pft.PositiveDimension = 0.400,
    sin_mask_dilation: pft.Coordinate = 0.0,
    sidewall_angle: pft.Angle = 0.0,
    heater_thickness: pft.PositiveDimension = 0.2,
    router_thickness: pft.PositiveDimension = 0.6,
    bottom_oxide_thickness: pft.PositiveDimension = 4.5,
    top_oxide_thickness: pft.PositiveDimension = 3.0,
    passivation_oxide_thickness: pft.PositiveDimension = 0.3,
    sio2: dict[str, pft.Medium] = {
        "optical": td.material_library["SiO2"]["Palik_Lossless"],
        "electrical": td.Medium(permittivity=4.2, name="SiO2"),
    },
    si: dict[str, pft.Medium] = {
        "optical": td.material_library["cSi"]["Li1993_293K"],
        "electrical": td.Medium(permittivity=12.3, name="Si"),
    },
    sin: dict[str, pft.Medium] = {
        "optical": td.material_library["Si3N4"]["Luke2015PMLStable"],
        "electrical": td.Medium(permittivity=7.5, name="Si3N4"),
    },
    router_metal: dict[str, pft.Medium] = {
        "optical": td.material_library["Au"]["Olmon2012evaporated"],
        "electrical": td.LossyMetalMedium(
            conductivity=17,
            frequency_range=[0.1e9, 200e9],
            fit_param=td.SurfaceImpedanceFitterParam(max_num_poles=16),
        ),
    },
    heater_metal: dict[str, pft.Medium] = {
        "optical": td.material_library["W"]["Werner2009"],
        "electrical": td.LossyMetalMedium(
            conductivity=1.6,
            frequency_range=[0.1e9, 200e9],
            fit_param=td.SurfaceImpedanceFitterParam(max_num_poles=16),
        ),
    },
    opening: pft.Medium = td.Medium(permittivity=1.0),
) -> pf.Technology:
    """Create a technology for the e-beam SiN PDK.

    Args:
        sin_thickness: SiN layer thickness.
        sin_mask_dilation: Mask dilation for the SiN layer.
        sidewall_angle: Sidewall angle (in degrees) for SiN etching.
        heater_thickness: Thickness of the heater metal layer.
        router_thickness: Thickness of the routing metal bilayer.
        bottom_oxide_thickness: Thickness of the bottom oxide clad.
        top_oxide_thickness: Thickness of the top oxide clad, measured from
          the substrate.
        passivation_oxide_thickness: Thickness of oxide above metal layers.
        sio2: Background medium.
        si: Silicon medium.
        sin: Silicon nitride medium.
        router_metal: Routing metal medium.
        heater_metal: Heater metal medium.
        opening: Medium for openings.

    Returns:
        Technology: E-Beam PDK technology definition.
    """

    layers = {k: v.copy() for k, v in _layers.items()}

    z_router = top_oxide_thickness + heater_thickness
    z_open = z_router + router_thickness
    z_top = z_open + passivation_oxide_thickness

    extrusion_specs = [
        pf.ExtrusionSpec(pf.MaskSpec(), si, (-pf.Z_INF, 0)),
        pf.ExtrusionSpec(
            pf.MaskSpec(),
            sio2,
            (-bottom_oxide_thickness, top_oxide_thickness + passivation_oxide_thickness),
        ),
        pf.ExtrusionSpec(
            pf.MaskSpec((11, 0), dilation=passivation_oxide_thickness),
            sio2,
            (top_oxide_thickness, z_router + passivation_oxide_thickness),
        ),
        pf.ExtrusionSpec(
            pf.MaskSpec((12, 0), dilation=passivation_oxide_thickness),
            sio2,
            (top_oxide_thickness, z_top),
        ),
        pf.ExtrusionSpec(pf.MaskSpec((11, 0)), heater_metal, (top_oxide_thickness, z_router)),
        pf.ExtrusionSpec(pf.MaskSpec((12, 0)), router_metal, (z_router, z_open)),
        pf.ExtrusionSpec(pf.MaskSpec((13, 0)), opening, (z_open, z_top)),
        pf.ExtrusionSpec(pf.MaskSpec((6, 0)), opening, (0, pf.Z_INF)),
        pf.ExtrusionSpec(
            pf.MaskSpec((4, 0), dilation=sin_mask_dilation), sin, (0, sin_thickness), sidewall_angle
        ),
        pf.ExtrusionSpec(pf.MaskSpec([(201, 0), (203, 0)]), opening, (-pf.Z_INF, pf.Z_INF)),
    ]

    ports = {
        "SiN_TE_895_450": pf.PortSpec(
            description="SiN Strip TE 895 nm, w=450 nm",
            width=2.0,
            limits=(-0.7, 0.7 + sin_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=2.1,
            path_profiles=((0.45, 0.0, (4, 0)),),
        ),
        "SiN_TE_1550_750": pf.PortSpec(
            description="SiN Strip TE 1550 nm, w=750 nm",
            width=4.0,
            limits=(-1.5, 1.5 + sin_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=2.1,
            path_profiles=((0.75, 0.0, (4, 0)),),
        ),
        "SiN_TE_1550_800": pf.PortSpec(
            description="SiN Strip TE 1550 nm, w=800 nm",
            width=4.0,
            limits=(-1.5, 1.5 + sin_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=2.1,
            path_profiles=((0.8, 0.0, (4, 0)),),
        ),
        "SiN_TE_1550_1000": pf.PortSpec(
            description="SiN Strip TE 1550 nm, w=1000 nm",
            width=4.0,
            limits=(-1.5, 1.5 + sin_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=2.1,
            path_profiles=((1.0, 0.0, (4, 0)),),
        ),
        "SiN_TM_1550_1000": pf.PortSpec(
            description="SiN Strip TM 1550 nm, w=1000 nm",
            width=3.5,
            limits=(-1.2, 1.2 + sin_thickness),
            num_modes=1,
            added_solver_modes=1,
            polarization="TM",
            target_neff=2.1,
            path_profiles=((1.0, 0.0, (4, 0)),),
        ),
        # Added for ebeam_Polarizer_TM_1550_UQAM
        "SiN_TE-TM_1550_1000": pf.PortSpec(
            description="SiN Strip TM 1550 nm, w=1000 nm",
            width=4.0,
            limits=(-1.8, 1.8 + sin_thickness),
            num_modes=2,
            added_solver_modes=0,
            polarization=None,
            target_neff=2.1,
            path_profiles=((1.0, 0.0, (4, 0)),),
        ),
        "SiN_TE_1310_750": pf.PortSpec(
            description="SiN Strip TE 1310 nm, w=750 nm",
            width=3.0,
            limits=(-1, 1 + sin_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=2.1,
            path_profiles=((0.75, 0.0, (4, 0)),),
        ),
        "SiN_TE_1310_800": pf.PortSpec(
            description="SiN Strip TE 1310 nm, w=800 nm",
            width=3.0,
            limits=(-1, 1 + sin_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=2.1,
            path_profiles=((0.8, 0.0, (4, 0)),),
        ),
        "SiN_TM_1310_750": pf.PortSpec(
            description="SiN Strip TM 1310 nm, w=750 nm",
            width=3.0,
            limits=(-1.2, 1.2 + sin_thickness),
            num_modes=1,
            added_solver_modes=1,
            polarization="TM",
            target_neff=2.1,
            path_profiles=((0.75, 0.0, (4, 0)),),
        ),
        "MM_SiN_TE_1550_3000": pf.PortSpec(
            description="Multimode SiN Strip TE 1550 nm, w=3000 nm",
            width=8.0,
            limits=(-2.5, 2.5 + sin_thickness),
            num_modes=7,
            added_solver_modes=0,
            polarization=None,
            target_neff=2.1,
            path_profiles=((3.0, 0.0, (4, 0)),),
        ),
    }

    result = pf.Technology("SiEPIC EBeam SiN", "1.2.0", layers, extrusion_specs, ports, opening)
    result.random_variables = []
    return result
