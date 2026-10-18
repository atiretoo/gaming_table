"""
Refined Modular Kitchen Gaming Table with Tapered Legs (Option 3 Final)
Parametric CadQuery Model
"""

import cadquery as cq

INCH = 25.4

# Table Envelope
TABLE_WIDTH = 27.0 * INCH        # 685.8 mm
TABLE_LENGTH = 56.0 * INCH       # 1422.4 mm
TABLE_HEIGHT = 30.0 * INCH       # 762.0 mm

# Plywood Specs
PLY_18 = 18.0                    # 18 mm Baltic birch
PLY_12 = 12.0                    # 12 mm vault floor
VAULT_DEPTH = 75.0               # 3" vault play depth
APRON_H = VAULT_DEPTH + PLY_12   # 87.0 mm

# Recess & Overhang
LEG_SIZE_TOP = 54.0              # 54x54mm at apron shoulder
LEG_SIZE_BOT = 34.0              # 34x34mm at floor (20mm inner taper)
LEG_RECESS = 18.0                # Legs recessed 18mm under leaf perimeter
NOTCH_W = LEG_SIZE_TOP - PLY_18  # 36.0 mm (apron fits into this 36mm shoulder)

APRON_OUTER_L = TABLE_LENGTH - 2 * (LEG_RECESS + NOTCH_W)  # 1314.4 mm
APRON_OUTER_W = TABLE_WIDTH - 2 * (LEG_RECESS + NOTCH_W)   # 577.8 mm

APRON_TOP_Z = TABLE_HEIGHT - PLY_18                # 744.0 mm
APRON_BOT_Z = APRON_TOP_Z - APRON_H                # 657.0 mm
LEG_H = APRON_TOP_Z                                # 744.0 mm

# Accessory Track on Outside Apron Face
TRACK_THROAT_W = 6.4             # 1/4" throat
TRACK_THROAT_D = 4.5             # 4.5 mm depth before T-wings
TRACK_CAVITY_W = 12.7            # 1/2" T-slot width
TRACK_CAVITY_H = 4.8             # 3/16" T-slot height
TRACK_Z = APRON_BOT_Z + APRON_H / 2.0


def make_apron_frame():
    """Apron box with 9mm outer fillet, 2.5mm inner chamfer, and outside T-slot."""
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
    
    # 9mm outer top fillet
    try:
        outer_top_edges = (
            apron.faces(">Z").edges()
            .filter(lambda e: abs(e.Center().x) > (APRON_OUTER_L / 2.0 - 5.0) or
                              abs(e.Center().y) > (APRON_OUTER_W / 2.0 - 5.0))
        )
        apron = outer_top_edges.fillet(9.0)
    except Exception:
        pass
        
    # 2.5mm inner top chamfer
    try:
        inner_top_edges = (
            apron.faces(">Z").edges()
            .filter(lambda e: abs(e.Center().x) < (APRON_OUTER_L / 2.0 - 10.0) and
                              abs(e.Center().y) < (APRON_OUTER_W / 2.0 - 10.0))
        )
        apron = inner_top_edges.chamfer(2.5)
    except Exception:
        pass
        
    # T-slot track along long sides
    for y_sign in [1, -1]:
        y_pos = y_sign * (APRON_OUTER_W / 2.0)
        throat = (
            cq.Workplane("XY")
            .box(APRON_OUTER_L, TRACK_THROAT_D * 2, TRACK_THROAT_W)
            .translate((0, y_pos, TRACK_Z))
        )
        cavity = (
            cq.Workplane("XY")
            .box(APRON_OUTER_L, (TRACK_THROAT_D + 4.0) * 2, TRACK_CAVITY_H)
            .translate((0, y_pos - y_sign * (TRACK_THROAT_D + 2.0), TRACK_Z))
        )
        apron = apron.cut(throat).cut(cavity)
        
    # Drop-in vertical dados at center for removable beam
    for y_sign in [1, -1]:
        dado_y = y_sign * (APRON_OUTER_W / 2.0 - PLY_18 + 3.0)
        dado = (
            cq.Workplane("XY")
            .box(PLY_18 + 0.5, 12.0, VAULT_DEPTH + 1)
            .translate((0, dado_y, APRON_TOP_Z - VAULT_DEPTH / 2.0))
        )
        apron = apron.cut(dado)
        
    return apron


def make_vault_floor():
    fl_len = APRON_OUTER_L - 2 * PLY_18
    fl_w = APRON_OUTER_W - 2 * PLY_18
    z_floor = APRON_TOP_Z - VAULT_DEPTH - PLY_12 / 2.0
    floor = (
        cq.Workplane("XY")
        .box(fl_len, fl_w, PLY_12)
        .translate((0, 0, z_floor))
    )
    return floor


