import streamlit as st

st.title("#FDM Calibration Tool")
st.write(
    " Print the Calibraation Cross and input Expected values and Actual Values"
)
st.write(
    " -----------------------------\n"
    " INPUT: CROSS DIMENSIONS\n"
    " -----------------------------"
)
true_lengths = []
measured_lengths = []

n = float(st.text_input("\nHow many cross measurements do you want to enter?"))

for i in range(n):
    st.write(f"\nMeasurement {i+1}")

    t= float(st.text_input("Enter TRUE length (CAD, mm):"))
    ##t = float(input(">> "))
    true_lengths.append(t)

    m = float(st.text_input("Enter MEASURED length (printed, mm):"))
    ##m = float(input(">> "))
    measured_lengths.append(m)

# -----------------------------
# CALCULATE SCALE + OFFSET
# Using manual least squares
# -----------------------------
sum_x = 0
sum_y = 0
sum_xx = 0
sum_xy = 0

for i in range(n):
    x = true_lengths[i]
    y = measured_lengths[i]

    sum_x += x
    sum_y += y
    sum_xx += x * x
    sum_xy += x * y

# slope (scale)
scale = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x)

# intercept (contour offset)
contour_offset = (sum_y - scale * sum_x) / n

# -----------------------------
# OPTIONAL: HOLE CALIBRATION
# -----------------------------
choice = str(st.text_input("\nDo you want to enter hole measurements? (y/n)")).lower()

hole_offset = None

if choice == "y":
    h = st.text_input("\nHow many hole measurements?")
    ##h = int(input(">> "))

    total_offset = 0

    for i in range(h):
        st.write(f"\nHole {i+1}")

        t = float(st.text_input("Enter TRUE hole diameter (mm):"))
        ##t = float(input(">> "))

        m = float(st.write("Enter MEASURED hole diameter (mm):"))
        ##m = float(input(">> "))

        # offset = measured - scale * true
        offset = m - scale * t
        total_offset += offset

    hole_offset = total_offset / h

# -----------------------------
# OUTPUT RESULTS
# -----------------------------
st.write("\n=== RESULTS ===")

st.write("Scale factor:", round(scale, 4))
st.write("Scaling error (%):", round((scale - 1) * 100, 3))
st.write("Contour offset (total, mm):", round(contour_offset, 4))

if hole_offset is not None:
    st.write("Hole offset (total, mm):", round(hole_offset, 4))
# -----------------------------
# SLICER SETTINGS
# -----------------------------
st.write("\n=== USE THESE IN SLICER (e.g. Bambu Studio) ===")

xy_scale = 1 / scale
horizontal_expansion = -contour_offset/2

st.write("XY Scale:", round(xy_scale, 4))
st.write("Horizontal Expansion (mm):", round(horizontal_expansion/2, 4))

if hole_offset is not None:
    hole_comp = -hole_offset / 2
    st.write("Hole Horizontal Expansion (mm):", round(hole_comp, 4))

