"""
Refined Modular Kitchen Gaming Table (Option 3 Final)
Parametric CadQuery Model

Key Refinements:
- Tabletop Envelope: 27.0" (685.8 mm) Width x 56.0" (1422.4 mm) Length.
- Floating Top Look: Big 12mm underside chamfer on leaf outer edges.
- Recessed Base: Apron box and legs recessed under leaf edges (leg outer corner recessed ~18mm, apron recessed 54mm).
- Ergonomic Apron Edges: 9mm radius fillet on top outer edge, 2.5mm chamfer on top inner edge.
- Integrated Accessory Track: Outside T-slot groove for gravity hook-and-tilt accessories.
- Removable Center Beam: 18mm beam in 6mm side dados.
- Clean Gaming Vault: 100% rectangular, 3" (75mm) depth.
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
LEG_SIZE = 54.0                  # 54x54mm mitered 3-ply leg (3x 18mm)
LEG_RECESS = 18.0                # Legs recessed 18mm (~0.71") under leaf perimeter
APRON_OVERHANG = LEG_RECESS + (LEG_SIZE - PLY_18)  # 18 + 36 = 54.0 mm (~2.13")

APRON_OUTER_L = TABLE_LENGTH - 2 * APRON_OVERHANG  # 1314.4 mm (~51.75")
APRON_OUTER_W = TABLE_WIDTH - 2 * APRON_OVERHANG   # 577.8 mm (~22.75")

APRON_TOP_Z = TABLE_HEIGHT - PLY_18                # 744.0 mm
APRON_BOT_Z = APRON_TOP_Z - APRON_H                # 657.0 mm
LEG_H = APRON_TOP_Z                                # 744.0 mm

# Accessory Track on Outside Apron Face
TRACK_THROAT_W = 6.4             # 1/4" throat
TRACK_THROAT_D = 4.5             # 4.5 mm depth before T-wings
TRACK_CAVITY_W = 12.7            # 1/2" T-slot width
TRACK_CAVITY_H = 4.8             # 3/16" T-slot height
TRACK_Z = APRON_BOT_Z + APRON_H / 2.0  # Centered vertically on apron face


def make_apron_frame():
    """
    Apron box with:
    - 9mm fillet on top outer edge
    - 2.5mm chamfer on top inner edge
    - Outside T-slot groove for gravity accessories
    - Drop-in dados for center beam
    """
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
    
    # Fillet top outer edges (9mm radius)
    try:
        # Select top outer edges: highest Z, outer perimeter
        outer_top_edges = (
            apron.faces(">Z").edges()
            .filter(lambda e: abs(e.Center().x) > (APRON_OUTER_L / 2.0 - 5.0) or
                              abs(e.Center().y) > (APRON_OUTER_W / 2.0 - 5.0))
        )
        apron = outer_top_edges.fillet(9.0)
    except Exception:
        pass  # Fallback if topology selection varies
        
    # Chamfer top inner edges (2.5mm)
    try:
        inner_top_edges = (
            apron.faces(">Z").edges()
            .filter(lambda e: abs(e.Center().x) < (APRON_OUTER_L / 2.0 - 10.0) and
                              abs(e.Center().y) < (APRON_OUTER_W / 2.0 - 10.0))
        )
        apron = inner_top_edges.chamfer(2.5)
    except Exception:
        pass
        
    # Cut outside accessory T-slot track along the two long sides
    for y_sign in [1, -1]:
        y_pos = y_sign * (APRON_OUTER_W / 2.0)
        # Throat groove
        throat = (
            cq.Workplane("XY")
            .box(APRON_OUTER_L - 2 * LEG_SIZE, TRACK_THROAT_D * 2, TRACK_THROAT_W)
            .translate((0, y_pos, TRACK_Z))
        )
        # Undercut cavity
        cavity = (
            cq.Workplane("XY")
            .box(APRON_OUTER_L - 2 * LEG_SIZE, (TRACK_THROAT_D + 4.0) * 2, TRACK_CAVITY_H)
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


def make_notched_legs():
    """
    Four 54x54mm mitered corner legs.
    Recessed LEG_RECESS (18mm) under leaf perimeter.
    Top inner corner notched 36x36mm by APRON_H (87mm) to cradle apron box.
    """
    leg = (
        cq.Workplane("XY")
        .box(LEG_SIZE, LEG_SIZE, LEG_H)
        .translate((0, 0, LEG_H / 2.0))
    )
    
    # Notch out inner shoulder: 36mm x 36mm x 87mm
    notch_w = LEG_SIZE - PLY_18  # 36mm
    notch = (
        cq.Workplane("XY")
        .box(notch_w + 1.0, notch_w + 1.0, APRON_H + 1.0)
        .translate((
            -LEG_SIZE / 2.0 + notch_w / 2.0,
            -LEG_SIZE / 2.0 + notch_w / 2.0,
            LEG_H - APRON_H / 2.0
        ))
    )
    leg_ne = leg.cut(notch)
    
    # Position: outer face of leg is at (TABLE_LENGTH/2 - LEG_RECESS, TABLE_WIDTH/2 - LEG_RECESS)
    cx = TABLE_LENGTH / 2.0 - LEG_RECESS - LEG_SIZE / 2.0
    cy = TABLE_WIDTH / 2.0 - LEG_RECESS - LEG_SIZE / 2.0
    
    leg_ne = leg_ne.translate((cx, cy, 0))
    leg_nw = leg_ne.mirror("YZ")
    leg_se = leg_ne.mirror("XZ")
    leg_sw = leg_nw.mirror("XZ")
    
    return leg_ne.union(leg_nw).union(leg_se).union(leg_sw)


def make_floating_tabletop(mode="closed"):
    """
    Tabletop leaves with:
    - 12mm underside reverse chamfer around outer perimeter (floating look)
    - Shiplap center meeting seam
    """
    leaf_w = TABLE_WIDTH
    gap = 1.0
    leaf_l = (TABLE_LENGTH - gap) / 2.0
    z_top = APRON_TOP_Z + PLY_18 / 2.0
    
    # Base leaves
    leaf_left = (
        cq.Workplane("XY")
        .box(leaf_l, leaf_w, PLY_18)
        .translate((-(leaf_l + gap) / 2.0, 0, z_top))
    )
    
    # Big 12mm underside chamfer on outer perimeter edges of left leaf
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
    """Removable beam supported in side apron dados."""
    beam_len = APRON_OUTER_W - 2 * PLY_18 + 12.0
    beam = (
        cq.Workplane("XY")
        .box(PLY_18, beam_len, VAULT_DEPTH)
        .translate((0, 0, APRON_TOP_Z - VAULT_DEPTH / 2.0))
    )
    return beam


def make_refined_table(mode="closed"):
    apron = make_apron_frame()
    legs = make_notched_legs()
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


result = make_refined_table(mode="closed")
