"""
Option 1: Center Pillar with Spreading Wings (Interlocking Plywood Trestle)
Parametric CadQuery Model for 27" x 56" Modular Kitchen Gaming Table
"""

import cadquery as cq

INCH = 25.4

# Dimensions
TABLE_WIDTH = 27.0 * INCH       # 685.8 mm
TABLE_LENGTH = 56.0 * INCH      # 1422.4 mm
TABLE_HEIGHT = 30.0 * INCH      # 762.0 mm

PLY_18 = 18.0
PLY_36 = 36.0                   # Double-layer laminated 18mm ply for base
PLY_12 = 12.0                   # 12mm vault floor

TOP_OVERHANG = 19.0             # 3/4" overhang
VAULT_DEPTH = 75.0              # 3" vault depth

APRON_OUTER_L = TABLE_LENGTH - 2 * TOP_OVERHANG   # 1384.4 mm
APRON_OUTER_W = TABLE_WIDTH - 2 * TOP_OVERHANG    # 647.8 mm
APRON_H = VAULT_DEPTH + PLY_12                    # 87.0 mm (~3.4")

BASE_TOP_Z = TABLE_HEIGHT - PLY_18 - APRON_H      # Height where base meets bottom of apron = 762 - 18 - 87 = 657 mm
BASE_H = BASE_TOP_Z                               # Base height from floor = 657 mm (~25.9")


def make_apron_and_vault():
    """Clean rectangular apron box and vault floor with zero corner leg obstructions."""
    outer = (
        cq.Workplane("XY")
        .box(APRON_OUTER_L, APRON_OUTER_W, APRON_H)
        .translate((0, 0, BASE_TOP_Z + APRON_H / 2.0))
    )
    inner = (
        cq.Workplane("XY")
        .box(APRON_OUTER_L - 2 * PLY_18, APRON_OUTER_W - 2 * PLY_18, APRON_H + 2)
        .translate((0, 0, BASE_TOP_Z + APRON_H / 2.0))
    )
    apron = outer.cut(inner)
    
    # Floor sits at the bottom of the vault
    floor = (
        cq.Workplane("XY")
        .box(APRON_OUTER_L - 2 * PLY_18, APRON_OUTER_W - 2 * PLY_18, PLY_12)
        .translate((0, 0, BASE_TOP_Z + PLY_12 / 2.0))
    )
    return apron.union(floor)


def make_removable_center_beam():
    """
    Removable center stretcher beam (18mm ply).
    Drops into shallow 6mm deep vertical dados in the side aprons.
    """
    beam_l = APRON_OUTER_W - 2 * PLY_18 + 12.0  # spans inner width plus 6mm into each side dado
    beam = (
        cq.Workplane("XY")
        .box(PLY_18, beam_l, VAULT_DEPTH)
        .translate((0, 0, BASE_TOP_Z + PLY_12 + VAULT_DEPTH / 2.0))
    )
    return beam


def make_pedestal_base():
    """
    Two interlocking double-ply (36mm) wings with sweeping stability profiles.
    - Longitudinal Wing (along X): 920mm floor span x 450mm top span x 657mm height.
    - Transverse Wing (along Y): 580mm floor span x 647mm top span (full apron width) x 657mm height.
    """
    # 1. Transverse wing (along Y, extruded in X by 36mm)
    # Profile in YZ plane
    pts_y = [
        (-290, 0),        # Bottom left foot
        (-250, 40),       # Arch inset
        (0, 70),          # Center arch peak
        (250, 40),
        (290, 0),         # Bottom right foot
        (280, 100),       # Lower taper
        (120, 350),       # Waist
        (APRON_OUTER_W / 2.0, BASE_H),  # Top right arm (spans full apron width)
        (-APRON_OUTER_W / 2.0, BASE_H), # Top left arm
        (-120, 350),      # Left waist
        (-280, 100),
    ]
    # In CadQuery, to draw on YZ plane with positive X extrusion:
    wing_transverse = (
        cq.Workplane("YZ")
        .polyline(pts_y).close()
        .extrude(PLY_36)
        .translate((-PLY_36 / 2.0, 0, 0))
    )
    
    # 2. Longitudinal wing (along X, extruded in Y by 36mm)
    # Profile in XZ plane (using ZX forward cyclic workplane to avoid reverse normal)
    # On "ZX", local X = Global Z, local Y = Global X
    # Or start on XY and extrude in Z, or draw in ZX:
    # Let's draw in ZX: coordinates are (z, x)
    pts_zx = [
        (0, -460),       # Bottom left foot (-X)
        (40, -400),
        (70, 0),         # Center arch
        (40, 400),
        (0, 460),        # Bottom right foot (+X)
        (100, 440),
        (350, 180),      # Waist
        (BASE_H, 250),   # Top arm (+X)
        (BASE_H, -250),  # Top arm (-X)
        (350, -180),
        (100, -440),
    ]
    wing_longitudinal = (
        cq.Workplane("ZX")
        .polyline(pts_zx).close()
        .extrude(PLY_36)
        .translate((0, -PLY_36 / 2.0, 0))
    )
    
    return wing_transverse.union(wing_longitudinal)


def make_tabletop(half_open=False):
    """27x56 tabletop with 3/4" overhang and center half-lap."""
    leaf_w = TABLE_WIDTH
    leaf_l = TABLE_LENGTH / 2.0
    z_top = TABLE_HEIGHT - PLY_18 / 2.0
    
    leaf_left = (
        cq.Workplane("XY")
        .box(leaf_l, leaf_w, PLY_18)
        .translate((-leaf_l / 2.0, 0, z_top))
    )
    if half_open:
        return leaf_left
        
    leaf_right = (
        cq.Workplane("XY")
        .box(leaf_l, leaf_w, PLY_18)
        .translate((leaf_l / 2.0, 0, z_top))
    )
    return leaf_left.union(leaf_right)


def make_full_pedestal_table(mode="closed"):
    apron_vault = make_apron_and_vault()
    base = make_pedestal_base()
    table = apron_vault.union(base)
    
    if mode == "closed":
        beam = make_removable_center_beam()
        top = make_tabletop(half_open=False)
        return table.union(beam).union(top)
    elif mode == "half":
        beam = make_removable_center_beam()
        top = make_tabletop(half_open=True)
        return table.union(beam).union(top)
    elif mode == "vault":
        # In vault mode: leaves and center beam removed!
        return table
    return table


result = make_full_pedestal_table(mode="half")
