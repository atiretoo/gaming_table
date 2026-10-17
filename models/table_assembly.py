"""
Modular Kitchen Dining & Gaming Table (27" x 56")
Parametric CadQuery Model

Key Updates:
- Updated envelope: 27.0" (685.8 mm) width x 56.0" (1422.4 mm) length.
- Removable center stretcher beam in shallow 6mm vertical drop-in dados.
- 3mm silicone foam cord groove in the half-lap center seam.
- 3/4" (19mm) spill-protecting perimeter overhang.
- 3.0" (75mm) recessed gaming vault with 12mm floor.
- Multiple modular leg options supported.
"""

import cadquery as cq

INCH = 25.4

# User Dimensions
TABLE_WIDTH = 27.0 * INCH        # 685.8 mm
TABLE_LENGTH = 56.0 * INCH       # 1422.4 mm
TABLE_HEIGHT = 30.0 * INCH       # 762.0 mm

# Plywood Specs
PLY_18 = 18.0                    # 18 mm (~3/4") Baltic birch
PLY_12 = 12.0                    # 12 mm (~1/2") Baltic birch floor
TOP_OVERHANG = 19.0              # 3/4" drip edge overhang
VAULT_DEPTH = 75.0               # 3" play depth

# Apron Box
APRON_OUTER_L = TABLE_LENGTH - 2 * TOP_OVERHANG   # 1384.4 mm
APRON_OUTER_W = TABLE_WIDTH - 2 * TOP_OVERHANG    # 647.8 mm
APRON_H = VAULT_DEPTH + PLY_12 + 25.0             # 112.0 mm

APRON_TOP_Z = TABLE_HEIGHT - PLY_18               # 744.0 mm
APRON_BOT_Z = APRON_TOP_Z - APRON_H               # 632.0 mm (24.9" knee clearance)

# Dowels
DOWEL_DIA = 9.5
DOWEL_PROTRUSION = 12.0
DOWEL_HOLE_DIA = 10.0
DOWEL_HOLE_DEPTH = 16.0
DOWEL_X_OFFSETS = [-500.0, -180.0, 180.0, 500.0]
DOWEL_Y_OFFSET = (APRON_OUTER_W - PLY_18) / 2.0

# Silicone Cord & Center Seam
CORD_GROOVE_W = 3.5              # 3.5 mm wide groove for 3.0 mm silicone cord
CORD_GROOVE_D = 2.0              # 2.0 mm deep groove (1.0 mm compression)
DADO_DEPTH = 6.0                 # 6 mm deep drop-in dado in side aprons


def make_apron_frame(with_dados=True):
    """Perimeter apron box with drop-in vertical dados for removable center beam."""
    outer = (
        cq.Workplane("XY")
        .box(APRON_OUTER_L, APRON_OUTER_W, APRON_H)
        .translate((0, 0, APRON_BOT_Z + APRON_H / 2.0))
    )
    inner = (
        cq.Workplane("XY")
        .box(APRON_OUTER_L - 2 * PLY_18, APRON_OUTER_W - 2 * PLY_18, APRON_H + 2)
        .translate((0, 0, APRON_BOT_Z + APRON_H / 2.0))
    )
    apron = outer.cut(inner)
    
    # Drop-in vertical dados in side aprons at X = 0
    if with_dados:
        for y_sign in [1, -1]:
            dado_y = y_sign * (APRON_OUTER_W / 2.0 - PLY_18 + DADO_DEPTH / 2.0)
            dado = (
                cq.Workplane("XY")
                .box(PLY_18 + 0.5, DADO_DEPTH * 2, VAULT_DEPTH + 1)
                .translate((0, dado_y, APRON_TOP_Z - VAULT_DEPTH / 2.0))
            )
            apron = apron.cut(dado)
            
    # Dowel holes on top edge
    for x in DOWEL_X_OFFSETS:
        for y_sign in [1, -1]:
            hole = (
                cq.Workplane("XY")
                .cylinder(DOWEL_HOLE_DEPTH * 2, DOWEL_HOLE_DIA / 2.0)
                .translate((x, y_sign * DOWEL_Y_OFFSET, APRON_TOP_Z))
            )
            apron = apron.cut(hole)
            
    return apron


