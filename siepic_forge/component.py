try:
    from importlib.resources import files, as_file
except ImportError:
    from importlib_resources import files, as_file

import math
import warnings

import photonforge as pf


_symmetries_2port = [("P0", "P1", {"P1": "P0"})]

_symmetries_3port = [("P1", "P2", {"P0": "P0", "P2": "P1"})]

_symmetries_crossing = [
    ("P0", "P1", {"P1": "P0", "P2": "P3", "P3": "P2"}),
    ("P0", "P2", {"P1": "P3", "P2": "P1", "P3": "P0"}),
    ("P0", "P3", {"P1": "P2", "P2": "P0", "P3": "P1"}),
]

_symmetries_directional_coupler = [
    ("P0", "P1", {"P1": "P0", "P2": "P3", "P3": "P2"}),
    ("P0", "P2", {"P1": "P3", "P2": "P0", "P3": "P1"}),
    ("P0", "P3", {"P1": "P2", "P2": "P1", "P3": "P0"}),
]

_symmetries_mmi12 = [("P0", "P2", {"P1": "P1", "P2": "P0"})]

_symmetries_mmi22 = _symmetries_directional_coupler

_waist = 5.0

_angle = 8 * math.pi / 180
_vx8 = math.sin(_angle)
_vy8 = -math.cos(_angle)

_angle = 7 * math.pi / 180
_tm1550_vx = math.sin(_angle)
_tm1550_vy = -math.cos(_angle)

_angle = -21 * math.pi / 180
_te1550_vx = math.sin(_angle)
_te1550_vy = -math.cos(_angle)

_angle = -7 * math.pi / 180
_te895_vx = math.sin(_angle)
_te895_vy = -math.cos(_angle)

