"""
3D Printable T-Slot Test Coupon & Gravity Hook Prototype (Rev 2)
Parametric CadQuery Model & STL Exporter

Revisions in v2:
1. Neck/shaft: 1mm shorter (reaches cavity with zero slop) and 1mm thicker (5.4mm vs 4.8mm for maximum rigidity).
2. Hook tip: Extended upward to Z=+5.8mm (2.6mm of solid vertical grab behind the lip, up from 1.8mm).
3. 5-Degree Upward Angle: Hook shaft angles upward by 5.0 degrees, while holder back pad is 100% vertical.
   Under gravity load, the 5-degree wedge pulls the entire 19mm-tall flat pad flush against the apron face,
   eliminating edge digging and point-load rubbing damage.
"""

import os
import math
import cadquery as cq

# --- Dimensions (mm) ---
PLY_18 = 18.0                    # Apron thickness
COUPON_W = 75.0                  # Width of test coupon block
COUPON_H = 60.0                  # Height of test coupon block

# T-Slot Cutter Profile (Whiteside 3050 / Rockler T-Slot Bit)
THROAT_W = 6.4                   # 1/4" (6.35 mm) throat width
THROAT_D = 4.5                   # 4.5 mm depth before undercut
CAVITY_W = 12.7                  # 1/2" (12.7 mm) internal cavity width
CAVITY_H = 4.8                   # 3/16" (4.76 mm) cavity height
CAVITY_D = 4.0                   # 4.0 mm cavity thickness (total depth = 8.5mm)


def make_t_slot_coupon():
    """Generates the 18mm apron test coupon with routed T-slot."""
    block = cq.Workplane("XY").box(COUPON_W, PLY_18, COUPON_H)
    
    # Throat groove along the front (+Y face at Y = 9.0)
    throat = (
        cq.Workplane("XY")
        .box(COUPON_W + 2.0, THROAT_D * 2, THROAT_W)
        .translate((0, PLY_18 / 2.0, 0))
    )
    # Undercut cavity
    cavity = (
        cq.Workplane("XY")
        .box(COUPON_W + 2.0, CAVITY_D * 2, CAVITY_W)
        .translate((0, PLY_18 / 2.0 - THROAT_D - CAVITY_D / 2.0, 0))
    )
    
    coupon = block.cut(throat).cut(cavity)
    
    # Two 4mm mounting screw counterbores
    screw_hole_l = cq.Workplane("XY").cylinder(PLY_18 * 2, 2.2).translate((-25.0, 0, 0))
    screw_hole_r = cq.Workplane("XY").cylinder(PLY_18 * 2, 2.2).translate((25.0, 0, 0))
    cb_l = cq.Workplane("XY").cylinder(12.0, 4.2).translate((-25.0, -PLY_18 / 2.0 + 3.0, 0))
    cb_r = cq.Workplane("XY").cylinder(12.0, 4.2).translate((25.0, -PLY_18 / 2.0 + 3.0, 0))
    
    return coupon.cut(screw_hole_l).cut(screw_hole_r).cut(cb_l).cut(cb_r)


def make_gravity_hook_clip_v2():
    """
    Refined Gravity Hook Clip (v2):
    - Shaft 1mm shorter (starts catch at Y = -3.8 to -4.0mm)
    - Shaft 1mm thicker (5.4mm vs 4.8mm)
    - Hook tip extended to Z = +5.8mm (2.6mm of vertical lip grab)
    - 5-degree upward slope on shaft with 100% vertical flat back pad (760 mm^2 bearing area)
    """
    clip_w = 40.0
    
    # 5-degree angle in radians
    deg5 = math.radians(5.0)
    tan5 = math.tan(deg5)
    
    # Y=0 is the apron front face.
    # The back pad is at Y = 0 from Z = -2.7 down to Z = -22.0 (19.3mm of flat vertical contact!).
    #
    # The neck enters the slot into -Y:
    # At Y = 0: neck top is at Z = +2.7, neck bot is at Z = -2.7 (thickness = 5.4mm).
    # As it travels into -Y (depth), it rises by -Y * tan(5 deg):
    # At Y = -3.8: neck top is at 2.7 - (-3.8)*tan5 = 2.7 + 0.33 = +3.03 mm (clears 3.20mm throat ceiling!).
    #              neck bot is at -2.7 + 0.33 = -2.37 mm (clears -3.20mm throat floor!).
    #
    # Hook geometry:
    # Hook catch shoulder: rises from (Y = -3.8, Z = 3.03) to (Y = -4.0, Z = 5.80)
    # Hook tip: from (Y = -4.0, Z = 5.80) to (Y = -6.5, Z = 5.80)
    # Hook back slope: down to (Y = -6.8, Z = 2.00)
    # Hook bottom slope: from (Y = -6.8, Z = 2.00) down to (Y = -5.5, Z = -1.00) to (Y = -3.8, Z = -2.37)
    
    pts = [
        # --- Internal Hook Geometry (Inside T-slot, Y < 0) ---
        (-6.8, 2.0),             # Hook back corner
        (-6.5, 5.8),             # Hook top-back
        (-4.0, 5.8),             # Hook top-front (extended tip: grabs 2.6mm of lip!)
        (-3.8, 3.03),            # Hook catch shoulder (1mm shorter shaft!)
        (0.0, 2.7),              # Shaft exit at apron face
        
        # --- External Card Holder Body (Outside, Y > 0) ---
        (5.0, 16.0),             # Upward card backrest
        (8.5, 16.0),
        (8.5, 2.5),              # Bottom of card slot (angled for card retention)
        (12.5, 2.5),
        (15.5, 6.5),             # Front card retaining lip
        (18.5, 6.5),
        (20.0, -3.0),            # Outer bottom corner
        (4.0, -18.0),            # Taper to lower fulcrum
        (0.0, -22.0),            # Bottom of flat vertical fulcrum pad (extended to -22mm)
        
        # --- Lower Fulcrum Pad (Flat against Y = 0) ---
        (0.0, -2.7),             # Top of flat fulcrum pad (at Y=0)
        
        # --- Bottom of Shaft (Angled upward at 5 degrees) ---
        (-3.8, -2.37),           # Bottom of neck at throat exit (rises at 5 deg)
        (-5.5, -1.0),            # Bottom transition to hook
    ]
    
    clip = (
        cq.Workplane("YZ")
        .polyline(pts).close()
        .extrude(clip_w)
        .translate((-clip_w / 2.0, 0, 0))
    )
    
    # Add a subtle 0.8mm fillet on the bottom transition of the fulcrum pad to prevent any sharp edge
    try:
        bot_edges = clip.faces("<Z").edges("|X")
        clip = bot_edges.fillet(0.8)
    except Exception:
        pass
        
    return clip


if __name__ == "__main__":
    out_dir = r"c:\Users\atyre\github\gaming_table\models\3d_print"
    os.makedirs(out_dir, exist_ok=True)
    
    coupon = make_t_slot_coupon()
    clip_v2 = make_gravity_hook_clip_v2()
    
    coupon_path = os.path.join(out_dir, "t_slot_coupon.stl")
    clip_v2_path = os.path.join(out_dir, "gravity_hook_clip_v2.stl")
    clip_default_path = os.path.join(out_dir, "gravity_hook_clip.stl")
    
    cq.exporters.export(coupon, coupon_path)
    cq.exporters.export(clip_v2, clip_v2_path)
    cq.exporters.export(clip_v2, clip_default_path) # Also update default
    
    print(f"Exported: {coupon_path}")
    print(f"Exported: {clip_v2_path}")
    print(f"Exported: {clip_default_path}")
