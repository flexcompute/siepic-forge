import photonforge as pf

_layers = {
    "Si": pf.LayerSpec((1, 0), "SiEPIC - Waveguide", "#ff80a818", ""),
    "PinRec": pf.LayerSpec((1, 10), "SiEPIC", "#ff80a818", ""),
    "PinRecM": pf.LayerSpec((1, 11), "SiEPIC", "#80000018", ""),
    "Si Slab": pf.LayerSpec(
        (2, 0), "Dedicated Run Layers - Device Layer Partial Etch", "#c080ff18", ""
    ),
    "SiN": pf.LayerSpec((4, 0), "Silicon Nitride Full Etch", "#c080ff18", "."),
    "Direct Metal": pf.LayerSpec((5, 0), "Dedicated Run Layers", "#80a8ff18", ""),
    "Oxide open to BOX": pf.LayerSpec((6, 0), "Dedicated Run Layers", "#ff000018", ""),
    "Text": pf.LayerSpec((10, 0), "Text-Not Fabricated", "#00000018", "hollow"),
    "M1_heater": pf.LayerSpec((11, 0), "TiW Heater", "#0000ff18", "\\\\"),
    "M2_router": pf.LayerSpec((12, 0), "TiW/Au Routing Bilayer", "#ffbf0018", "//"),
    "M_Open": pf.LayerSpec((13, 0), "Bond Pad Open", "#80005718", "\\\\"),
    "Si n": pf.LayerSpec((20, 0), "Dedicated Run Layers", "#afff8018", ""),
    "Si p": pf.LayerSpec((21, 0), "Dedicated Run Layers", "#ffd9df18", ""),
    "Si n+": pf.LayerSpec((22, 0), "Dedicated Run Layers", "#ff800018", ""),
    "Si p+": pf.LayerSpec((23, 0), "Dedicated Run Layers", "#ddff0018", ""),
    "Si n++": pf.LayerSpec((24, 0), "Dedicated Run Layers", "#00ffff18", ""),
    "Si p++": pf.LayerSpec((25, 0), "Dedicated Run Layers", "#00800018", ""),
    "ANT Reserved": pf.LayerSpec((31, 0), "SiEPIC/ANT Reserved", "#9580ff18", "/"),
    "ANT Reserved 1": pf.LayerSpec((33, 0), "ANT Reserved", "#9580ff18", "/"),
    "Via to silicon": pf.LayerSpec((40, 0), "Dedicated Run Layers", "#0000ff18", ""),
    "DevRec": pf.LayerSpec((68, 0), "SiEPIC", "#00800018", ""),
    "FbrTgt": pf.LayerSpec((81, 0), "SiEPIC/Dedicated Run Layers", "#80808018", ""),
    "ANT Reserved 2": pf.LayerSpec((102, 0), "ANT Reserved", "#9580ff18", "/"),
    "ANT Reserved 3": pf.LayerSpec((110, 0), "ANT Reserved", "#9580ff18", "/"),
    "Custom Dicing": pf.LayerSpec((189, 0), "", "#00000018", "hollow"),
    "SEM Imaging": pf.LayerSpec((200, 0), "", "#ff000018", "x"),
    "Deep Trench": pf.LayerSpec((201, 0), "", "#00ff0018", "."),
    "Deep Trench Handling Exclusion": pf.LayerSpec((202, 0), "", "#00760018", ":"),
    "Thermal Isolation Trenches": pf.LayerSpec((203, 0), "", "#00800018", "\\"),
    "Laser Integration Shelf": pf.LayerSpec((205, 0), "Dedicated Run Layers", "#69ff0518", ""),
    "Floor Plan-Not Fabricated": pf.LayerSpec((290, 0), "", "#c080ff18", "hollow"),
    "Error: device layer width is less than design rule": pf.LayerSpec(
        (301, 0), "DRC Errors", "#80005718", ""
    ),
    "Error: device layer spacing is less than design rule": pf.LayerSpec(
        (301, 1), "DRC Errors", "#80005718", ""
    ),
    "Warning: polygons/paths on PinRec layer (1/10) will NOT be fabricated": pf.LayerSpec(
        (301, 2), "DRC Errors", "#80005718", ""
    ),
    "Error: direct metal width is less than 5 microns": pf.LayerSpec(
        (305, 0), "DRC Errors", "#80808018", ""
    ),
    "Error: direct metal spacing is less than 10 microns": pf.LayerSpec(
        (305, 1), "DRC Errors", "#80808018", ""
    ),
    "Error: TiW width is less than 3 microns": pf.LayerSpec(
        (311, 0), "DRC Errors", "#ffa08018", ""
    ),
    "Error: TiW spacing is less than 3 microns": pf.LayerSpec(
        (311, 1), "DRC Errors", "#ffa08018", ""
    ),
    "Error: Al width is less than design rule": pf.LayerSpec(
        (312, 0), "DRC Errors", "#00ffff18", ""
    ),
    "Error: Al spacing is less than design rule": pf.LayerSpec(
        (312, 1), "DRC Errors", "#00ffff18", ""
    ),
    "Error: Spacing between TiW and Al is less than 5 microns": pf.LayerSpec(
        (312, 3), "DRC Errors", "#00ffff18", ""
    ),
    "Error: Oxide window width is less than 10 microns": pf.LayerSpec(
        (313, 0), "DRC Errors", "#01ff6b18", ""
    ),
    "Error: Oxide window spacing is less than 10 microns": pf.LayerSpec(
        (313, 1), "DRC Errors", "#01ff6b18", ""
    ),
    "Error: Oxide window is not placed over Al": pf.LayerSpec(
        (313, 2), "DRC Errors", "#01ff6b18", ""
    ),
    "Standard Design Area": pf.LayerSpec((350, 0), "DRC Errors", "#ddff0018", ""),
    "Error: Features outside design area. Verify design size and centering.": pf.LayerSpec(
        (350, 1), "DRC Errors", "#ddff0018", ""
    ),
    "Error: Dicing lane width is less than 100 microns": pf.LayerSpec(
        (389, 0), "DRC Errors", "#ff00ff18", ""
    ),
    "Error: Spacing between dicing lane and devices is less than 50 microns": pf.LayerSpec(
        (389, 1), "DRC Errors", "#ff00ff18", ""
    ),
    "Error: SEM width is less than 500 nm": pf.LayerSpec((400, 0), "DRC Errors", "#ff9d9d18", ""),
    "Deep Trench Design Area": pf.LayerSpec((401, 0), "DRC Errors", "#80a8ff18", ""),
    "Error: Metal, SEM, or handling region overlap with deep trenches. Verify design centering": pf.LayerSpec(
        (401, 1), "DRC Errors", "#80a8ff18", ""
    ),
    "Warning: Silicon features outside deep trench design area. Verify accuracy before submission": pf.LayerSpec(
        (401, 2), "DRC Errors", "#80a8ff18", ""
    ),
    "Error: Spacing between metal and deep trench is less than 30 microns": pf.LayerSpec(
        (401, 3), "DRC Errors", "#80a8ff18", ""
    ),
    "Error: Deep trench width is less than 260 microns": pf.LayerSpec(
        (401, 4), "DRC Errors", "#80a8ff18", ""
    ),
    "Error: Deep trench handling area missing. Please add handling area of size shown by polygons": pf.LayerSpec(
        (402, 0), "DRC Errors", "#ff000018", ""
    ),
    "Error: Features inside deep trench handling area": pf.LayerSpec(
        (402, 1), "DRC Errors", "#ff000018", ""
    ),
    "Error: Thermal isolation width is less than design rule": pf.LayerSpec(
        (403, 0), "DRC Errors", "#50008018", ""
    ),
    "Error: Thermal isolation spacing is less than design rule": pf.LayerSpec(
        (403, 1), "DRC Errors", "#50008018", ""
    ),
    "Error: Spacing between thermal isolation and metal is less than design rule": pf.LayerSpec(
        (403, 2), "DRC Errors", "#50008018", ""
    ),
    "Error: Thermal isolation and device layer overlap, or spacing is less than design rule": pf.LayerSpec(
        (403, 3), "DRC Errors", "#50008018", ""
    ),
    "Dream Photonics Black Box-Not Fabricated": pf.LayerSpec((998, 0), "", "#00000018", "hollow"),
    "Errors": pf.LayerSpec((999, 0), "SiEPIC", "#0000ff18", ""),
}
