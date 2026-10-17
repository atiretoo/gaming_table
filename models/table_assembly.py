"""
Modular Kitchen Dining & Gaming Table
Parametric CadQuery Model

Designed for compact kitchens / multi-use living:
- 30" (762mm) short end: narrowest width for a comfortable single place setting.
- 60" (1524mm) long side: exactly 2x width (maximum 60").
- Standard 30" dining height with 24.9" under-apron knee clearance.
- 3" (75mm) deep recessed gaming vault with 1/2" Baltic birch floor (fits playmat/felt).
- Continuous perimeter apron box with heavy-duty diagonal corner blocks.
- Detachable laminated Baltic birch legs (64x64mm) secured with knock-down bolts.
- Center cross-stretcher supporting the two-piece leaf seam and resisting racking.
- Two-piece removable top with 3/4" (19mm) perimeter overhang shielding stretchers from spills.
- Shiplap center seam with protective overlap to stop spills between leaves.
- Drop-in locating dowel pins on leaves with mating receiver holes in stretchers.
"""

import cadquery as cq

# ==============================================================================
# Parametric Dimensions (all internal units in mm)
# ==============================================================================
INCH = 25.4

# User Configurable Table Envelope
TABLE_WIDTH = 30.0 * INCH        # 762.0 mm (short end, 1 diner)
TABLE_LENGTH = 60.0 * INCH       # 1524.0 mm (long side, 2x width, max 60")
TABLE_HEIGHT = 30.0 * INCH       # 762.0 mm (standard dining table height)

# Material Specifications (Baltic Birch Plywood)
PLY_18 = 18.0                    # 18 mm (~3/4") BB ply for stretchers, leaves, legs
PLY_12 = 12.0                    # 12 mm (~1/2") BB ply for gaming vault floor
EDGE_BAND = 3.0                  # 3 mm solid hardwood edge banding on leaves

# Gaming Vault & Overhang
TOP_OVERHANG = 19.0              # 3/4" drip edge past stretchers (protects from spills)
VAULT_DEPTH = 75.0               # Recessed play area depth (~3")

# Perimeter Apron Box
APRON_OUTER_L = TABLE_LENGTH - 2 * TOP_OVERHANG   # 1486.0 mm
APRON_OUTER_W = TABLE_WIDTH - 2 * TOP_OVERHANG    # 724.0 mm
APRON_H = VAULT_DEPTH + PLY_12 + 25.0             # 112.0 mm (~4.4")

APRON_TOP_Z = TABLE_HEIGHT - PLY_18               # 744.0 mm
APRON_BOT_Z = APRON_TOP_Z - APRON_H               # 632.0 mm (24.9" knee clearance)

# Legs
LEG_SIZE = 64.0                  # 64 x 64 mm square laminated ply
LEG_H = APRON_TOP_Z              # 744.0 mm

# Dowel Alignment System
DOWEL_DIA = 9.5                  # 3/8" dowels
DOWEL_PROTRUSION = 12.0          # Extends 12mm below leaf into stretcher
DOWEL_HOLE_DIA = 10.0            # 10mm hole (slip fit with 0.5mm clearance)
DOWEL_HOLE_DEPTH = 16.0          # 16mm deep blind hole in stretcher top edge

# Dowel coordinate offsets along long stretchers (relative to table center)
DOWEL_X_OFFSETS = [-550.0, -200.0, 200.0, 550.0]
DOWEL_Y_OFFSET = (APRON_OUTER_W - PLY_18) / 2.0


# ==============================================================================
# Component Generators
# ==============================================================================