_component_data = {
    "ANT_MMI_1x2_te1550_3dB_BB": (
        "EBeam_SiN",
        "ANT_MMI_1x2_te1550_3dB_BB",
        [
            ((-12.88, 0.0), 0, "SiN_TE_1550_750"),
            ((12.88, -0.975), 180, "SiN_TE_1550_750"),
            ((12.88, 0.975), 180, "SiN_TE_1550_750"),
        ],
        None,
    ),
    "GC_SiN_TE_1550_8degOxide_BB": (
        "EBeam_SiN",
        "GC_SiN_TE_1550_8degOxide_BB",
        [
            ((0.0, 0.0), 180, "SiN_TE_1550_750"),
            ((-29.7, 0.0), (_vx8, 0, _vy8), _waist, 90),
        ],
        None,
    ),
    "ebeam_MMI_2x2_5050_te1310": (
        "EBeam_SiN",
        "ULaval",
        [
            ((-16.72, -1.2), 0, "SiN_TE_1550_800"),
            ((-16.72, 1.2), 0, "SiN_TE_1550_800"),
            ((16.72, -1.2), 180, "SiN_TE_1550_800"),
            ((16.72, 1.2), 180, "SiN_TE_1550_800"),
        ],
        {"port_symmetries": _symmetries_mmi22},
    ),
    # NOTE: no TE port at 1310 nm with 800 nm
    "ebeam_YBranch_te1310": (
        "EBeam_SiN",
        "ULaval",
        [
            ((-7.69, 0.0), 0, "SiN_TE_1550_800"),
            ((7.69, 0.7), 180, "SiN_TE_1550_800"),
            ((7.69, -0.7), 180, "SiN_TE_1550_800"),
        ],
        {"port_symmetries": _symmetries_3port},
    ),
    "ebeam_BondPad": (
        "EBeam_SiN",
        "ebeam_BondPad",
        [],
        None,
    ),
    "ebeam_DC_2-1_te895": (
        "EBeam_SiN",
        "ebeam_DC_2-1_te895",
        [
            ((-14.56, -2.285), 0, "SiN_TE_895_450"),
            ((-14.56, 2.285), 0, "SiN_TE_895_450"),
            ((14.56, -2.285), 180, "SiN_TE_895_450"),
            ((14.56, 2.285), 180, "SiN_TE_895_450"),
        ],
        {"port_symmetries": _symmetries_directional_coupler},
    ),
    "ebeam_DC_te895": (
        "EBeam_SiN",
        "ebeam_DC_te895",
        [
            ((-14.137, -2.285), 0, "SiN_TE_895_450"),
            ((-14.137, 2.285), 0, "SiN_TE_895_450"),
            ((14.137, -2.285), 180, "SiN_TE_895_450"),
            ((14.137, 2.285), 180, "SiN_TE_895_450"),
        ],
        {"port_symmetries": _symmetries_directional_coupler},
    ),
    # WARN: Missing port (-6.0, 0.0).
    # WARN: Missing port (6.0, 0.0).
    # "ebeam_Polarizer_TM_1550_UQAM": (
    #     "EBeam_SiN",
    #     "ebeam_Polarizer_TM_1550_UQAM",
    #     [],
    #     None,
    # ),
    "ebeam_YBranch_895": (
        "EBeam_SiN",
        "ebeam_YBranch_895",
        [
            ((0.0, 0.0), 0, "SiN_TE_895_450"),
            ((15.0, -2.75), 180, "SiN_TE_895_450"),
            ((15.0, 2.75), 180, "SiN_TE_895_450"),
        ],
        {"port_symmetries": _symmetries_3port},
    ),
    "ebeam_gc_te895": (
        "EBeam_SiN",
        "ebeam_gc_te895",
        [
            ((-24.2, 0.0), 0, "SiN_TE_895_450"),
            ((8, 0), (_te895_vx, 0, _te895_vy), _waist, 90),
        ],
        {"symmetry": (0, -1, 0), "bounds": ((None, -10, None), (25, 10, None))},
    ),
    "ebeam_terminator_SiN_1550": (
        "EBeam_SiN",
        "ebeam_terminator_SiN_1550",
        [((0.0, 0.0), 180, "SiN_TE_1550_750")],
        {},
    ),
    "ebeam_terminator_SiN_te895": (
        "EBeam_SiN",
        "ebeam_terminator_SiN_te895",
        [((0.0, 0.0), 180, "SiN_TE_895_450")],
        {},
    ),
    "taper_SiN_750_3000": (
        "EBeam_SiN",
        "taper_SiN_750_3000",
        [
            ((0.0, 0.0), 0, "SiN_TE_1550_750"),
            ((50.0, 0.0), 180, "MM_SiN_TE_1550_3000"),
        ],
        {},
    ),
    "GC_TE_1310_8degOxide_BB": (
        "EBeam",
        "GCs_BB",
        [
            ((0.0, 0.0), 180, "TE_1310_350"),
            ((-20.4, 0.0), (_vx8, 0, _vy8), _waist, 90),
        ],
        None,
    ),
    "GC_TE_1550_8degOxide_BB": (
        "EBeam",
        "GCs_BB",
        [
            ((0.0, 0.0), 180, "TE_1550_500"),
            ((-20.4, 0.0), (_vx8, 0, _vy8), _waist, 90),
        ],
        None,
    ),
    # NOTE: no TM port with width 350 nm
    "GC_TM_1310_8degOxide_BB": (
        "EBeam",
        "GCs_BB",
        [
            ((0.0, 0.0), 180, "TE_1310_350"),
            ((-20.4, 0.0), (_vx8, 0, _vy8), _waist, 0),
        ],
        None,
    ),
    "GC_TM_1550_8degOxide_BB": (
        "EBeam",
        "GCs_BB",
        [
            ((0.0, 0.0), 180, "TM_1550_500"),
            ((-20.4, 0.0), (_vx8, 0, _vy8), _waist, 0),
        ],
        None,
    ),
    "ebeam_adiabatic_te1550": (
        "EBeam",
        "ebeam_adiabatic_te1550",
        [
            ((0.1, -1.5), 0, "TE_1550_500"),
            ((0.1, 1.5), 0, "TE_1550_500"),
            ((195.9, -1.5), 180, "TE_1550_500"),
            ((195.9, 1.5), 180, "TE_1550_500"),
        ],
        {},
    ),
    "ebeam_adiabatic_tm1550": (
        "EBeam",
        "ebeam_adiabatic_tm1550",
        [
            ((0.1, -1.5), 0, "TM_1550_500"),
            ((0.1, 1.5), 0, "TM_1550_500"),
            ((217.9, -1.5), 180, "TM_1550_500"),
            ((217.9, 1.5), 180, "TM_1550_500"),
        ],
        {},
    ),
    "ebeam_bdc_te1550": (
        "EBeam",
        "ebeam_bdc_te1550",
        [
            ((-35.45, -2.35), 0, "TE_1550_500"),
            ((-35.45, 2.35), 0, "TE_1550_500"),
            ((35.3, -2.35), 180, "TE_1550_500"),
            ((35.3, 2.35), 180, "TE_1550_500"),
        ],
        {},
    ),
    "ebeam_crossing4": (
        "EBeam",
        "ebeam_crossing4",
        [
            ((-4.8, 0.0), 0, "TE_1550_500"),
            ((4.8, 0.0), 180, "TE_1550_500"),
            ((0.0, -4.8), 90, "TE_1550_500"),
            ((0.0, 4.8), 270, "TE_1550_500"),
        ],
        {"port_symmetries": _symmetries_crossing},
    ),
    "ebeam_gc_te1550": (
        "EBeam",
        "ebeam_gc_te1550",
        [
            ((0.0, 0.0), 180, "TE_1550_500"),
            ((-20.4, 0.0), (_te1550_vx, 0, _te1550_vy), _waist, 90),
        ],
        {"symmetry": (0, -1, 0), "bounds": ((-33, -11, None), (None, 11, None))},
    ),
    "ebeam_gc_tm1550": (
        "EBeam",
        "ebeam_gc_tm1550",
        [
            ((0.0, 0.0), 180, "TM_1550_500"),
            ((-24.4, 0.0), (_tm1550_vx, 0, _tm1550_vy), _waist, 0),
        ],
        {"symmetry": (0, 1, 0), "bounds": ((None, -11, None), (None, 11, None))},
    ),
    "ebeam_splitter_swg_assist_te1310": (
        "EBeam",
        "ebeam_splitter_swg_assist_te1310",
        [
            ((-63.001, -2.0), 0, "TE_1310_350"),
            ((-63.001, 2.0), 0, "TE_1310_350"),
            ((63.001, -2.0), 180, "TE_1310_350"),
            ((63.001, 2.0), 180, "TE_1310_350"),
        ],
        {},
    ),
    "ebeam_splitter_swg_assist_te1550": (
        "EBeam",
        "ebeam_splitter_swg_assist_te1550",
        [
            ((-63.001, -1.975), 0, "TE_1550_500"),
            ((-63.001, 1.975), 0, "TE_1550_500"),
            ((63.001, -1.975), 180, "TE_1550_500"),
            ((63.001, 1.975), 180, "TE_1550_500"),
        ],
        {},
    ),
    "ebeam_terminator_te1310": (
        "EBeam",
        "ebeam_terminator_te1310",
        [((0.0, 0.0), 180, "TE_1310_350")],
        {},
    ),
    "ebeam_terminator_te1550": (
        "EBeam",
        "ebeam_terminator_te1550",
        [((0.0, 0.0), 180, "TE_1550_500")],
        {},
    ),
    "ebeam_terminator_tm1550": (
        "EBeam",
        "ebeam_terminator_tm1550",
        [((0.0, 0.0), 180, "TM_1550_500")],
        {},
    ),
    "ebeam_y_1550": (
        "EBeam",
        "ebeam_y_1550",
        [
            ((-7.4, 0.0), 0, "TE_1550_500"),
            ((7.4, -2.75), 180, "TE_1550_500"),
            ((7.4, 2.75), 180, "TE_1550_500"),
        ],
        {"port_symmetries": _symmetries_3port},
    ),
    "ebeam_y_adiabatic": (
        "EBeam",
        "ebeam_y_adiabatic",
        [
            ((0.05, 0.0), 0, "TE-TM_1550_450"),
            ((50.05, -1.25), 180, "TE-TM_1550_450"),
            ((50.05, 1.25), 180, "TE-TM_1550_450"),
        ],
        {"port_symmetries": _symmetries_3port},
    ),
    "ebeam_y_adiabatic_500pin": (
        "EBeam",
        "ebeam_y_adiabatic_500pin",
        [
            ((-1.0, 0.0), 0, "TE_1550_500"),
            ((51.0, -1.25), 180, "TE_1550_500"),
            ((51.0, 1.25), 180, "TE_1550_500"),
        ],
        {"port_symmetries": _symmetries_3port},
    ),
    "taper_si_simm_1310": (
        "EBeam",
        "taper_si_simm_1310",
        # NOTE: no MM TM port at 1310 nm
        [((50.0, 0.0), 180, "MM_TE_1550_3000"), ((0.0, 0.0), 0, "TE_1310_350")],
        {},
    ),
    "taper_si_simm_1550": (
        "EBeam",
        "taper_si_simm_1550",
        [((50.0, 0.0), 180, "MM_TE_1550_3000"), ((0.0, 0.0), 0, "TE_1550_500")],
        {},
    ),
}

