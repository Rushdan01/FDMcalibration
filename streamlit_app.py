import streamlit as st

st.title("FDM Calibration Tool")

st.write("Print the Calibration Cross and input Expected values and Actual Values")

st.write("""
-----------------------------
INPUT: CROSS DIMENSIONS
-----------------------------
""")

true_lengths = []
measured_lengths = []

# Number of cross measurements
n = st.number_input("How many cross measurements do you want to enter?", min_value=1, step=1)

# Collect cross inputs (ALWAYS shown)
for i in range(int(n)):
    st.write(f"Measurement {i+1}")

    t = st.number_input(f"TRUE length {i+1} (CAD, mm):", key=f"t_{i}")
    m = st.number_input(f"MEASURED length {i+1} (printed, mm):", key=f"m_{i}")

    true_lengths.append(t)
    measured_lengths.append(m)

# -----------------------------
# OPTIONAL: HOLE CALIBRATION
# -----------------------------
hole_offset = None
include_holes = st.checkbox("Include hole calibration")

hole_true = []
hole_measured = []

if include_holes:
    h = st.number_input("How many hole measurements?", min_value=1, step=1)

    for i in range(int(h)):
        st.write(f"Hole {i+1}")

        t = st.number_input(f"TRUE hole diameter {i+1} (mm):", key=f"ht_{i}")
        m = st.number_input(f"MEASURED hole diameter {i+1} (mm):", key=f"hm_{i}")

        hole_true.append(t)
        hole_measured.append(m)

# -----------------------------
# CALCULATE BUTTON
# -----------------------------
if st.button("Calculate"):

    # -----------------------------
    # CALCULATE SCALE + OFFSET
    # -----------------------------
    sum_x = sum(true_lengths)
    sum_y = sum(measured_lengths)
    sum_xx = sum(x*x for x in true_lengths)
    sum_xy = sum(true_lengths[i]*measured_lengths[i] for i in range(int(n)))

    # Avoid division by zero
    if (n * sum_xx - sum_x * sum_x) == 0:
        st.error("Invalid data: division by zero in scale calculation")
    else:
        scale = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x)
        contour_offset = (sum_y - scale * sum_x) / n

        # -----------------------------
        # HOLE CALCULATION
        # -----------------------------
        if include_holes:
            total_offset = 0
            for i in range(int(h)):
                offset = hole_measured[i] - scale * hole_true[i]
                total_offset += offset

            hole_offset = total_offset / h

        # -----------------------------
        # OUTPUT RESULTS
        # -----------------------------
        st.write("=== RESULTS ===")
        st.write("Scale factor:", round(scale, 4))
        st.write("Scaling error (%):", round((scale - 1) * 100, 3))
        st.write("Absolute contour error (mm):", round(contour_offset, 4))

        if hole_offset is not None:
            st.write("Absolute hole error (mm):", round(hole_offset, 4))

        # -----------------------------
        # SLICER SETTINGS
        # -----------------------------
        st.write("=== USE THESE IN SLICER (e.g. Bambu Studio) ===")

        xy_scale = 1 / scale
        horizontal_expansion = -contour_offset / 2

        st.write("XY Scale:", round(xy_scale, 4))
        st.write("XY Contour Offset (mm):", round(horizontal_expansion, 4))

        if hole_offset is not None:
            hole_comp = -hole_offset / 2
            st.write("Hole Offset (mm):", round(hole_comp, 4))
