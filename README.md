# 💻 Laptop Recommendation - Decision Support System (DSS)

An automated Decision Support System (DSS) built with Python to help consumers find the best laptop recommendations objectively. This project applies Multi-Criteria Decision Making (MCDM) algorithms to evaluate and rank laptops based on a real-world dataset.

## 📝 Project Overview
Choosing a laptop can be overwhelming due to the sheer number of options and specifications (Brand, RAM, Storage, CPU, Weight, and Price). This project eliminates brand bias by ranking laptops mathematically using 3 different DSS algorithms simultaneously. 

The system acts as a smart filter—processing over 1,300 real laptop data points from Kaggle, applying realistic budget constraints (e.g., `< 1000 Euros` and `>= 8GB RAM`), and outputting the top 10 most "worth it" laptops based on user-defined criteria weights.

## ⚙️ Algorithms Implemented
To ensure unbiased and accurate rankings, this project compares the results of three prominent algorithms:
1. **SAW (Simple Additive Weighting):** The classic weighted sum method.
2. **TOPSIS (Technique for Order Preference by Similarity to Ideal Solution):** Evaluates options based on the shortest distance to the positive ideal solution and the farthest from the negative ideal solution.
3. **WASPAS (Weighted Aggregated Sum Product Assessment):** A highly accurate hybrid method combining WSM (Weighted Sum Model) and WPM (Weighted Product Model) with a lambda (λ) parameter of 0.5.

## 📊 Dataset & Criteria Matrix
**Data Source:** [Kaggle - Laptop Price Dataset](https://www.kaggle.com/datasets/muhammetvarl/laptop-price) (1,303 original rows).

**Evaluation Criteria:**
*   **C1 (Price) - 35% Weight** -> Cost Attribute
*   **C2 (RAM) - 20% Weight** -> Benefit Attribute
*   **C3 (Storage) - 20% Weight** -> Benefit Attribute
*   **C4 (Weight/Kg) - 15% Weight** -> Cost Attribute
*   **C5 (Screen Size) - 10% Weight** -> Benefit Attribute

## 🚀 How to Run
1. Clone this repository:
   ```bash
   git clone https://github.com/HyLuthfi/laptop-recommendation-dss.git
   ```
2. Open `pemilihan_laptop.ipynb` using Jupyter Notebook or VS Code.
3. Make sure you have the required libraries installed:
   ```bash
   pip install pandas numpy matplotlib
   ```
4. Run all cells to see the data processing, mathematical normalizations, and the final comparative Bar Chart visualizations.

## 👨‍💻 Author
**HyLuthfi** - Final Project / UAS Sistem Pendukung Keputusan.