component_names = set(_component_data.keys())


def component(
    cell_name: str, technology: pf.Technology = None, tidy3d_model_kwargs: dict = {}
) -> pf.Component:
    """Load a component from the default PDK library.

    Args:
        cell_name (str): Name of the component to load.
        technology (Technology): Technology for the created component.
        tidy3d_model_kwargs (dict): Keyword arguments passed to the Tidy3D
          model of the created component.

    Returns:
        Component: Component loaded from the default PDK library.

    Note:
        The available component names are listed in the module-level tuple
        ``component_names``.
    """
    family, libname, port_data, kwargs = _component_data.get(cell_name, (None, None, None, None))
    if family is None:
        raise KeyError(f"{cell_name} is not a library component.")

    if technology is None:
        technology = pf.config.default_technology
        if not technology.name.startswith("SiEPIC EBeam"):
            warnings.warn(
                f"Current default technology {technology.name} does not seem supported by the "
                "SiEPIC EBeam UW component library",
                RuntimeWarning,
                1,
            )

    # Load library cell
    gdsii = files("siepic_forge") / "library" / family / (libname + ".gds")
    with as_file(gdsii) as fname:
        c = pf.load_layout(fname, technology=technology)[cell_name]

    # Add ports
    z = technology.parametric_kwargs.get("top_oxide_thickness", -1.0)
    if z > 0:
        z += 0.1
    else:
        z = 1.0
    for data in port_data:
        if len(data) == 3:
            port = pf.Port(data[0], data[1], technology.ports[data[2]])
        else:
            port = pf.GaussianPort(
                data[0] + (z,),
                data[1],
                waist_radius=data[2],
                polarization_angle=data[3],
            )
        c.add_port(port)

    # Add model
    if kwargs is not None:
        kwargs = dict(kwargs)
        kwargs.update(tidy3d_model_kwargs)
        c.add_model(pf.Tidy3DModel(**kwargs), "Tidy3D")

    return c
