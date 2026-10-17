# Modular Dining & Gaming Table: Design Specification (Rev 4)

## 1. Project Overview & Updated Dimensions

- **Total Dimensions**: **27.0" (685.8 mm) Width $\times$ 56.0" (1422.4 mm) Length $\times$ 30.0" (762 mm) Height**.
- **Dining Capacity**: 4 to 6 people (1 at each short end, 2 along each long side).
- **Gaming Vault**: **24.1" $\times$ 53.1" (612 $\times$ 1348 mm)** playing field, 3.0" (75 mm) recessed depth.
- **Under-Apron Knee Clearance**: **24.9" (632 mm)** clear height from floor to underside of aprons.
- **Top Overhang**: **3/4" (19 mm)** perimeter drip edge shielding stretchers and vault from liquid spills.
- **Center Seam Gasket**: Half-lap shiplap rebate with 3.5mm $\times$ 2.0mm groove housing a 3.0mm closed-cell silicone foam cord.
- **Removable Center Beam**: 18mm Baltic birch beam dropping into 6mm vertical dados in side aprons.

---

## 2. Long-Side Chair Tuck-In Analysis for Option 1 (Center Pillar)

### How do chairs slide in from the long side with Option 1?

#### A. Lateral Spacing (X-Axis)
- The table length is 56" (1422 mm).
- Two diners sit along each long side. Their chair centers are naturally positioned at roughly $X = -14"$ (-355 mm) and $X = +14"$ (+355 mm).
- A standard dining chair is **18" (457 mm) wide**, meaning its legs span from roughly $X = 5"$ to $X = 23"$.
- The transverse wing of the center pillar sits at $X = 0$ with a thickness of only **36 mm (1.4")** (from $X = -18\text{ mm}$ to $+18\text{ mm}$).
- **Lateral Clearance**: There is $5" - 0.7" = \mathbf{4.3" (110 mm)}$ of clear space between the inner chair leg and the transverse pillar wing. **Lateral interference is zero**; both chairs fit easily side-by-side.

#### B. Inward Push-In Depth (Y-Axis)
- The table width is 27" (685.8 mm). The center line of the table is at **$Y = 0$**, which is **13.5" (343 mm)** inward from the table edge.
- The longitudinal wing of the center pillar runs directly along the center line ($Y = 0$), with a thickness of 36 mm (extending 18 mm / 0.7" to each side of center).
- **Chair Tuck-In Stop**: When an 18" deep dining chair is pushed inward from the long side, the front edge of the seat hits the longitudinal center wing at **13.5" of depth**:
  - **75% of the chair slides completely under the table** ($13.5"$ of the $18"$ seat depth).
  - The back **4.5" of the seat plus the chair backrest** remain proud of the table edge.
- **In-Use Seating**: When diners sit down, their knees do not cross past the 13.5" center line (on a 27" table, diners sitting opposite each other already share the 13.5" center). The 36 mm center ply fin simply acts as a clean divider between opposite diners' feet.

---

## 3. Comprehensive Leg Architecture Comparison

| Feature | Option 1: Center Pillar / Trestle Wings | Option 3: Notched Corner Posts |
| :--- | :--- | :--- |
| **Short-End Chair Tuck-In** | **Partial (10" inward)**: Base wing blocks chair ~8" before fully flush | **100% Full Tuck-In**: 18" chair slides completely between legs |
| **Long-Side Chair Tuck-In** | **75% Tuck-In (13.5" inward)**: Chair front meets center fin at $Y=0$ | **100% Full Tuck-In**: Chair slides fully under apron box |
| **Corner Freedom for Diners** | **Maximum**: Zero corner legs to bump shins when sliding into chairs | **Standard**: Corner legs at $X = \pm 27"$, $Y = \pm 12.75"$ |
| **Interior Vault Cleanliness** | **100% Clean & Continuous** (Zero corner posts) | **100% Clean & Continuous** (Legs notch outside apron) |
| **Disassembly Protocol** | 4 hand-tightened star knobs into threaded inserts; 2 wings slide apart | 8 Joint Connector Bolts through apron walls into leg inserts |
| **Longitudinal Table Support** | Cantilevers 18" on each end from center support | Direct 4-point column support down to floor at all corners |
| **Fabrication Method** | CNC / jigsaw sweeping curved profiles in double 18mm ply | Pre-lamination stepped ply glue-up (automatic 90° shoulder) |

---

## 4. CadQuery Model Scripts

- [`models/table_notched_legs.py`](file:///c:/Users/atyre/github/gaming_table/models/table_notched_legs.py): Parametric model for Option 3 (closed, half, and vault modes).
- [`models/table_pedestal.py`](file:///c:/Users/atyre/github/gaming_table/models/table_pedestal.py): Parametric model for Option 1 (closed, half, and vault modes).
- [`models/table_assembly.py`](file:///c:/Users/atyre/github/gaming_table/models/table_assembly.py): Master table assembly with removable center beam, dados, and silicone foam cord groove.
