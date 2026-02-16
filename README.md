# Measurement-of-Micro-Scale-Displacement-Using-Computer-Vision.
A computer vision–based system for measuring micrometer-scale displacement in hybrid sandwich sheets using morphology-based crack tracking and sub-pixel deformation analysis. Generates overlay images, displacement graphs, and quantitative CSV reports for engineering applications.


Overview

This project presents a non-contact computer vision–based deformation measurement system developed to quantify micrometer-scale displacement in lightweight hybrid sandwich sheets.

Hybrid sandwich sheets are widely used in aerospace and automotive applications. During bending, relative in-plane displacement occurs between layers. Conventional contact-based measurement techniques lack the precision required to capture these micro-scale deformations.

This repository contains a morphology-based crack tracking and displacement quantification algorithm that extracts vertical crack paths and computes sub-pixel displacement with high robustness.

⸻

🎯 Problem Statement
	•	Micro-scale deformation cannot be measured accurately using traditional tools.
	•	Surface oxidation and scratches introduce noise.
	•	Industrial specimens require a robust automated measurement system.

⸻

🧠 Approach

❌ Algorithm 1: Blob Detection (Failed Approach)
	•	Detected 685 features instead of the actual 2 markers.
	•	Surface scratches and oxidation residue were falsely classified as markers.
	•	Not reliable for industrial surface conditions.

✅ Algorithm 2: Morphology-Based Deformation Tracking (Final Approach)

The final algorithm includes:

1️⃣ Preprocessing
	•	Grayscale conversion
	•	Gaussian blur for noise reduction

2️⃣ Morphology-Based Crack Segmentation
	•	Vertical structure extraction
	•	Binary mask generation
	•	Noise filtering
	•	Restriction to silver layer regions

3️⃣ Crack Path Tracking
	•	Continuity-constrained tracking
	•	Prevents switching between multiple cracks
	•	Gap filling for incomplete segments
	•	Path smoothing for stable displacement calculation

4️⃣ Displacement Calculation
	•	Statistical median reference line generation
	•	Perpendicular crack deviation measurement
	•	Sub-pixel displacement estimation
	•	Pixel-to-micrometer calibration conversion

⸻

📊 Outputs Generated

The system automatically produces:
	•	🖼 Overlay Image
	•	Red: Crack pixels
	•	Yellow: Tracked crack path
	•	Blue: Statistical reference line
	•	📈 Displacement Graph
	•	X-axis → Displacement (µm)
	•	Y-axis → Height (pixels)
	•	Full deformation profile
	•	📄 CSV Report
	•	Top displacement (px, µm, mm)
	•	Bottom displacement (px, µm, mm)
	•	Total displacement

⸻

🚀 Key Features
	•	Robust against oxidation and surface scratches
	•	Sub-pixel accuracy
	•	Fully automated processing
	•	Industrially applicable
	•	Scalable for forming and deformation analysis

⸻

🛠 Technologies Used
	•	Python
	•	OpenCV
	•	NumPy
	•	Matplotlib
	•	Morphological Image Processing
	•	Statistical Segmentation

⸻

📌 Applications
	•	Aerospace material deformation analysis
	•	Automotive forming validation
	•	Crack tracking & structural monitoring
	•	Non-contact optical metrology

⸻

📖 Conclusion

A morphology-based deformation tracking system was successfully developed to automatically extract vertical crack paths and measure midpoint deformation with high precision.

The approach combines morphological enhancement, statistical segmentation, and continuity-constrained tracking to produce reliable visual and numerical displacement results suitable for engineering applications.
