import tidy3d as td
import photonforge as pf


_Medium = td.components.medium.MediumType


@pf.parametric_technology
def ebeam(
    *,
    si_thickness: float = 0.220,
    si_slab_thickness: float = 0.090,
    sin_thickness: float = 0.400,
    si_mask_dilation: float = 0.0,
    si_slab_mask_dilation: float = 0.0,
    sin_mask_dilation: float = 0.0,
    sidewall_angle: float = 0.0,
    metal_si_separation: float = 2.2,
    router_thickness: float = 0.6,
    heater_thickness: float = 0.2,
    top_oxide_thickness: float = 0.3,
    bottom_oxide_thickness: float = 3.017,
    include_top_opening: bool = False,
    include_substrate: bool = False,
    sio2: dict[str, _Medium] = {
        "optical": td.material_library["SiO2"]["Palik_Lossless"],
        "electrical": td.Medium(permittivity=4.2, name="SiO2"),
    },
    si: dict[str, _Medium] = {
        "optical": td.material_library["cSi"]["Li1993_293K"],
        "electrical": td.Medium(permittivity=12.3, name="Si"),
    },
    sin: dict[str, _Medium] = {
        "optical": td.material_library["Si3N4"]["Luke2015PMLStable"],
        "electrical": td.Medium(permittivity=7.5, name="Si3N4"),
    },
    router_metal: dict[str, _Medium] = {
        "optical": td.material_library["Au"]["JohnsonChristy1972"],
        "electrical": td.LossyMetalMedium(
            conductivity=17,
            frequency_range=[0.1e9, 200e9],
            fit_param=td.SurfaceImpedanceFitterParam(max_num_poles=16),
        ),
    },
    heater_metal: dict[str, _Medium] = {
        "optical": td.material_library["W"]["Werner2009"],
        "electrical": td.LossyMetalMedium(
            conductivity=1.6,
            frequency_range=[0.1e9, 200e9],
            fit_param=td.SurfaceImpedanceFitterParam(max_num_poles=16),
        ),
    },
    opening: _Medium = td.Medium(permittivity=1.0),
) -> pf.Technology:
    """Create a technology for the e-beam PDK.

    The current version does not extrude heaters or metal layers, nor oxide
    opening windows.

    Args:
        si_thickness (float): Full silicon layer thickness.
        si_slab_thickness (float): Partially etched slab thickness in
          silicon.
        sin_thickness (float): SiN layer thickness.
        si_mask_dilation (float): Mask dilation for the full-thickness Si
          layer.
        si_slab_mask_dilation (float): Mask dilation for the partially
          etched Si layer.
        sin_mask_dilation (float): Mask dilation for the SiN layer.
        sidewall_angle (float): Sidewall angle (in degrees) for Si and SiN
          etching.
        metal_si_separation (float): Separation between the metal layers and
          the Si layer.
        router_thickness (float): Thickness of the routing metal layer.
        heater_thickness (float): Thickness of the heater metal layer.
        top_oxide_thickness (float): Thickness of the top oxide clad,
          measured from the substrate.
        bottom_oxide_thickness (float): Thickness of the bottom oxide clad.
        include_top_opening (bool): Flag indicating whether or not to
          include the region above the top oxide.
        include_substrate (bool): Flag indicating whether or not to include
          the silicon substrate.
        sio2 (Medium): Background medium.
        si (Medium): Silicon medium.
        sin (Medium): Silicon nitride medium.
        router_metal (Medium): Routing metal medium.
        heater_metal (Medium): Heater metal medium.
        opening (Medium): Medium for openings.

    Returns:
        Technology: E-Beam PDK technology definition.
    """

    layers = {
        "Waveguide": pf.LayerSpec((1, 99), "Waveguides", "#ff80a818", "\\"),
        "Si": pf.LayerSpec((1, 0), "Waveguides", "#ff80a818", "\\\\"),
        "SiN": pf.LayerSpec((4, 0), "Waveguides", "#a6cee318", "\\\\"),
        "Si slab": pf.LayerSpec((2, 0), "Waveguides", "#80a8ff18", "/"),
        "Si_Litho193nm": pf.LayerSpec((1, 69), "Waveguides", "#cc80a818", "\\"),
        "Oxide open (to BOX)": pf.LayerSpec((6, 0), "Waveguides", "#ffae0018", "\\"),
        "Text": pf.LayerSpec((10, 0), "", "#0000ff18", "\\"),
        "Si N": pf.LayerSpec((20, 0), "Doping", "#7000FF18", "\\\\"),
        "Si N++": pf.LayerSpec((24, 0), "Doping", "#0000ff18", ":"),
        "M1_heater": pf.LayerSpec((11, 0), "Metal", "#ebc63418", "xx"),
        "M2_router": pf.LayerSpec((12, 0), "Metal", "#90857018", "xx"),
        "M_Open": pf.LayerSpec((13, 0), "Metal", "#3471eb18", "xx"),
        "VC": pf.LayerSpec((40, 0), "Metal", "#3a027f18", "xx"),
        "FloorPlan": pf.LayerSpec((99, 0), "Misc", "#8000ff18", "hollow"),
        "Deep Trench": pf.LayerSpec((201, 0), "Misc", "#c0c0c018", "solid"),
        "Isolation Trench": pf.LayerSpec((203, 0), "Misc", "#c0c0c018", "solid"),
        "Dicing": pf.LayerSpec((210, 0), "Misc", "#a0a0c018", "solid"),
        "Chip design area": pf.LayerSpec((290, 0), "Misc", "#80005718", "hollow"),
        "Keep out": pf.LayerSpec((202, 0), "Misc", "#a0a0c018", "//"),
        "SEM": pf.LayerSpec((200, 0), "Misc", "#ff00ff18", "\\"),
        "DevRec": pf.LayerSpec((68, 0), "SiEPIC", "#00408018", "hollow"),
        "PinRec": pf.LayerSpec((1, 10), "SiEPIC", "#00408018", "/"),
        "PinRecM": pf.LayerSpec((1, 11), "SiEPIC", "#00408018", "/"),
        "FbrTgt": pf.LayerSpec((81, 0), "SiEPIC", "#00408018", "/"),
        "Errors": pf.LayerSpec((999, 0), "SiEPIC", "#00008018", "/"),
        "FDTD": pf.LayerSpec((733, 0), "SiEPIC", "#80005718", "hollow"),
        "BlackBox": pf.LayerSpec((998, 0), "SiEPIC", "#00408018", "solid"),
    }

    # References:
    # https://www.appliednt.com/nanosoi-fabrication-service/
    # https://www.appliednt.com/nanosoi/sys/
    z_heater = si_thickness + metal_si_separation
    z_router = z_heater + heater_thickness
    z_open = z_heater + router_thickness

    extrusion_specs = [
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
        pf.ExtrusionSpec(
            pf.MaskSpec((4, 0), dilation=sin_mask_dilation), sin, (0, sin_thickness), sidewall_angle
        ),
        pf.ExtrusionSpec(pf.MaskSpec((11, 0), (12, 0), "+"), heater_metal, (z_heater, z_router)),
        pf.ExtrusionSpec(pf.MaskSpec((12, 0)), router_metal, (z_router, z_open)),
        pf.ExtrusionSpec(pf.MaskSpec((13, 0)), opening, (z_open, pf.Z_INF)),
        pf.ExtrusionSpec(
            pf.MaskSpec([(201, 0), (203, 0), (210, 0)]), opening, (-pf.Z_INF, pf.Z_INF)
        ),
    ]

    if include_top_opening:
        extrusion_specs.insert(
            0, pf.ExtrusionSpec(pf.MaskSpec(), opening, (top_oxide_thickness, pf.Z_INF))
        )

    if include_substrate:
        extrusion_specs.insert(
            0, pf.ExtrusionSpec(pf.MaskSpec(), si, (-pf.Z_INF, -bottom_oxide_thickness))
        )

    ports = {
        "TE_1550_500": pf.PortSpec(
            description="Strip TE 1550 nm, w=500 nm",
            width=2.0,
            limits=(-1, 1 + si_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=3.5,
            path_profiles=((0.5, 0.0, (1, 0)),),
        ),
        "TE_1310_410": pf.PortSpec(
            description="Strip TE 1310 nm, w=410 nm",
            width=2.0,
            limits=(-1, 1 + si_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=3.5,
            path_profiles=((0.41, 0.0, (1, 0)),),
        ),
        "TE_1310_350": pf.PortSpec(
            description="Strip TE 1310 nm, w=350 nm",
            width=2.0,
            limits=(-1, 1 + si_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=3.5,
            path_profiles=((0.35, 0.0, (1, 0)),),
        ),
        "TM_1310_350": pf.PortSpec(
            description="Strip TM 1310 nm, w=350 nm",
            width=2.0,
            limits=(-1, 1 + si_thickness),
            num_modes=1,
            added_solver_modes=1,
            polarization="TM",
            target_neff=3.5,
            path_profiles=((0.35, 0.0, (1, 0)),),
        ),
        "TM_1550_500": pf.PortSpec(
            description="Strip TM 1550 nm, w=500 nm",
            width=2.5,
            limits=(-1, 1 + si_thickness),
            num_modes=1,
            added_solver_modes=1,
            polarization="TM",
            target_neff=3.5,
            path_profiles=((0.5, 0.0, (1, 0)),),
        ),
        "TE-TM_1550_450": pf.PortSpec(
            description="Strip TE-TM 1550, w=450 nm",
            width=2.0,
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
            num_modes=12,
            added_solver_modes=0,
            polarization=None,
            target_neff=3.5,
            path_profiles=((2.0, 0.0, (1, 0)),),
        ),
        "MM_TE_1550_3000": pf.PortSpec(
            description="Multimode Strip TE 1550 nm, w=3000 nm",
            width=6.0,
            limits=(-2, 2 + si_thickness),
            num_modes=17,
            added_solver_modes=0,
            polarization=None,
            target_neff=3.5,
            path_profiles=((3.0, 0.0, (1, 0)),),
        ),
        "Slot_TE_1550_500": pf.PortSpec(
            description="Slot TE 1550 nm, w=500 nm, gap=100nm",
            width=2.0,
            limits=(-1, 1 + si_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=3.5,
            path_profiles=((0.2, -0.15, (1, 0)), (0.2, 0.15, (1, 0))),
        ),
        "eskid_TE_1550": pf.PortSpec(
            description="eskid TE 1550",
            width=3.31,
            limits=(-1, 1 + si_thickness),
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
            limits=(-1, 1 + si_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=3.5,
            path_profiles=((0.5, 0.0, (1, 0)), (3.0, 0.0, (2, 0))),
        ),
        "Rib_TE_1310_350": pf.PortSpec(
            description="Rib (90 nm slab) TE 1310 nm, w=350 nm",
            width=2.35,
            limits=(-1, 1 + si_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=3.5,
            path_profiles=((0.35, 0.0, (1, 0)), (3.0, 0.0, (2, 0))),
        ),
        "SiN_TE_895_450": pf.PortSpec(
            description="SiN Strip TE 895 nm, w=450 nm",
            width=2.0,
            limits=(-1.0, 1.0 + sin_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=2.1,
            path_profiles=((0.45, 0.0, (4, 0)),),
        ),
        "SiN_TE_1550_750": pf.PortSpec(
            description="SiN Strip TE 1550 nm, w=750 nm",
            width=3.0,
            limits=(-1, 1 + sin_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=2.1,
            path_profiles=((0.75, 0.0, (4, 0)),),
        ),
        "SiN_TE_1550_800": pf.PortSpec(
            description="SiN Strip TE 1550 nm, w=800 nm",
            width=3.0,
            limits=(-1, 1 + sin_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=2.1,
            path_profiles=((0.8, 0.0, (4, 0)),),
        ),
        "SiN_TE_1550_1000": pf.PortSpec(
            description="SiN Strip TE 1550 nm, w=1000 nm",
            width=3.0,
            limits=(-1, 1 + sin_thickness),
            num_modes=1,
            added_solver_modes=0,
            polarization=None,
            target_neff=2.1,
            path_profiles=((1.0, 0.0, (4, 0)),),
        ),
        "SiN_TM_1550_1000": pf.PortSpec(
            description="SiN Strip TM 1550 nm, w=1000 nm",
            width=3.0,
            limits=(-1.5, 1.5 + sin_thickness),
            num_modes=1,
            added_solver_modes=1,
            polarization="TM",
            target_neff=2.1,
            path_profiles=((1.0, 0.0, (4, 0)),),
        ),
        # Added for ebeam_Polarizer_TM_1550_UQAM
        "SiN_TE-TM_1550_1000": pf.PortSpec(
            description="SiN Strip TM 1550 nm, w=1000 nm",
            width=3.0,
            limits=(-1.5, 1.5 + sin_thickness),
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
            limits=(-1.5, 1.5 + sin_thickness),
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

    result = pf.Technology("SiEPIC EBeam", "0.4.32", layers, extrusion_specs, ports, sio2)
    result.random_variables = [
        pf.monte_carlo.RandomVariable("si_thickness", value=0.22, stdev=0.0223 / 6),
        pf.monte_carlo.RandomVariable("bottom_oxide_thickness", value=3.017, stdev=0.006 / 6),
    ]
    return result
