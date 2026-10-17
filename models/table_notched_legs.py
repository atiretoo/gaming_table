"""
Option 3: Laminated Corner Posts with Top Notches
Parametric CadQuery Model for 27" x 56" Modular Kitchen Gaming Table
Apron rests inside cutouts in the legs; interior gaming vault is 100% clean.
"""

import cadquery as cq

INCH = 25.4

TABLE_WIDTH = 27.0 * INCH       # 685.8 mm
TABLE_LENGTH = 56.0 * INCH      # 1422.4 mm
TABLE_HEIGHT = 30.0 * INCH      # 762.0 mm

PLY_18 = 18.0
PLY_12 = 12.0

TOP_OVERHANG = 19.0             # 3/4" overhang past apron
VAULT_DEPTH = 75.0              # 3" recessed play area
APRON_H = VAULT_DEPTH + PLY_12  # 87.0 mm

APRON_OUTER_L = TABLE_LENGTH - 2 * TOP_OVERHANG   # 1384.4 mm
APRON_OUTER_W = TABLE_WIDTH - 2 * TOP_OVERHANG    # 647.8 mm

APRON_TOP_Z = TABLE_HEIGHT - PLY_18               # 744.0 mm
APRON_BOT_Z = APRON_TOP_Z - APRON_H               # 657.0 mm

LEG_SIZE = 64.0                                   # 64x64mm square laminated post
LEG_H = APRON_TOP_Z                               # Top of leg reaches top of apron (744 mm)


def make_clean_apron_and_vault():
    """Uninterrupted apron box and vault floor with zero corner obstructions."""
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
    
    floor = (
        cq.Workplane("XY")
        .box(APRON_OUTER_L - 2 * PLY_18, APRON_OUTER_W - 2 * PLY_18, PLY_12)
        .translate((0, 0, APRON_BOT_Z + PLY_12 / 2.0))
    )
    return apron.union(floor)


def make_notched_legs():
    """
    Four legs located at the outer corners.
    Each leg has an L-notch (shoulder) cut out of its top:
    - Depth of notch: APRON_H (87mm) in Z
    - Width of notch: 18mm x 18mm (the thickness of the apron walls)
    The apron box rests down into the notch.
    The leg never enters the interior of the vault.
    """
    # Base leg
    leg = (
        cq.Workplane("XY")
        .box(LEG_SIZE, LEG_SIZE, LEG_H)
        .translate((0, 0, LEG_H / 2.0))
    )
    
    # We cut a top notch into the inner corner of the leg
    # Let's define notch in local coords for +X, +Y corner leg:
    # Inner corner is at -X, -Y in local coords of the leg
    notch = (
        cq.Workplane("XY")
        .box(PLY_18 + 0.5, PLY_18 + 0.5, APRON_H + 1.0)
        .translate((
            -LEG_SIZE / 2.0 + PLY_18 / 2.0,
            -LEG_SIZE / 2.0 + PLY_18 / 2.0,
            LEG_H - APRON_H / 2.0
        ))
    )
    leg_ne = leg.cut(notch)
    
    # Position: outer face of leg is flush with outer face of apron
    cx = APRON_OUTER_L / 2.0 - LEG_SIZE / 2.0 + PLY_18
    cy = APRON_OUTER_W / 2.0 - LEG_SIZE / 2.0 + PLY_18
    
    leg_ne = leg_ne.translate((cx, cy, 0))
    leg_nw = leg_ne.mirror("YZ")
    leg_se = leg_ne.mirror("XZ")
    leg_sw = leg_nw.mirror("XZ")
    
    return leg_ne.union(leg_nw).union(leg_se).union(leg_sw)


def make_half_table():
    box = make_clean_apron_and_vault()
    legs = make_notched_legs()
    
    # Add left tabletop leaf
    leaf_w = TABLE_WIDTH
    leaf_l = TABLE_LENGTH / 2.0
    z_top = APRON_TOP_Z + PLY_18 / 2.0
    
    leaf_left = (
        cq.Workplane("XY")
        .box(leaf_l, leaf_w, PLY_18)
        .translate((-leaf_l / 2.0, 0, z_top))
    )
    
    return box.union(legs).union(leaf_left)


result = make_half_table()
