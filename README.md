# E-Commerce Data Analysis Project

This project focuses on performing an RFM (Recency, Frequency, Monetary) analysis and other insights from an e-commerce dataset. The dataset used is publicly available and contains customer orders, payments, and other transactional details.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Dataset](#dataset)
- [RFM Analysis](#rfm-analysis)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project uses a public dataset to analyze e-commerce data with a focus on customer segmentation through **RFM analysis**. The analysis helps businesses understand customer behavior, optimize marketing strategies, and increase sales by identifying loyal, at-risk, and potential churn customers.

The key objectives of the project:
1. Analyze customer transactions.
2. Perform RFM segmentation.
3. Visualize the results using Streamlit.
4. Identify potential marketing strategies based on customer segments.

## Features

- Merge customer, order, and payment data to generate meaningful insights.
- Perform **RFM segmentation** to group customers based on their purchase behavior.
- Visualize the customer segments for Recency, Frequency, and Monetary categories using Streamlit.

## Installation

To set up and run the project on your local machine, follow the steps below:

### 1. Clone the repository:
First, clone the project from GitHub by running the following command:

```bash
git clone https://github.com/dheekz/E-commerce-Public-Dataset.git
```
### 2. Navigate to the project directory:
```bash
cd E-commerce-Public-Dataset
```
### 3. Set up a virtual environment (optional but recommended):
For Python users, it's recommended to create a virtual environment to manage dependencies.

```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```
### 4. Install the required dependencies:
Install all the required libraries from the requirements.txt file by running:

```bash
pip install -r requirements.txt
```
### 5. Install Streamlit:
If Streamlit is not included in the requirements.txt, you can install it by running:

```bash
pip install streamlit
```
## Usage
Once you have installed the dependencies, you can run the Streamlit app to visualize the RFM segmentation analysis.

Steps to run:
Run the Streamlit application:

```bash
streamlit run main.py
```
View the results:

The Streamlit app will open in your browser (default URL: http://localhost:8501).
You will be able to see the visualizations of RFM segmentation and analyze customer behavior interactively.

### Project Structure
submission
├───dashboard

| ├───main_data.csv

| └───dashboard.py

├───data

| ├───data_1.csv

| └───data_2.csv

├───notebook.ipynb

├───README.md

└───requirements.txt

└───url.txt

## RFM Analysis
RFM Analysis stands for Recency, Frequency, and Monetary analysis. It's a proven method used to evaluate customer value by analyzing three key factors:

Recency: How recently a customer made a purchase.
Frequency: How often a customer makes purchases.
Monetary: How much money a customer spends on purchases.
Based on the analysis, customers are grouped into different segments such as:

High-Value Customers: Customers with high frequency and monetary value.
Loyal Customers: Customers who make frequent purchases.
At-Risk Customers: Customers who have not made recent purchases.
## Contributing
If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. Any contributions, such as new features or bug fixes, are welcome!

## License
This project is licensed under the MIT License. See the LICENSE file for details.
