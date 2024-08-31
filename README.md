# Web Scraping and Data Visualization( Red Bus for 10 State Bus Routes )

This project involves scraping bus route details and associated data from a website, cleaning and processing the data using Python and Pandas, and storing it in an AWS RDS instance. The data is then retrieved and visualized in a Streamlit app with advanced filtering and graphing capabilities.

## Steps Overview

### **Step 1: Understanding the Website**
- **Objective**: Analyze the website's DOM structure using browser developer tools to identify key elements, classes, and IDs.
- **Purpose**: This foundational step allows efficient automated scraping based on our SQL schema.

### **Step 2: Data Scraping**
- **Objective**: Scrape route names, links, and detailed bus information.
- **Duration**:
  - Route names and links: 4 minutes
  - Complete bus details: 222 minutes
- **Tools**: Python, Selenium

### **Step 3: Data Cleaning with Pandas**
- **Objective**: Clean and process the scraped data.
- **Actions**:
  - Store the raw data in Excel for future reference.
  - Use Pandas for data cleaning, including splitting, merging, changing data types, and removing whitespace.

### **Step 4: Data Storage in SQL**
- **Objective**: Store the cleaned data in an AWS RDS instance.
- **Tools**: SQLAlchemy for interacting with MySQL databases on AWS RDS.

### **Step 5: Data Retrieval and Visualization**
- **Objective**: Retrieve the stored data and visualize it using Streamlit.
- **Features**:
  - Interactive filtering and graphing
  - Advanced visualizations using Plotly Express

### **Step 6: Tools Used**
- 🐍 **Python**: Core programming language for scraping and data processing.
- 🚗 **Selenium**: Browser automation tool for scraping dynamic web content.
- 📊 **Pandas**: Data manipulation and cleaning.
- 💾 **MySQL**: Database management system.
- ☁️ **AWS**: Cloud storage using RDS.
- 🎛️ **Streamlit**: Web app framework for displaying data visualizations.

## Author

- **Name**: M. Gopinath
- **Education**: BE (EEE)
- **LinkedIn**: [Gopinath Manickam](https://www.linkedin.com/in/gopinath-manickam-49aa06104/)
- **Email**: gopinathmanikcam95@gmail.com
- **GitHub**: [Gopinath Manickam](https://github.com/GOPINATHMANICKAM95)

## Getting Started

### Prerequisites
- Python 3.x
- Selenium
- Pandas
- SQLAlchemy
- MySQL
- AWS account for RDS
- Streamlit
