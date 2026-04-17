import math

_symmetries_3port = [("P1", "P2", {"P0": "P0", "P2": "P1"})]

_symmetries_crossing = [
    ("P0", "P1", {"P1": "P0", "P2": "P3", "P3": "P2"}),
    ("P0", "P2", {"P1": "P3", "P2": "P1", "P3": "P0"}),
    ("P0", "P3", {"P1": "P2", "P2": "P0", "P3": "P1"}),
]

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

_component_data = {
    "GC_TE_1310_8degOxide_BB": (
        "GCs_BB",
        [
            ((0.0, 0.0), 180, "TE_1310_350"),
            ((-20.4, 0.0), (_vx8, 0, _vy8), _waist, 90),
        ],
        None,
        "grating-coupler",
    ),
    "GC_TE_1550_8degOxide_BB": (
        "GCs_BB",
        [
            ((0.0, 0.0), 180, "TE_1550_500"),
            ((-20.4, 0.0), (_vx8, 0, _vy8), _waist, 90),
        ],
        None,
        "grating-coupler",
    ),
    "GC_TM_1310_8degOxide_BB": (
        "GCs_BB",
        [
            ((0.0, 0.0), 180, "TM_1310_350"),
            ((-20.4, 0.0), (_vx8, 0, _vy8), _waist, 0),
        ],
        None,
        "grating-coupler",
    ),
    "GC_TM_1550_8degOxide_BB": (
        "GCs_BB",
        [
            ((0.0, 0.0), 180, "TM_1550_500"),
            ((-20.4, 0.0), (_vx8, 0, _vy8), _waist, 0),
        ],
        None,
        "grating_coupler",
    ),
    "ebeam_adiabatic_te1550": (
        "ebeam_adiabatic_te1550",
        [
            ((0.1, -1.5), 0, "TE_1550_500"),
            ((0.1, 1.5), 0, "TE_1550_500"),
            ((195.9, -1.5), 180, "TE_1550_500"),
            ((195.9, 1.5), 180, "TE_1550_500"),
        ],
        {},
        "dc",
    ),
    "ebeam_adiabatic_tm1550": (
        "ebeam_adiabatic_tm1550",
        [
            ((0.1, -1.5), 0, "TM_1550_500"),
            ((0.1, 1.5), 0, "TM_1550_500"),
            ((217.9, -1.5), 180, "TM_1550_500"),
            ((217.9, 1.5), 180, "TM_1550_500"),
        ],
        {},
        "dc",
    ),
    "ebeam_bdc_te1550": (
        "ebeam_bdc_te1550",
        [
            ((-35.45, -2.35), 0, "TE_1550_500"),
            ((-35.45, 2.35), 0, "TE_1550_500"),
            ((35.3, -2.35), 180, "TE_1550_500"),
            ((35.3, 2.35), 180, "TE_1550_500"),
        ],
        {},
        "dc",
    ),
    "ebeam_crossing4": (
        "ebeam_crossing4",
        [
            ((-4.8, 0.0), 0, "TE_1550_500"),
            ((4.8, 0.0), 180, "TE_1550_500"),
            ((0.0, -4.8), 90, "TE_1550_500"),
            ((0.0, 4.8), 270, "TE_1550_500"),
        ],
        {"port_symmetries": _symmetries_crossing},
        "crossing",
    ),
    "ebeam_gc_te1550": (
        "ebeam_gc_te1550",
        [
            ((0.0, 0.0), 180, "TE_1550_500"),
            ((-20.4, 0.0), (_te1550_vx, 0, _te1550_vy), _waist, 90),
        ],
        {"symmetry": (0, -1, 0), "bounds": ((-33, -11, None), (None, 11, None))},
        "grating_coupler",
    ),
    "ebeam_gc_tm1550": (
        "ebeam_gc_tm1550",
        [
            ((0.0, 0.0), 180, "TM_1550_500"),
            ((-24.4, 0.0), (_tm1550_vx, 0, _tm1550_vy), _waist, 0),
        ],
        {"symmetry": (0, 1, 0), "bounds": ((None, -11, None), (None, 11, None))},
        "grating_coupler",
    ),
    "ebeam_routing_taper_te1550_w=500nm_to_w=3000nm_L=20um": (
        "ebeam_routing_taper_te1550_w=500nm_to_w=3000nm_L=20um",
        [
            ((0.0, 0.0), 0, "TE_1550_500"),
            ((20.0, 0.0), 180, "MM_TE_1550_3000"),
        ],
        {},
        "taper",
    ),
    "ebeam_routing_taper_te1550_w=500nm_to_w=3000nm_L=40um": (
        "ebeam_routing_taper_te1550_w=500nm_to_w=3000nm_L=40um",
        [
            ((0.0, 0.0), 0, "TE_1550_500"),
            ((40.0, 0.0), 180, "MM_TE_1550_3000"),
        ],
        {},
        "taper",
    ),
    "ebeam_splitter_swg_assist_te1310": (
        "ebeam_splitter_swg_assist_te1310",
        [
            ((-63.001, -2.0), 0, "TE_1310_350"),
            ((-63.001, 2.0), 0, "TE_1310_350"),
            ((63.001, -2.0), 180, "TE_1310_350"),
            ((63.001, 2.0), 180, "TE_1310_350"),
        ],
        {},
        "dc",
    ),
    "ebeam_splitter_swg_assist_te1550": (
        "ebeam_splitter_swg_assist_te1550",
        [
            ((-63.001, -1.975), 0, "TE_1550_500"),
            ((-63.001, 1.975), 0, "TE_1550_500"),
            ((63.001, -1.975), 180, "TE_1550_500"),
            ((63.001, 1.975), 180, "TE_1550_500"),
        ],
        {},
        "dc",
    ),
    "ebeam_terminator_te1310": (
        "ebeam_terminator_te1310",
        [((0.0, 0.0), 180, "TE_1310_350")],
        {},
        "termination",
    ),
    "ebeam_terminator_te1550": (
        "ebeam_terminator_te1550",
        [((0.0, 0.0), 180, "TE_1550_500")],
        {},
        "termination",
    ),
    "ebeam_terminator_tm1550": (
        "ebeam_terminator_tm1550",
        [((0.0, 0.0), 180, "TM_1550_500")],
        {},
        "termination",
    ),
    "ebeam_y_1310": (
        "ebeam_y_1310",
        [
            ((-9.4, 0.0), 0, "TE_1310_350"),
            ((9.4, -2.75), 180, "TE_1310_350"),
            ((9.4, 2.75), 180, "TE_1310_350"),
        ],
        {"port_symmetries": _symmetries_3port},
        "y-splitter",
    ),
    "ebeam_y_1550": (
        "ebeam_y_1550",
        [
            ((-7.4, 0.0), 0, "TE_1550_500"),
            ((7.4, -2.75), 180, "TE_1550_500"),
            ((7.4, 2.75), 180, "TE_1550_500"),
        ],
        {"port_symmetries": _symmetries_3port},
        "y-splitter",
    ),
    "ebeam_y_adiabatic": (
        "ebeam_y_adiabatic",
        [
            ((0.05, 0.0), 0, "TE-TM_1550_450"),
            ((50.05, -1.25), 180, "TE-TM_1550_450"),
            ((50.05, 1.25), 180, "TE-TM_1550_450"),
        ],
        {"port_symmetries": _symmetries_3port},
        "y-splitter",
    ),
    "ebeam_y_adiabatic_500pin": (
        "ebeam_y_adiabatic_500pin",
        [
            ((-1.0, 0.0), 0, "TE_1550_500"),
            ((51.0, -1.25), 180, "TE_1550_500"),
            ((51.0, 1.25), 180, "TE_1550_500"),
        ],
        {"port_symmetries": _symmetries_3port},
        "y-splitter",
    ),
    "taper_si_simm_1310": (
        "taper_si_simm_1310",
        [((50.0, 0.0), 180, "MM_TE_1550_3000"), ((0.0, 0.0), 0, "TE_1310_350")],
        {},
        "taper",
    ),
    "taper_si_simm_1550": (
        "taper_si_simm_1550",
        [((50.0, 0.0), 180, "MM_TE_1550_3000"), ((0.0, 0.0), 0, "TE_1550_500")],
        {},
        "taper",
    ),
}