def make_single_tapered_leg():
    """
    Creates a single NE (+X, +Y) corner leg:
    - Outer faces at +X and +Y are straight and vertical (plumb).
    - Top 87mm has inner shoulder notch (36x36mm) for apron.
    - Lower 657mm has inner faces (-X and -Y) tapered from 54mm down to 34mm at floor.
    """
    # Outer corner is at (0, 0)
    # Upper section (Z from APRON_BOT_Z to LEG_H):
    # Full block from (-54, -54) to (0, 0)
    upper = (
        cq.Workplane("XY")
        .box(LEG_SIZE_TOP, LEG_SIZE_TOP, APRON_H)
        .translate((-LEG_SIZE_TOP / 2.0, -LEG_SIZE_TOP / 2.0, APRON_BOT_Z + APRON_H / 2.0))
    )
    # Cut notch from inner corner: (-54, -54) to (-18, -18)
    notch = (
        cq.Workplane("XY")
        .box(NOTCH_W + 1.0, NOTCH_W + 1.0, APRON_H + 2.0)
        .translate((
            -LEG_SIZE_TOP + NOTCH_W / 2.0 - 0.5,
            -LEG_SIZE_TOP + NOTCH_W / 2.0 - 0.5,
            APRON_BOT_Z + APRON_H / 2.0
        ))
    )
    upper_notched = upper.cut(notch)
    
    # Lower tapered section (Z from 0 to APRON_BOT_Z):
    # Outer faces X=0 and Y=0 are stationary.
    # Inner faces taper from (-54, -54) at Z=APRON_BOT_Z to (-34, -34) at Z=0.
    lower = (
        cq.Workplane("XY")
        .workplane(offset=0)
        .polyline([(0, 0), (-LEG_SIZE_BOT, 0), (-LEG_SIZE_BOT, -LEG_SIZE_BOT), (0, -LEG_SIZE_BOT)]).close()
        .workplane(offset=APRON_BOT_Z)
        .polyline([(0, 0), (-LEG_SIZE_TOP, 0), (-LEG_SIZE_TOP, -LEG_SIZE_TOP), (0, -LEG_SIZE_TOP)]).close()
        .loft(combine=True)
    )
    
    return upper_notched.union(lower)


def make_tapered_legs():
    """Generates all 4 tapered corner legs positioned at the apron corners."""
    leg_ne = make_single_tapered_leg()
    
    ox = TABLE_LENGTH / 2.0 - LEG_RECESS
    oy = TABLE_WIDTH / 2.0 - LEG_RECESS
    
    leg_ne = leg_ne.translate((ox, oy, 0))
    leg_nw = leg_ne.mirror("YZ")
    leg_se = leg_ne.mirror("XZ")
    leg_sw = leg_nw.mirror("XZ")
    
    return leg_ne.union(leg_nw).union(leg_se).union(leg_sw)


def make_floating_tabletop(mode="closed"):
    leaf_w = TABLE_WIDTH
    gap = 1.0
    leaf_l = (TABLE_LENGTH - gap) / 2.0
    z_top = APRON_TOP_Z + PLY_18 / 2.0
    
    leaf_left = (
        cq.Workplane("XY")
        .box(leaf_l, leaf_w, PLY_18)
        .translate((-(leaf_l + gap) / 2.0, 0, z_top))
    )
    try:
        outer_bot_edges_l = (
            leaf_left.faces("<Z").edges()
            .filter(lambda e: abs(e.Center().y) > (TABLE_WIDTH / 2.0 - 5.0) or
                              e.Center().x < -(TABLE_LENGTH / 2.0 - 5.0))
        )
        leaf_left = outer_bot_edges_l.chamfer(12.0)
    except Exception:
        pass
        
    if mode == "half":
        return leaf_left
        
    leaf_right = (
        cq.Workplane("XY")
        .box(leaf_l, leaf_w, PLY_18)
        .translate(((leaf_l + gap) / 2.0, 0, z_top))
    )
    try:
        outer_bot_edges_r = (
            leaf_right.faces("<Z").edges()
            .filter(lambda e: abs(e.Center().y) > (TABLE_WIDTH / 2.0 - 5.0) or
                              e.Center().x > (TABLE_LENGTH / 2.0 - 5.0))
        )
        leaf_right = outer_bot_edges_r.chamfer(12.0)
    except Exception:
        pass
        
    return leaf_left.union(leaf_right)


def make_removable_center_beam():
    beam_len = APRON_OUTER_W - 2 * PLY_18 + 12.0
    beam = (
        cq.Workplane("XY")
        .box(PLY_18, beam_len, VAULT_DEPTH)
        .translate((0, 0, APRON_TOP_Z - VAULT_DEPTH / 2.0))
    )
    return beam


def make_tapered_table(mode="closed"):
    apron = make_apron_frame()
    legs = make_tapered_legs()
    floor = make_vault_floor()
    base = apron.union(legs).union(floor)
    
    if mode == "closed":
        top = make_floating_tabletop(mode="closed")
        beam = make_removable_center_beam()
        return base.union(top).union(beam)
    elif mode == "half":
        top = make_floating_tabletop(mode="half")
        beam = make_removable_center_beam()
        return base.union(top).union(beam)
    else:  # "vault"
        return base


result = make_tapered_table(mode="closed")
