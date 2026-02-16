import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

# ============================================================
# USER SETTINGS
# ============================================================
IMG_PATH = "/Users/raghavdixit/Downloads/Mark8.tif"
PIXEL_TO_MICRON = 1200 / 2181


# ============================================================
# 1️⃣ DETECT VERTICAL CRACKS
# ============================================================
def detect_vertical_cracks(img):

    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    blackhat = cv2.normalize(blackhat, None, 0, 255, cv2.NORM_MINMAX)

    _, bw = cv2.threshold(
        blackhat, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    bw = cv2.morphologyEx(
        bw,
        cv2.MORPH_OPEN,
        cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    )

    vertical_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (3, 35)
    )

    vertical = cv2.morphologyEx(
        bw, cv2.MORPH_OPEN, vertical_kernel
    )

    region_mask = np.zeros_like(vertical)
    region_mask[:h//3, :] = 255
    region_mask[2*h//3:, :] = 255

    return cv2.bitwise_and(vertical, region_mask)


# ============================================================
# 2️⃣ TRACK CRACK PATH
# ============================================================
def detect_seam_from_mask(mask):

    h, w = mask.shape
    xs = np.full(h, np.nan)
    prev_x = w // 2

    for y in range(h):
        cols = np.where(mask[y] > 0)[0]
        if cols.size == 0:
            continue

        x = cols[np.argmin(np.abs(cols - prev_x))]
        xs[y] = x
        prev_x = x

    y_idx = np.arange(h)
    valid = np.isfinite(xs)

    xs[~valid] = np.interp(
        y_idx[~valid],
        y_idx[valid],
        xs[valid]
    )

    xs = np.convolve(xs, np.ones(9)/9, mode="same")

    return np.column_stack([xs, y_idx]).astype(np.float32)


# ============================================================
# MAIN
# ============================================================
def main():

    img = cv2.imread(IMG_PATH)
    if img is None:
        raise FileNotFoundError("Image not found.")

    file_name = os.path.splitext(os.path.basename(IMG_PATH))[0]
    base_dir = os.path.dirname(IMG_PATH)
    output_folder = os.path.join(base_dir, f"Output {file_name}")
    os.makedirs(output_folder, exist_ok=True)

    vertical_mask = detect_vertical_cracks(img)
    seam = detect_seam_from_mask(vertical_mask)

    x_ref = int(np.median(seam[:, 0]))

    h = len(seam)
    top_mid = seam[h//4]
    bottom_mid = seam[3*h//4]

    # ============================================================
    # DISPLACEMENT CALCULATION
    # ============================================================
    top_px = abs(top_mid[0] - x_ref)
    bottom_px = abs(bottom_mid[0] - x_ref)
    total_px = top_px + bottom_px

    top_um = top_px * PIXEL_TO_MICRON
    bottom_um = bottom_px * PIXEL_TO_MICRON
    total_um = top_um + bottom_um

    top_mm = top_um / 1000
    bottom_mm = bottom_um / 1000
    total_mm = total_um / 1000

    print(f"\n=== MIDPOINT DISPLACEMENT ({file_name}) ===")
    print(f"TOP: {top_px:.2f}px | {top_um:.2f}µm | {top_mm:.4f}mm")
    print(f"BOTTOM: {bottom_px:.2f}px | {bottom_um:.2f}µm | {bottom_mm:.4f}mm")
    print(f"TOTAL: {total_px:.2f}px | {total_um:.2f}µm | {total_mm:.4f}mm")

    # ============================================================
    # IMAGE OUTPUT
    # ============================================================
    overlay = img.copy()
    overlay[vertical_mask > 0] = [0, 0, 255]

    cv2.line(overlay,(x_ref,0),(x_ref,img.shape[0]),(255,0,0),2)
    cv2.polylines(overlay,[seam.astype(np.int32)],False,(0,255,255),2)

    cv2.line(overlay,(x_ref,int(top_mid[1])),
             (int(top_mid[0]),int(top_mid[1])),(0,0,255),3)

    cv2.line(overlay,(x_ref,int(bottom_mid[1])),
             (int(bottom_mid[0]),int(bottom_mid[1])),(0,0,255),3)

    image_file = os.path.join(output_folder, f"{file_name}_overlay.jpg")
    cv2.imwrite(image_file, overlay)

    # ============================================================
    # GRAPH (CORRECT STYLE)
    # ============================================================
    d_um = np.abs(seam[:,0] - x_ref) * PIXEL_TO_MICRON

    fig = plt.figure(figsize=(6,8))

    plt.plot(d_um, seam[:,1],
             linewidth=3,
             color='#2C5C8A')

    # Only midpoint lines
    plt.hlines(top_mid[1], 0, top_um,
               colors='red', linewidth=4)

    plt.hlines(bottom_mid[1], 0, bottom_um,
               colors='red', linewidth=4)

    plt.gca().invert_yaxis()
    plt.xlabel("Displacement (µm)", fontsize=14)
    plt.ylabel("Height (pixels)", fontsize=14)
    plt.title("Displacement Profile", fontsize=20)
    plt.grid(True, linewidth=1.2)

    graph_file = os.path.join(output_folder, f"{file_name}_graph.jpg")
    fig.savefig(graph_file, dpi=600, bbox_inches='tight')
    plt.close(fig)

    # ============================================================
    # CSV OUTPUT (px + µm + mm)
    # ============================================================
    csv_file = os.path.join(output_folder, f"{file_name}_results.csv")

    df = pd.DataFrame({
        "Top (px)": [top_px],
        "Top (µm)": [top_um],
        "Top (mm)": [top_mm],
        "Bottom (px)": [bottom_px],
        "Bottom (µm)": [bottom_um],
        "Bottom (mm)": [bottom_mm],
        "Total (px)": [total_px],
        "Total (µm)": [total_um],
        "Total (mm)": [total_mm]
    })

    df.to_csv(csv_file, index=False)

    print("\nSaved:")
    print("Image →", image_file)
    print("Graph →", graph_file)
    print("CSV →", csv_file)


if __name__ == "__main__":
    main()