"""
3D Printable T-Slot Test Coupon & Gravity Hook Prototype
Parametric CadQuery Model & STL Exporter

Components:
1. t_slot_coupon: 75mm wide x 60mm tall x 18mm thick block matching the apron
   with the exact routed T-slot profile (1/4" throat, 1/2" internal cavity).
2. gravity_hook_clip: Mating test accessory with upward L-hook, fulcrum pad,
   and an integrated card holding ledge.
"""

import os
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

# Hook Clearance Tolerances (for FDM 3D printing)
FIT_TOLERANCE = 0.4              # 0.4mm clearance for smooth slide & tilt


def make_t_slot_coupon():
    """Generates the 18mm apron test coupon with routed T-slot."""
    # Base block
    block = cq.Workplane("XY").box(COUPON_W, PLY_18, COUPON_H)
    
    # Throat groove along the front (+Y face)
    # Front face is at Y = PLY_18 / 2 = 9.0
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
    
    # Add two 4mm mounting screw counterbores to attach to bench/scrap if desired
    screw_hole_l = (
        cq.Workplane("XY")
        .cylinder(PLY_18 * 2, 2.2)
        .translate((-25.0, 0, 0))
    )
    screw_hole_r = (
        cq.Workplane("XY")
        .cylinder(PLY_18 * 2, 2.2)
        .translate((25.0, 0, 0))
    )
    # Counterbores from back (-Y)
    cb_l = (
        cq.Workplane("XY")
        .cylinder(12.0, 4.2)
        .translate((-25.0, -PLY_18 / 2.0 + 3.0, 0))
    )
    cb_r = (
        cq.Workplane("XY")
        .cylinder(12.0, 4.2)
        .translate((25.0, -PLY_18 / 2.0 + 3.0, 0))
    )
    coupon = coupon.cut(screw_hole_l).cut(screw_hole_r).cut(cb_l).cut(cb_r)
    
    return coupon


def make_gravity_hook_clip():
    """
    Generates the mating test accessory clip:
    - Upward hook tab that inserts at a 15-deg angle and drops behind upper lip
    - Lower fulcrum pad pressing against the apron face
    - Integrated card holding shelf to test weight bearing
    """
    clip_w = 40.0                # 40mm wide test clip
    
    # Hook cross-section profile in YZ plane (extrude along X by clip_w):
    # Front face of apron is at Y = 0.
    # Interior of slot extends into -Y (from Y = 0 to Y = -8.0).
    # Exterior of accessory extends into +Y (from Y = 0 to Y = +35.0).
    
    # Clearances:
    # Throat height = 6.4mm -> neck thickness = 5.2mm (allows 15-deg tilt)
    # Upper cavity lip is at Z = +6.35/2 = +3.17 to Z = +12.7/2 = +6.35
    # Hook tip rises up to Z = +5.2mm (well behind the upper lip of the throat)
    pts = [
        # 1. Back hook inside T-slot
        (-7.5, 2.2),             # Upper hook tip (inside cavity)
        (-7.5, 5.0),             # Top of hook
        (-5.5, 5.0),             # Hook shoulder
        (-4.5, 2.4),             # Neck top (clears throat)
        (0.0, 2.4),              # Exit from throat to outside face
        
        # 2. Outer body with card slot
        (5.0, 15.0),             # Upward card backrest
        (8.0, 15.0),
        (8.0, 2.0),              # Bottom of card slot (angled)
        (12.0, 2.0),
        (15.0, 6.0),             # Front card retaining lip
        (18.0, 6.0),
        (20.0, -4.0),            # Outer bottom corner
        (4.0, -18.0),            # Taper to lower fulcrum
        
        # 3. Lower fulcrum pad pressing against apron face
        (0.0, -18.0),            # Fulcrum pad touching apron face
        (0.0, -2.4),             # Enters throat
        (-4.5, -2.4),            # Lower neck
        (-6.5, -1.0),            # Bottom of hook
    ]
    
    clip = (
        cq.Workplane("YZ")
        .polyline(pts).close()
        .extrude(clip_w)
        .translate((-clip_w / 2.0, 0, 0))
    )
    
    return clip


if __name__ == "__main__":
    out_dir = r"c:\Users\atyre\github\gaming_table\models\3d_print"
    os.makedirs(out_dir, exist_ok=True)
    
    coupon = make_t_slot_coupon()
    clip = make_gravity_hook_clip()
    
    coupon_path = os.path.join(out_dir, "t_slot_coupon.stl")
    clip_path = os.path.join(out_dir, "gravity_hook_clip.stl")
    
    cq.exporters.export(coupon, coupon_path)
    cq.exporters.export(clip, clip_path)
    
    print(f"Exported: {coupon_path}")
    print(f"Exported: {clip_path}")
