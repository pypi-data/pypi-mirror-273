<span style='color: Pink; font-size:25px'>  **Data Quality Validation** </span>

This package is designed for performing data quality validation using PyDeequ.  
It enables users to validate the quality of their data, identifying any potential issues that may affect its suitability for processing or analysis.  
Also, to send email notification about the validation result.

**Author**: Ketan Kirange

**Contributors**: Ketan Kirange, Ajay Rahul Raja

This package contains tools and utilities for performing data quality checks on data files in 
 - Pandas, 
 - Dask, and 
 - PySpark formats, leveraging libraries such as PyDeequ and SODA utilities.

These checks help ensure the integrity, accuracy, and completeness of the data, essential for robust data-driven decision-making processes.

<span style='color: Pink; font-size:25px'> **Importance of Data Quality** </span>

Data quality plays a pivotal role in any engineering project, especially in data science, reporting, and analysis.  

Here's why ensuring high data quality is crucial:

<span style='color: Pink; font-size:25px'> 1. Reliable Insights </span>

High-quality data leads to reliable and trustworthy insights.  
When the data is accurate, complete, and consistent, data scientists and analysts can make informed decisions confidently.

<span style='color: Pink; font-size:25px'> 2. Trustworthy Models </span>

Data quality directly impacts the performance and reliability of machine learning models.  
Models trained on low-quality data may produce biased or inaccurate predictions, leading to unreliable outcomes.

<span style='color: Pink; font-size:25px'> 3. Effective Reporting </span>

Quality data is fundamental for generating accurate reports and visualizations.  
Analysts and stakeholders rely on these reports for understanding trends, identifying patterns, and making strategic decisions.  
Poor data quality can lead to misleading reports and flawed interpretations.

<span style='color: Pink; font-size:25px'> 4. Regulatory Compliance </span>

In many industries, compliance with regulations such as GDPR, HIPAA, or industry-specific standards is mandatory.  
Ensuring data quality is essential for meeting these regulatory requirements and avoiding potential legal consequences.



<span style='color: Pink; font-size:25px'> **Getting Started** </span>

To get started with data quality validation using this repository, follow the instructions in the respective documentation for each tool:

- [Pandas Data Quality Validation Guide](link-to-pandas-guide)
- [Dask Data Quality Validation Guide](link-to-dask-guide)
- [PySpark with PyDeequ Guide](link-to-pyspark-guide)
- [SODA Utilities Guide](link-to-soda-guide)

<span style='color: Pink; font-size:25px'> **Contributing** </span>

We welcome contributions from the community to enhance and expand the capabilities of this data quality validation repository.  
Please refer to the [contribution guidelines](link-to-contribution-guidelines) for more information on how to contribute.




<br></br>
<span style="font-size:13pt; color:orange">**Prerequisites:**</span>

- Step 1: Download Java, Python, and Apache Spark.    
Having the appropriate versions is essential to run the code on a local system.  

<span style="font-size:11pt; color:green"> **Java:** </span>     [Java 1.8 Archive Downloads](https://www.oracle.com/uk/java/technologies/javase/javase8-archive-downloads.html)

<span style="font-size:11pt; color:green"> **Python:** </span> [Python 3.9.18 Release](https://www.python.org/downloads/release/python-390/)

<span style="font-size:11pt; color:green"> **Apache Spark:** </span> [Apache Spark 3.3.0 Release](https://spark.apache.org/releases/spark-release-3-3-0.html)

- Step 2: Install PyDeequ in the terminal if you encounter an error related to "PyDeequ module is not installed on the machine."

<span style="font-size:13pt; color:orange"> **How to install PyDeequ? Use the following command:** </span>  
  `pip install pydeequ`

- Step 3: Install our ‘Data Quality Validation’ python library in terminal.  
  `pip install data-quality-validation-pydeequ`

- Step 4: To run the Data Quality Validation function, import the library as below:  
  `from dqv.dqv_pydeequ import DqvPydeequ, sendEmailNotification`  

- Step 5: Create a config file in a folder with the columns that need to be validated.  
  Name the file as you wish, but remember to use the name in the DqvPydeequ function.

- Step 6: Upload your data to S3 and save it in a new directory if you are running locally.

- Step 7: Pass your source and target file paths in the DqvPydeequ function.

   ```
   DqvPydeequ(
        "", #config_file
        "", #source_data_path
        "") #target_data_path
   ```

- Step 8: Run the file to validate.

- Step 9: After validating the data, the result can be sent via email.  
  For this, import the library as below:  
  `from email_notification import sendEmailNotification`

- Step 10: save your aws administration imputs, sender email, and region as dictionary.
  Then pass source path, target path and this config in the sendEmailNotification function.

   ```
   email_config = {
    "aws_access_key_id": "", #aws administration
    "aws_secret_access_key": "", #aws administration
    "aws_session_token": "", #aws administration
    "sender_email": "", #sender email
    "receiver_email": "", #receiver email 
    "aws_region": "" #region
    }
   ```

  ``` 
   send_notification = sendEmailNotification(
        "", #source_data_path
        "", #target_data_path
        email_config #dictionary
    )
   ```  


<br></br>
Refer this repo to follow the structure of config file format  <br></br>
Git: <a href="https://github.com/dataruk/data-quality-validation">https://github.com/dataruk/data-quality-validation</a>