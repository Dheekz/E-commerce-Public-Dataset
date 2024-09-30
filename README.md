# E-Commerce Data Analysis Project
This project focuses on performing an RFM (Recency, Frequency, Monetary) analysis and other insights from an e-commerce dataset. The dataset used is publicly available and contains customer orders, payments, and other transactional details.

### Table of Contents
Introduction
Features
Installation
Usage
Project Structure
Dataset
RFM Analysis
Contributing
License
### Introduction
This project uses a public dataset to analyze e-commerce data with a focus on customer segmentation through RFM analysis. The analysis helps businesses understand customer behavior, optimize marketing strategies, and increase sales by identifying loyal, at-risk, and potential churn customers.

The key objectives of the project:

Analyze customer transactions.
Perform RFM segmentation.
Visualize the results using Streamlit.
Identify potential marketing strategies based on customer segments.
### Features
Merge customer, order, and payment data to generate meaningful insights.
Perform RFM segmentation to group customers based on their purchase behavior.
Visualize the customer segments for Recency, Frequency, and Monetary categories using interactive charts with Streamlit.
Identify segments for loyal, frequent, or high-value customers.
### Installation
To set up and run the project on your local machine, follow the steps below:

### 1. Clone the repository:
First, clone the project from GitHub by running the following command:

bash
Copy code
git clone https://github.com/yourusername/ecommerce-data-analysis.git
### 2. Navigate to the project directory:
bash
Copy code
cd ecommerce-data-analysis
### 3. Set up a virtual environment (optional but recommended):
For Python users, it's recommended to create a virtual environment to manage dependencies.

bash
Copy code
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
### 4. Install the required dependencies:
Install all the required libraries from the requirements.txt file by running:

bash
Copy code
pip install -r requirements.txt
### 5. Install Streamlit:
If Streamlit is not included in the requirements.txt, you can install it by running:

bash
Copy code
pip install streamlit
## Usage
Once you have installed the dependencies, you can run the Streamlit app to visualize the RFM segmentation analysis.

Steps to run:
Run the Streamlit application:

bash
Copy code
streamlit run streamlit_rfm.py
View the results:

The Streamlit app will open in your browser (default URL: http://localhost:8501).
You will be able to see the visualizations of RFM segmentation and analyze customer behavior interactively.
Code Example
Here is a brief example of the code used for merging the datasets and performing RFM analysis:

python
Copy code
# Merge the orders and payments data
rfm_data = pd.merge(orders_df, order_payments_df, on='order_id', how='inner')
rfm_data = pd.merge(rfm_data, customers_df, on='customer_id', how='inner')

# Convert timestamps and calculate Recency, Frequency, Monetary (RFM)
rfm_data['order_purchase_timestamp'] = pd.to_datetime(rfm_data['order_purchase_timestamp'])
last_date = rfm_data['order_purchase_timestamp'].max()

rfm_table = rfm_data.groupby('customer_id').agg({
    'order_purchase_timestamp': lambda x: (last_date - x.max()).days,
    'order_id': 'count',
    'payment_value': 'sum'
})

# Rename columns for RFM
rfm_table.rename(columns={
    'order_purchase_timestamp': 'Recency',
    'order_id': 'Frequency',
    'payment_value': 'Monetary'
}, inplace=True)

# Visualize the segments using Streamlit
st.title('RFM Segmentation Analysis')
Project Structure
bash
Copy code
├── data/                 # Folder for storing the dataset
├── notebooks/            # Jupyter notebooks for analysis
├── streamlit_rfm.py      # Main Streamlit application for RFM analysis
├── requirements.txt      # Dependencies and packages required for the project
├── README.md             # Project documentation
└── .gitignore            # Ignored files/folders in the repository
Dataset
This project uses a public e-commerce dataset that contains the following information:

Orders: Data related to customer orders, such as order ID, timestamps, and status.
Payments: Data about payments including payment method, value, and order ID.
Customers: Information about the customers, such as customer ID and location.
You can download the dataset from the source (e.g., Kaggle) and place it in the data/ folder.

RFM Analysis
RFM Analysis stands for Recency, Frequency, and Monetary analysis. It's a proven method used to evaluate customer value by analyzing three key factors:

Recency: How recently a customer made a purchase.
Frequency: How often a customer makes purchases.
Monetary: How much money a customer spends on purchases.
Based on the analysis, customers are grouped into different segments such as:

High-Value Customers: Customers with high frequency and monetary value.
Loyal Customers: Customers who make frequent purchases.
At-Risk Customers: Customers who have not made recent purchases.
Contributing
If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. Any contributions, such as new features or bug fixes, are welcome!

# License
This project is licensed under the MIT License. See the LICENSE file for details.
