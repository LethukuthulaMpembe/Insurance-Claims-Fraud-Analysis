# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW insurance_data_raw
# MAGIC using csv
# MAGIC options (
# MAGIC   path '/Volumes/workspace/dataforge/dfa_files/dfa_insurance_project_raw_dataset.csv',
# MAGIC   header = true,
# MAGIC   inferSchema = true 
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM insurance_data_raw;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     COUNT(*) AS total_rows,
# MAGIC     COUNT(DISTINCT Customer_ID) AS total_customers,
# MAGIC     COUNT(DISTINCT Policy_ID) AS total_policies,
# MAGIC     COUNT(DISTINCT Claim_ID) AS total_claims
# MAGIC FROM insurance_data_raw;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     SUM(CASE WHEN Customer_ID IS NULL OR TRIM(Customer_ID) = '' THEN 1 ELSE 0 END) AS missing_customer_id,
# MAGIC     SUM(CASE WHEN Age IS NULL THEN 1 ELSE 0 END) AS missing_age,
# MAGIC     SUM(CASE WHEN Gender IS NULL OR TRIM(Gender) = '' THEN 1 ELSE 0 END) AS missing_gender,
# MAGIC     SUM(CASE WHEN Province IS NULL OR TRIM(Province) = '' THEN 1 ELSE 0 END) AS missing_province,
# MAGIC     SUM(CASE WHEN Monthly_Income IS NULL THEN 1 ELSE 0 END) AS missing_monthlyincome,
# MAGIC     SUM(CASE WHEN Join_Date IS NULL OR TRIM(Join_Date) = '' THEN 1 ELSE 0 END) AS missing_join_date,
# MAGIC     SUM(CASE WHEN Policy_ID IS NULL OR TRIM(Policy_ID) = '' THEN 1 ELSE 0 END) AS missing_policy_id,
# MAGIC     SUM(CASE WHEN Policy_Type IS NULL OR TRIM(Policy_Type) = '' THEN 1 ELSE 0 END) AS missing_policy_type,
# MAGIC     SUM(CASE WHEN Premium_Amount IS NULL THEN 1 ELSE 0 END) AS missing_premium,
# MAGIC     SUM(CASE WHEN Policy_Status IS NULL OR TRIM(Policy_Status) = '' THEN 1 ELSE 0 END) AS missing_policy_status,
# MAGIC     SUM(CASE WHEN Claim_ID IS NULL OR TRIM(Claim_ID) = '' THEN 1 ELSE 0 END) AS missing_claim_id,
# MAGIC     SUM(CASE WHEN Claim_Date IS NULL OR TRIM(Claim_Date) = '' THEN 1 ELSE 0 END) AS missing_claim_date,
# MAGIC     SUM(CASE WHEN Claim_Amount IS NULL THEN 1 ELSE 0 END) AS missing_claim_amount,
# MAGIC     SUM(CASE WHEN Claim_Status IS NULL OR TRIM(Claim_Status) = '' THEN 1 ELSE 0 END) AS missing_claim_status,
# MAGIC     SUM(CASE WHEN Fraud_Flag IS NULL OR TRIM(Fraud_Flag) = '' THEN 1 ELSE 0 END) AS missing_fraud_flag
# MAGIC FROM insurance_data_raw;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC   policy_id,
# MAGIC   COUNT(*) AS row_count
# MAGIC FROM insurance_data_raw
# MAGIC where claim_status = 'Approved'
# MAGIC GROUP BY policy_id
# MAGIC HAVING COUNT(*) > 1
# MAGIC ORDER BY row_count DESC, policy_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     Claim_ID,
# MAGIC     COUNT(*) AS duplicate_count
# MAGIC FROM insurance_data_raw
# MAGIC GROUP BY Claim_ID
# MAGIC HAVING COUNT(*) > 1;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT DISTINCT Gender
# MAGIC FROM insurance_data_raw;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT DISTINCT Policy_Type
# MAGIC FROM insurance_data_raw;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT DISTINCT Claim_Status
# MAGIC FROM insurance_data_raw;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT DISTINCT Fraud_Flag
# MAGIC FROM insurance_data_raw;

# COMMAND ----------

# DBTITLE 1,Cell 11
# MAGIC %sql
# MAGIC SELECT 
# MAGIC     SUM(CAST(REGEXP_REPLACE(TRIM(Claim_Amount), '[^0-9.-]', '') AS DOUBLE)) AS total_claim_amount
# MAGIC FROM insurance_data_raw;

# COMMAND ----------

# DBTITLE 1,Cell 12
# MAGIC %sql
# MAGIC SELECT 
# MAGIC     AVG(CAST(REGEXP_REPLACE(TRIM(Claim_Amount), '[^0-9.-]', '') AS DOUBLE)) AS avg_claim_amount
# MAGIC FROM insurance_data_raw;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     Province,
# MAGIC     COUNT(Claim_ID) AS total_claims,
# MAGIC     SUM(CAST(REGEXP_REPLACE(TRIM(Claim_Amount), '[^0-9.-]', '') AS DOUBLE)) AS total_claim_amount,
# MAGIC     AVG(CAST(REGEXP_REPLACE(TRIM(Claim_Amount), '[^0-9.-]', '') AS DOUBLE)) AS avg_claim_amount
# MAGIC FROM insurance_data_raw
# MAGIC GROUP BY Province
# MAGIC ORDER BY total_claim_amount DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     Customer_ID,
# MAGIC     Policy_Type,
# MAGIC     Province,
# MAGIC     Claim_ID,
# MAGIC     Claim_Amount
# MAGIC FROM insurance_data_raw
# MAGIC ORDER BY Claim_Amount DESC
# MAGIC LIMIT 5;