def make_apron_frame(with_dowel_holes=True):
    """
    Creates the continuous perimeter apron box, center cross-stretcher,
    and precision blind dowel holes along the top edge of the long stretchers.
    """
    outer_box = (
        cq.Workplane("XY")
        .box(APRON_OUTER_L, APRON_OUTER_W, APRON_H)
        .translate((0, 0, APRON_BOT_Z + APRON_H / 2.0))
    )
    inner_box = (
        cq.Workplane("XY")
        .box(APRON_OUTER_L - 2 * PLY_18, APRON_OUTER_W - 2 * PLY_18, APRON_H + 2)
        .translate((0, 0, APRON_BOT_Z + APRON_H / 2.0))
    )
    apron = outer_box.cut(inner_box)
    
    # Center cross-stretcher supporting leaf center seam
    center_stretcher = (
        cq.Workplane("XY")
        .box(PLY_18, APRON_OUTER_W - 2 * PLY_18, APRON_H)
        .translate((0, 0, APRON_BOT_Z + APRON_H / 2.0))
    )
    apron = apron.union(center_stretcher)
    
    # Drill dowel holes on top edge
    if with_dowel_holes:
        for x in DOWEL_X_OFFSETS:
            for y_sign in [1, -1]:
                hole = (
                    cq.Workplane("XY")
                    .cylinder(DOWEL_HOLE_DEPTH * 2, DOWEL_HOLE_DIA / 2.0)
                    .translate((x, y_sign * DOWEL_Y_OFFSET, APRON_TOP_Z))
                )
                apron = apron.cut(hole)
                
    return apron


def make_corner_blocks():
    """
    Modular knock-down diagonal corner braces.
    Secures each leg into the apron corner with bolts into threaded inserts.
    """
    block_size = 90.0
    block_h = APRON_H - 12.0
    z_pos = APRON_BOT_Z + 6.0
    
    pts = [(0, 0), (block_size, 0), (0, block_size)]
    brace = (
        cq.Workplane("XY")
        .polyline(pts).close()
        .extrude(block_h)
        .translate((0, 0, z_pos))
    )
    inner_pts = [(PLY_18, PLY_18), (block_size - 12, PLY_18), (PLY_18, block_size - 12)]
    brace_cutout = (
        cq.Workplane("XY")
        .polyline(inner_pts).close()
        .extrude(block_h + 2)
        .translate((0, 0, z_pos - 1))
    )
    corner_bracket = brace.cut(brace_cutout)
    
    cx = APRON_OUTER_L / 2.0 - PLY_18
    cy = APRON_OUTER_W / 2.0 - PLY_18
    
    b_ne = corner_bracket.rotate((0, 0, 0), (0, 0, 1), 180).translate((cx, cy, 0))
    b_nw = corner_bracket.rotate((0, 0, 0), (0, 0, 1), 270).translate((-cx, cy, 0))
    b_se = corner_bracket.rotate((0, 0, 0), (0, 0, 1), 90).translate((cx, -cy, 0))
    b_sw = corner_bracket.translate((-cx, -cy, 0))
    
    return b_ne.union(b_nw).union(b_se).union(b_sw)


def make_legs():
    """
    Four detachable legs positioned neatly inside the corners of the apron box.
    """
    leg = (
        cq.Workplane("XY")
        .box(LEG_SIZE, LEG_SIZE, LEG_H)
        .translate((0, 0, LEG_H / 2.0))
    )
    
    dx = APRON_OUTER_L / 2.0 - PLY_18 - LEG_SIZE / 2.0
    dy = APRON_OUTER_W / 2.0 - PLY_18 - LEG_SIZE / 2.0
    
    legs = (
        leg.translate((dx, dy, 0))
        .union(leg.translate((-dx, dy, 0)))
        .union(leg.translate((dx, -dy, 0)))
        .union(leg.translate((-dx, -dy, 0)))
    )
    return legs


