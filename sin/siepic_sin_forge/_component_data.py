import math

_symmetries_3port = [("P1", "P2", {"P0": "P0", "P2": "P1"})]

_symmetries_crossing = [
    ("P0", "P1", {"P1": "P0", "P2": "P3", "P3": "P2"}),
    ("P2", "P3", {"P0": "P1", "P1": "P0", "P3": "P2"}),
]

_symmetries_directional_coupler = [
    ("P0", "P1", {"P1": "P0", "P2": "P3", "P3": "P2"}),
    ("P0", "P2", {"P1": "P3", "P2": "P0", "P3": "P1"}),
    ("P0", "P3", {"P1": "P2", "P2": "P1", "P3": "P0"}),
]

_symmetries_mmi22 = _symmetries_directional_coupler

_waist = 5.0

_angle = 8 * math.pi / 180
_vx8 = math.sin(_angle)
_vy8 = -math.cos(_angle)

_angle = 10 * math.pi / 180
_te895_vx = math.sin(_angle)
_te895_vy = -math.cos(_angle)

_component_data = {
    "ANT_MMI_1x2_te1550_3dB_BB": (
        "ANT_MMI_1x2_te1550_3dB_BB",
        [
            ((-12.88, 0.0), 0, "SiN_TE_1550_750"),
            ((12.88, -0.975), 180, "SiN_TE_1550_750"),
            ((12.88, 0.975), 180, "SiN_TE_1550_750"),
        ],
        None,
        "mmi1x2",
    ),
    "GC_SiN_TE_1310_8degOxide_BB": (
        "GC_SiN_TE_1310_8degOxide_BB",
        [
            ((0.0, 0.0), 180, "SiN_TE_1310_750"),
            ((-29.7, 0.0), (_vx8, 0, _vy8), _waist, 90),
        ],
        None,
        "grating_coupler",
    ),
    "GC_SiN_TE_1550_8degOxide_BB": (
        "GC_SiN_TE_1550_8degOxide_BB",
        [
            ((0.0, 0.0), 180, "SiN_TE_1550_750"),
            ((-29.7, 0.0), (_vx8, 0, _vy8), _waist, 90),
        ],
        None,
        "grating_coupler",
    ),
    "ebeam_MMI_2x2_5050_te1310": (
        "ULaval",
        [
            ((-16.72, -1.2), 0, "SiN_TE_1550_800"),
            ((-16.72, 1.2), 0, "SiN_TE_1550_800"),
            ((16.72, -1.2), 180, "SiN_TE_1550_800"),
            ((16.72, 1.2), 180, "SiN_TE_1550_800"),
        ],
        {"port_symmetries": _symmetries_mmi22},
        "mmi2x2",
    ),
    "ebeam_YBranch_te1310": (
        "ULaval",
        [
            ((-7.69, 0.0), 0, "SiN_TE_1310_800"),
            ((15.5, -1.0), 180, "SiN_TE_1310_800"),
            ((15.5, 1.0), 180, "SiN_TE_1310_800"),
        ],
        {"port_symmetries": _symmetries_3port},
        "y-splitter",
    ),
    "crossing_horizontal": (
        "crossing_horizontal",
        [
            ((-37.83, -17.12), 0, "SiN_TE_1550_750"),
            ((-37.83, 17.12), 0, "SiN_TE_1550_750"),
            ((37.83, -17.12), 180, "SiN_TE_1550_750"),
            ((37.83, 17.12), 180, "SiN_TE_1550_750"),
        ],
        {"port_symmetries": _symmetries_directional_coupler},
        "crossing",
    ),
    "crossing_manhattan": (
        "crossing_manhattan",
        [
            ((-3.5, 0.0), 0, "SiN_TE_1550_750"),
            ((3.5, 0.0), 180, "SiN_TE_1550_750"),
            ((0.0, -3.5), 90, "SiN_TE_1550_750"),
            ((0.0, 3.5), 270, "SiN_TE_1550_750"),
        ],
        {"port_symmetries": _symmetries_crossing},
        "crossing",
    ),
    "ebeam_BondPad": (
        "ebeam_BondPad",
        [((0, 0), (100, 100), "M2_router")],
        None,
        "bondpad",
    ),
    "ebeam_DC_2-1_te895": (
        "ebeam_DC_2-1_te895",
        [
            ((-14.56, -2.285), 0, "SiN_TE_895_450"),
            ((-14.56, 2.285), 0, "SiN_TE_895_450"),
            ((14.56, -2.285), 180, "SiN_TE_895_450"),
            ((14.56, 2.285), 180, "SiN_TE_895_450"),
        ],
        {"port_symmetries": _symmetries_directional_coupler},
        "dc",
    ),
    "ebeam_DC_te895": (
        "ebeam_DC_te895",
        [
            ((-14.137, -2.285), 0, "SiN_TE_895_450"),
            ((-14.137, 2.285), 0, "SiN_TE_895_450"),
            ((14.137, -2.285), 180, "SiN_TE_895_450"),
            ((14.137, 2.285), 180, "SiN_TE_895_450"),
        ],
        {"port_symmetries": _symmetries_directional_coupler},
        "dc",
    ),
    "ebeam_Polarizer_TM_1550_UQAM": (
        "ebeam_Polarizer_TM_1550_UQAM",
        [((-6.0, 0.0), 0, "SiN_TE-TM_1550_1000"), ((6.0, 0.0), 180, "SiN_TE-TM_1550_1000")],
        {},
        "transition",
    ),
    "ebeam_YBranch_895": (
        "ebeam_YBranch_895",
        [
            ((0.0, 0.0), 0, "SiN_TE_895_450"),
            ((15.0, -2.75), 180, "SiN_TE_895_450"),
            ((15.0, 2.75), 180, "SiN_TE_895_450"),
        ],
        {"port_symmetries": _symmetries_3port},
        "y-splitter",
    ),
    "ebeam_gc_te895": (
        "ebeam_gc_te895",
        [
            ((0.0, 0.0), 180, "SiN_TE_895_450"),
            ((-29.0, 0), (_te895_vx, 0, _te895_vy), _waist, 90),
        ],
        {"symmetry": (0, -1, 0), "bounds": ((None, -10, None), (None, 10, None))},
        "grating_coupler",
    ),
    "ebeam_terminator_SiN_1310": (
        "ebeam_terminator_SiN_1310",
        [((0.0, 0.0), 180, "SiN_TE_1310_800")],
        {},
        "termination",
    ),
    "ebeam_terminator_SiN_1550": (
        "ebeam_terminator_SiN_1550",
        [((0.0, 0.0), 180, "SiN_TE_1550_750")],
        {},
        "termination",
    ),
    "ebeam_terminator_SiN_te895": (
        "ebeam_terminator_SiN_te895",
        [((0.0, 0.0), 180, "SiN_TE_895_450")],
        {},
        "termination",
    ),
    "port_SiN_800": (
        "port_SiN_800",
        [((1.0, 0.0), 180, "SiN_TE_1550_800")],
        {},
        "termination",
    ),
    "taper_SiN_750_3000": (
        "taper_SiN_750_3000",
        [((0.0, 0.0), 0, "SiN_TE_1550_750"), ((50.0, 0.0), 180, "MM_SiN_TE_1550_3000")],
        {},
        "taper",
    ),
    "taper_SiN_750_800": (
        "taper_SiN_750_800",
        [((0.0, 0.0), 0, "SiN_TE_1550_800"), ((2.0, 0.0), 180, "SiN_TE_1550_750")],
        {},
        "taper",
    ),
}