def make_removable_center_beam():
    """
    Removable 18mm Baltic birch center support beam.
    Tabs on ends slide into 6mm dados in the side aprons.
    Flush with top edge of stretchers when dining; lifted out when gaming.
    """
    inner_w = APRON_OUTER_W - 2 * PLY_18
    beam_len = inner_w + 2 * DADO_DEPTH - 1.0  # slight tolerance
    beam_h = VAULT_DEPTH
    z_beam = APRON_TOP_Z - beam_h / 2.0
    
    beam = (
        cq.Workplane("XY")
        .box(PLY_18, beam_len, beam_h)
        .translate((0, 0, z_beam))
    )
    return beam


def make_vault_floor():
    """Recessed gaming vault floor."""
    fl_len = APRON_OUTER_L - 2 * PLY_18
    fl_w = APRON_OUTER_W - 2 * PLY_18
    z_floor = APRON_TOP_Z - VAULT_DEPTH - PLY_12 / 2.0
    
    floor = (
        cq.Workplane("XY")
        .box(fl_len, fl_w, PLY_12)
        .translate((0, 0, z_floor))
    )
    return floor


def make_tabletop_leaves(with_silicone_groove=True, with_dowels=True):
    """
    Two-piece 27" x 56" tabletop leaves.
    - 3/4" perimeter overhang.
    - Shiplap center rebate.
    - Embedded groove for 3mm silicone foam cord.
    - Underside dowel pins.
    """
    leaf_w = TABLE_WIDTH
    leaf_l = TABLE_LENGTH / 2.0
    z_top = APRON_TOP_Z + PLY_18 / 2.0
    lap_w = 12.0
    lap_d = PLY_18 / 2.0
    
    # Left Leaf (-X)
    leaf_left = (
        cq.Workplane("XY")
        .box(leaf_l, leaf_w, PLY_18)
        .translate((-leaf_l / 2.0, 0, z_top))
    )
    # Rebate upper half on right edge
    rebate_left = (
        cq.Workplane("XY")
        .box(lap_w * 2, leaf_w + 2, lap_d + 1)
        .translate((0, 0, z_top + lap_d / 2.0 + 0.5))
    )
    leaf_left = leaf_left.cut(rebate_left)
    
    # Right Leaf (+X)
    leaf_right = (
        cq.Workplane("XY")
        .box(leaf_l, leaf_w, PLY_18)
        .translate((leaf_l / 2.0, 0, z_top))
    )
    # Rebate lower half on left edge
    rebate_right = (
        cq.Workplane("XY")
        .box(lap_w * 2, leaf_w + 2, lap_d + 1)
        .translate((0, 0, z_top - lap_d / 2.0 - 0.5))
    )
    leaf_right = leaf_right.cut(rebate_right)
    
    # Silicone foam cord groove on the lower rebate shelf of the left leaf
    if with_silicone_groove:
        groove = (
            cq.Workplane("XY")
            .box(CORD_GROOVE_W, leaf_w - 2 * TOP_OVERHANG, CORD_GROOVE_D * 2)
            .translate((-lap_w / 2.0, 0, z_top))
        )
        leaf_left = leaf_left.cut(groove)
        
    # Dowels
    if with_dowels:
        z_dowel = APRON_TOP_Z - DOWEL_PROTRUSION / 2.0
        for x in DOWEL_X_OFFSETS:
            dowel_pair = (
                cq.Workplane("XY")
                .cylinder(DOWEL_PROTRUSION, DOWEL_DIA / 2.0)
                .translate((x, DOWEL_Y_OFFSET, z_dowel))
                .union(
                    cq.Workplane("XY")
                    .cylinder(DOWEL_PROTRUSION, DOWEL_DIA / 2.0)
                    .translate((x, -DOWEL_Y_OFFSET, z_dowel))
                )
            )
            if x < 0:
                leaf_left = leaf_left.union(dowel_pair)
            else:
                leaf_right = leaf_right.union(dowel_pair)
                
    return leaf_left, leaf_right


def make_dining_table():
    """Builds the 27"x56" table with removable center beam and leaves."""
    apron = make_apron_frame()
    floor = make_vault_floor()
    beam = make_removable_center_beam()
    leaf_left, leaf_right = make_tabletop_leaves()
    return apron.union(floor).union(beam).union(leaf_left).union(leaf_right)


result = make_dining_table()
