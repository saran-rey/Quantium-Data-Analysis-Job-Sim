# Quantium Simulation Project

## Overview
This project is designed to perform Retail data analysis on the provided datasets. The primary focus is on processing raw data, conducting exploratory data analysis (EDA), and generating insights through simulations.

## Project Structure
- data/: This directory contains all the data used in the project.
    - raw/: Contains the raw data files that are used as input for the simulations.
        - [QVI_purchase_behavior.csv](https://github.com/saran-rey/Quantium-Data-Analysis-Job-Sim/blob/main/Task%201/data/raw/QVI_purchase_behaviour.csv)
        - [QVI_transaction_data.xlsx](https://github.com/saran-rey/Quantium-Data-Analysis-Job-Sim/blob/main/Task%201/data/raw/QVI_transaction_data.xlsx)
    - processed/: Contains the processed data files that result from the simulations.
        - [MergedData.csv](https://github.com/saran-rey/Quantium-Data-Analysis-Job-Sim/blob/main/Task%201/data/processed/MergedData.csv)
        - [flavour_frequency.csv](https://github.com/saran-rey/Quantium-Data-Analysis-Job-Sim/blob/main/Task%201/data/processed/flavour_frequency.csv)
        - [unique_product_words.csv](https://github.com/saran-rey/Quantium-Data-Analysis-Job-Sim/blob/main/Task%201/data/processed/unique_product_words.csv)
- data analysis/: This directory contains notebooks and scripts for data analysis.
         - [Task1_Part1_Data_Exploration.ipynb](https://github.com/saran-rey/Quantium-Data-Analysis-Job-Sim/blob/main/Task%201/data%20analysis/Task1_Part1_Data_Exploration.ipynb):A Jupyter notebook for exploratory data analysis and data preparation.
     - [Task1_Part2_Data_Analysis.ipynb](https://github.com/saran-rey/Quantium-Data-Analysis-Job-Sim/blob/main/Task%201/data%20analysis/Task1_Part2_Data_Analysis.ipynb):
         - A Jupyter notebook for generating insights from the data.
     - visuals/: Contains visualizations generated during the data analysis process.
- [Solution_roadmap.md](https://github.com/saran-rey/Quantium-Data-Analysis-Job-Sim/blob/main/Task%201/Solution_roadmap.md):
    - An Markdown file providing a template for the Quantium Virtual Internship Task 1, guiding through the analysis with scaffolding for solutions.

## Requirements
The project requires the following Python packages, which are listed in the requirements.txt file:
- pandas>=2.2.0
- seaborn>=0.13.0
- matplotlib>=3.8.0
- pathlib>=1.0.1
- scipy>=1.11.0
- warnings>=0.4.0

To install the required packages, run:
```bash
pip install -r requirements.txt
```

## Getting Started
To get started with this project, you will need to have the following prerequisites installed:
- Python 3.x
- Jupyter Notebook

## Tasks Performed
- Data Cleaning
    - Date format corrected
    - Whitepsaces cleared fro product name
    - Inconsistent data droped
    - Unrelated Products were indentified and dropped via Frequency tables (salsa, dips, crackers, popcorn)
 - Data Wrangling
   - Custom columns (Brand, Weight) for analysis
   - The cleaned datsets were merged for easier handling into MergedData.csv
   - Custom tables were made to analyse Brand name inconsistency and identify most selling flavour
- Data Visualizaions
- Satistical Analysis

## Key Identifications
- High Revenue generating Segmnets
    - Budget: Old families
    - Mainstream: Young Singles/Couples
    - Mainstream: Retirees
- Desired Package size of the top segments - 175 grams, 150 grams
- Desired Package size of overall population - 170 grams
- Highest Selling Brands
    - Kettle
    - Smiths
    - Doritos
- Most selling Flavours
    - salt, Cheese, Sour, Vinegar, etc
- Seasoal trend
    - High sales in December and April
- Missing Data
    - Christmas Holiday

## Usage
1. Place your raw data files in the data/raw/ directory
2. Use the Task1_Part1_Data_Exploration.ipynb notebook to perform exploratory data analysis and prepare the data.
3. Use the Task1_Part2_Data_Analysis.ipynb notebook to generate insights from the data.
4. The processed data will be available in the data/processed/ directory, and visualizations will be stored in the data analysis/visuals/ directory.
5. Use the Solution_roadmap.md to guide your analysis for the Quantium Virtual Internship Task 1.
