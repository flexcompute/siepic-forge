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
    si_thickness: pft.PositiveDimension = 0.220,
    si_slab_thickness: pft.PositiveDimension = 0.090,
    si_mask_dilation: pft.Coordinate = 0.0,
    si_slab_mask_dilation: pft.Coordinate = 0.0,
    sidewall_angle: pft.Angle = 0.0,
    heater_thickness: pft.PositiveDimension = 0.2,
    router_thickness: pft.PositiveDimension = 0.6,
    bottom_oxide_thickness: pft.PositiveDimension = 2.0,
    top_oxide_thickness: pft.PositiveDimension = 2.2,
    passivation_oxide_thickness: pft.PositiveDimension = 0.3,
    sio2: dict[str, pft.Medium] = {
        "optical": td.material_library["SiO2"]["Palik_Lossless"],
        "electrical": td.Medium(permittivity=4.2, name="SiO2"),
    },
    si: dict[str, pft.Medium] = {
        "optical": td.material_library["cSi"]["Li1993_293K"],
        "electrical": td.Medium(permittivity=12.3, name="Si"),
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
    """Create a technology for the e-beam PDK.

    Args:
        si_thickness: Full silicon layer thickness.
        si_slab_thickness: Partially etched slab thickness in silicon.
        si_mask_dilation: Mask dilation for the full-thickness Si layer.
        si_slab_mask_dilation: Mask dilation for the partially etched Si
          layer.
        sidewall_angle: Sidewall angle (in degrees) for Si etching.
        heater_thickness: Thickness of the heater metal layer.
        router_thickness: Thickness of the routing metal bilayer.
        bottom_oxide_thickness: Thickness of the bottom oxide clad.
        top_oxide_thickness: Thickness of the top oxide clad, measured from
          the substrate.
        passivation_oxide_thickness: Thickness of oxide above metal layers.
        sio2: Background medium.
        si: Silicon medium.
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
            pf.MaskSpec((1, 0), dilation=si_mask_dilation), si, (0, si_thickness), sidewall_angle
        ),
        pf.ExtrusionSpec(
            pf.MaskSpec((2, 0), dilation=si_slab_mask_dilation),
            si,
            (0, si_slab_thickness),
            sidewall_angle,
        ),
        pf.ExtrusionSpec(pf.MaskSpec([(201, 0), (203, 0)]), opening, (-pf.Z_INF, pf.Z_INF)),
    ]

    ports = {
        "TE_1550_500": pf.PortSpec(
            description="Strip TE 1550 nm, w=500 nm",
            width=1.5,
            limits=(-0.6, 0.6 + si_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=3.5,
            path_profiles=((0.5, 0.0, (1, 0)),),
        ),
        "TE_1310_410": pf.PortSpec(
            description="Strip TE 1310 nm, w=410 nm",
            width=1.5,
            limits=(-0.6, 0.6 + si_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=3.5,
            path_profiles=((0.41, 0.0, (1, 0)),),
        ),
        "TE_1310_350": pf.PortSpec(
            description="Strip TE 1310 nm, w=350 nm",
            width=1.5,
            limits=(-0.6, 0.6 + si_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=3.5,
            path_profiles=((0.35, 0.0, (1, 0)),),
        ),
        "TM_1310_350": pf.PortSpec(
            description="Strip TM 1310 nm, w=350 nm",
            width=1.5,
            limits=(-0.6, 0.6 + si_thickness),
            num_modes=1,
            added_solver_modes=1,
            polarization="TM",
            target_neff=3.5,
            path_profiles=((0.35, 0.0, (1, 0)),),
        ),
        "TM_1550_500": pf.PortSpec(
            description="Strip TM 1550 nm, w=500 nm",
            width=1.5,
            limits=(-0.6, 0.6 + si_thickness),
            num_modes=1,
            added_solver_modes=1,
            polarization="TM",
            target_neff=3.5,
            path_profiles=((0.5, 0.0, (1, 0)),),
        ),
        "TE-TM_1550_450": pf.PortSpec(
            description="Strip TE-TM 1550, w=450 nm",
            width=2.2,
            limits=(-1, 1 + si_thickness),
            num_modes=2,
            added_solver_modes=0,
            polarization=None,
            target_neff=3.5,
            path_profiles=((0.45, 0.0, (1, 0)),),
        ),
        "MM_TE_1550_2000": pf.PortSpec(
            description="Multimode Strip TE 1550 nm, w=2000 nm",
            width=6.0,
            limits=(-2, 2 + si_thickness),
            num_modes=10,
            added_solver_modes=0,
            polarization=None,
            target_neff=3.5,
            path_profiles=((2.0, 0.0, (1, 0)),),
        ),
        "MM_TE_1550_3000": pf.PortSpec(
            description="Multimode Strip TE 1550 nm, w=3000 nm",
            width=6.0,
            limits=(-2, 2 + si_thickness),
            num_modes=15,
            added_solver_modes=0,
            polarization=None,
            target_neff=3.5,
            path_profiles=((3.0, 0.0, (1, 0)),),
        ),
        "Slot_TE_1550_500": pf.PortSpec(
            description="Slot TE 1550 nm, w=500 nm, gap=100nm",
            width=3.0,
            limits=(-1, 1 + si_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=3.5,
            path_profiles=((0.2, -0.15, (1, 0)), (0.2, 0.15, (1, 0))),
        ),
        "eskid_TE_1550": pf.PortSpec(
            description="eskid TE 1550",
            width=2.0,
            limits=(-0.7, 0.7 + si_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=3.5,
            path_profiles=(
                (0.35, 0.0, (1, 0)),
                (0.06, 0.265, (1, 0)),
                (0.06, -0.265, (1, 0)),
                (0.06, 0.385, (1, 0)),
                (0.06, -0.385, (1, 0)),
                (0.06, 0.505, (1, 0)),
                (0.06, -0.505, (1, 0)),
                (0.06, 0.625, (1, 0)),
                (0.06, -0.625, (1, 0)),
            ),
        ),
        "Rib_TE_1550_500": pf.PortSpec(
            description="Rib (90 nm slab) TE 1550 nm, w=500 nm",
            width=2.5,
            limits=(-0.6, 0.6 + si_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=3.5,
            path_profiles=((0.5, 0.0, (1, 0)), (3.0, 0.0, (2, 0))),
        ),
        "Rib_TE_1310_350": pf.PortSpec(
            description="Rib (90 nm slab) TE 1310 nm, w=350 nm",
            width=2.35,
            limits=(-0.6, 0.6 + si_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=3.5,
            path_profiles=((0.35, 0.0, (1, 0)), (3.0, 0.0, (2, 0))),
        ),
    }

    result = pf.Technology("SiEPIC EBeam Si", "1.2.0", layers, extrusion_specs, ports, opening)
    result.random_variables = [
        pf.monte_carlo.RandomVariable("si_thickness", value=0.22, stdev=0.0223 / 6),
    ]
    return result