def make_vault_floor():
    """
    Recessed play surface floor supported on interior ledger cleats.
    Sits VAULT_DEPTH below the top edge of the apron stretchers.
    """
    floor_l = APRON_OUTER_L - 2 * PLY_18
    floor_w = APRON_OUTER_W - 2 * PLY_18
    z_floor = APRON_TOP_Z - VAULT_DEPTH - PLY_12 / 2.0
    
    floor = (
        cq.Workplane("XY")
        .box(floor_l, floor_w, PLY_12)
        .translate((0, 0, z_floor))
    )
    
    # Corner leg clearance cutouts
    for sx in [1, -1]:
        for sy in [1, -1]:
            notch = (
                cq.Workplane("XY")
                .box(LEG_SIZE + 0.5, LEG_SIZE + 0.5, PLY_12 + 2)
                .translate((
                    sx * (floor_l / 2.0 - LEG_SIZE / 2.0),
                    sy * (floor_w / 2.0 - LEG_SIZE / 2.0),
                    z_floor
                ))
            )
            floor = floor.cut(notch)
            
    return floor


def make_tabletop_leaves(gap=1.5, with_dowels=True):
    """
    Two-piece removable dining tabletop leaves.
    Features:
    - 3/4" (19mm) perimeter overhang shielding stretchers from spills.
    - Shiplap center rebate preventing spills through center seam.
    - Underside dowels fitting into apron holes.
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
    # Rebate upper half along center meeting edge
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
    # Rebate lower half along center meeting edge
    rebate_right = (
        cq.Workplane("XY")
        .box(lap_w * 2, leaf_w + 2, lap_d + 1)
        .translate((0, 0, z_top - lap_d / 2.0 - 0.5))
    )
    leaf_right = leaf_right.cut(rebate_right)
    
    # Add dowels under each leaf
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
                
    return leaf_left.union(leaf_right)


# ==============================================================================
# Complete Assembly Selector
# ==============================================================================

def make_table(mode="closed"):
    """
    Builds the table in desired configuration:
    - 'closed': Complete dining table with both top leaves in place.
    - 'half': Transition view with one leaf in place and one removed.
    - 'vault': Open gaming vault configuration (both leaves removed).
    """
    aprons = make_apron_frame()
    corner_blocks = make_corner_blocks()
    legs = make_legs()
    vault = make_vault_floor()
    base = aprons.union(corner_blocks).union(legs).union(vault)
    
    if mode == "closed":
        leaves = make_tabletop_leaves(gap=1.0, with_dowels=True)
        return base.union(leaves)
    elif mode == "half":
        leaf_w = TABLE_WIDTH
        leaf_l = TABLE_LENGTH / 2.0
        z_top = APRON_TOP_Z + PLY_18 / 2.0
        lap_w = 12.0
        lap_d = PLY_18 / 2.0
        
        leaf_left = (
            cq.Workplane("XY")
            .box(leaf_l, leaf_w, PLY_18)
            .translate((-leaf_l / 2.0, 0, z_top))
        )
        rebate_left = (
            cq.Workplane("XY")
            .box(lap_w * 2, leaf_w + 2, lap_d + 1)
            .translate((0, 0, z_top + lap_d / 2.0 + 0.5))
        )
        leaf_left = leaf_left.cut(rebate_left)
        return base.union(leaf_left)
    else:  # "vault"
        return base


result = make_table(mode="closed")

if __name__ == "__main__":
    print(f"Table Width:  {TABLE_WIDTH/INCH:.1f}\" ({TABLE_WIDTH:.1f} mm)")
    print(f"Table Length: {TABLE_LENGTH/INCH:.1f}\" ({TABLE_LENGTH:.1f} mm)")
    print(f"Table Height: {TABLE_HEIGHT/INCH:.1f}\" ({TABLE_HEIGHT:.1f} mm)")
    print(f"Apron Size:   {APRON_OUTER_L/INCH:.1f}\" L x {APRON_OUTER_W/INCH:.1f}\" W")
    print(f"Vault Depth:  {VAULT_DEPTH/INCH:.1f}\" ({VAULT_DEPTH:.1f} mm)")
    print(f"Knee Room:    {APRON_BOT_Z/INCH:.1f}\" ({APRON_BOT_Z:.1f} mm)")
