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
# MAGIC CREATE OR REPLACE TEMP VIEW insurance_stage AS
# MAGIC SELECT
# MAGIC   TRIM(Policy_ID) AS policy_id,
# MAGIC   TRIM(Customer_ID) AS customer_id,
# MAGIC   TRIM(Claim_ID) AS claim_id,
# MAGIC
# MAGIC CASE
# MAGIC     WHEN Age IS NULL THEN NULL
# MAGIC     ELSE Age
# MAGIC END AS age_raw,
# MAGIC CASE
# MAGIC     WHEN gender IS NULL OR TRIM(Gender) = '' THEN 'Unknown'
# MAGIC     WHEN UPPER(TRIM(Gender)) IN ('M', 'MALE') THEN 'Male'
# MAGIC     WHEN UPPER(TRIM(Gender)) IN ('F', 'FEMALE') THEN 'Female'
# MAGIC     ELSE 'Unknown'
# MAGIC END AS gender,
# MAGIC CASE
# MAGIC     WHEN Province IS NULL OR TRIM(Province) = '' THEN 'Unknown'
# MAGIC
# MAGIC     WHEN UPPER(TRIM(Province)) IN ('GP', 'GAUTENG') THEN 'Gauteng'
# MAGIC     WHEN UPPER(TRIM(Province)) IN ('WC', 'WESTERN CAPE') THEN 'Western Cape'
# MAGIC     WHEN UPPER(TRIM(Province)) IN ('KZN', 'KWAZULU-NATAL') THEN 'KwaZulu-Natal'
# MAGIC     WHEN UPPER(TRIM(Province)) IN ('EC', 'EASTERN CAPE') THEN 'Eastern Cape'
# MAGIC     WHEN UPPER(TRIM(Province)) IN ('FS', 'FREE STATE') THEN 'Free State'
# MAGIC     WHEN UPPER(TRIM(Province)) IN ('NW', 'NORTH WEST') THEN 'North West'
# MAGIC     WHEN UPPER(TRIM(Province)) IN ('NC', 'NORTHERN CAPE') THEN 'Northern Cape'
# MAGIC     WHEN UPPER(TRIM(Province)) IN ('MP', 'MPUMALANGA') THEN 'Mpumalanga'
# MAGIC     WHEN UPPER(TRIM(Province)) IN ('LP', 'LIMPOPO') THEN 'Limpopo'
# MAGIC
# MAGIC     ELSE INITCAP(TRIM(Province))
# MAGIC END AS province,
# MAGIC CASE
# MAGIC     WHEN Monthly_Income IS NULL THEN NULL
# MAGIC     WHEN TRIM(Monthly_Income) = '' THEN NULL
# MAGIC     WHEN UPPER(TRIM(Monthly_Income)) IN ('N/A', 'NA', 'NULL') THEN NULL
# MAGIC     ELSE CAST(REGEXP_REPLACE(Monthly_Income, '[^0-9.]', '') AS DOUBLE)
# MAGIC END AS income_clean,
# MAGIC CASE
# MAGIC     WHEN Join_Date IS NULL THEN NULL
# MAGIC     WHEN TRIM(Join_Date) = '' THEN NULL
# MAGIC     WHEN UPPER(TRIM(Join_Date)) IN ('N/A', 'NA', 'NULL') THEN NULL
# MAGIC
# MAGIC     ELSE COALESCE(
# MAGIC         TRY_TO_DATE(TRIM(Join_Date), 'yyyy-MM-dd'),
# MAGIC         TRY_TO_DATE(TRIM(Join_Date), 'dd/MM/yyyy'),
# MAGIC         TRY_TO_DATE(TRIM(Join_Date), 'MM-dd-yyyy'),
# MAGIC         TRY_TO_DATE(TRIM(Join_Date), 'yyyy/MM/dd'),
# MAGIC         TRY_TO_DATE(TRIM(Join_Date), 'dd-MMM-yyyy'),
# MAGIC         TRY_TO_DATE(TRIM(Join_Date), 'MM/dd/yyyy')
# MAGIC     )
# MAGIC END AS join_date_clean,
# MAGIC CASE
# MAGIC     WHEN policy_type IS NULL OR TRIM(Policy_Type) = '' THEN 'Unknown'
# MAGIC
# MAGIC     WHEN LOWER(TRIM(Policy_Type)) = 'auto' THEN 'Auto'
# MAGIC     WHEN LOWER(TRIM(Policy_Type)) = 'motor' THEN 'Motor'
# MAGIC
# MAGIC     WHEN LOWER(TRIM(Policy_Type)) = 'health' THEN 'Health'
# MAGIC     WHEN LOWER(TRIM(Policy_Type)) = 'medical' THEN 'Medical'
# MAGIC
# MAGIC     WHEN LOWER(TRIM(Policy_Type)) = 'life' THEN 'Life'
# MAGIC     WHEN LOWER(TRIM(Policy_Type)) = 'funeral' THEN 'Funeral'
# MAGIC     WHEN LOWER(TRIM(Policy_Type)) = 'home' THEN 'Home'
# MAGIC
# MAGIC     ELSE INITCAP(TRIM(Policy_Type))
# MAGIC END AS policy_type,
# MAGIC CASE
# MAGIC     WHEN Premium_Amount IS NULL THEN NULL
# MAGIC     WHEN TRIM(Premium_Amount) = '' THEN NULL
# MAGIC     WHEN UPPER(TRIM(Premium_Amount)) IN ('N/A', 'NA', 'NULL') THEN NULL
# MAGIC
# MAGIC     ELSE CAST(
# MAGIC         REGEXP_REPLACE(TRIM(Premium_Amount), '[^0-9.]', '') 
# MAGIC         AS DOUBLE
# MAGIC     )
# MAGIC END AS premium_amount,
# MAGIC CASE
# MAGIC     WHEN Policy_Status IS NULL THEN 'Unknown'
# MAGIC     WHEN TRIM(Policy_Status) = '' THEN 'Unknown'
# MAGIC
# MAGIC     WHEN UPPER(TRIM(Policy_Status)) = 'ACTIVE' THEN 'Active'
# MAGIC     WHEN UPPER(TRIM(Policy_Status)) = 'CANCELLED' THEN 'Cancelled'
# MAGIC     WHEN UPPER(TRIM(Policy_Status)) = 'LAPSED' THEN 'Lapsed'
# MAGIC
# MAGIC     ELSE INITCAP(TRIM(Policy_Status))
# MAGIC END AS policy_status,
# MAGIC CASE
# MAGIC     WHEN Claim_Date IS NULL THEN NULL
# MAGIC     WHEN TRIM(Claim_Date) = '' THEN NULL
# MAGIC     WHEN UPPER(TRIM(Claim_Date)) IN ('N/A', 'NA', 'NULL') THEN NULL
# MAGIC
# MAGIC     ELSE COALESCE(
# MAGIC         TRY_TO_DATE(TRIM(Claim_Date), 'yyyy-MM-dd'),
# MAGIC         TRY_TO_DATE(TRIM(Claim_Date), 'dd/MM/yyyy'),
# MAGIC         TRY_TO_DATE(TRIM(Claim_Date), 'MM-dd-yyyy'),
# MAGIC         TRY_TO_DATE(TRIM(Claim_Date), 'yyyy/MM/dd'),
# MAGIC         TRY_TO_DATE(TRIM(Claim_Date), 'dd-MMM-yyyy'),
# MAGIC         TRY_TO_DATE(TRIM(Claim_Date), 'MM/dd/yyyy')
# MAGIC     )
# MAGIC END AS claim_date_clean,
# MAGIC CASE
# MAGIC     WHEN Claim_Amount IS NULL THEN NULL
# MAGIC     WHEN TRIM(Claim_Amount) = '' THEN NULL
# MAGIC     WHEN UPPER(TRIM(Claim_Amount)) IN ('N/A', 'NA', 'NULL') THEN NULL
# MAGIC
# MAGIC     ELSE CAST(
# MAGIC         REGEXP_REPLACE(TRIM(Claim_Amount), '[^0-9.]', '') 
# MAGIC         AS DOUBLE
# MAGIC     )
# MAGIC END AS claim_amount_clean,
# MAGIC CASE
# MAGIC     WHEN Claim_Status IS NULL THEN 'Unknown'
# MAGIC     WHEN TRIM(Claim_Status) = '' THEN 'Unknown'
# MAGIC
# MAGIC     WHEN UPPER(TRIM(Claim_Status)) = 'APPROVED' THEN 'Approved'
# MAGIC     WHEN UPPER(TRIM(Claim_Status)) = 'REJECTED' THEN 'Rejected'
# MAGIC     WHEN UPPER(TRIM(Claim_Status)) = 'DECLINED' THEN 'Declined'
# MAGIC     WHEN UPPER(TRIM(Claim_Status)) = 'PENDING' THEN 'Pending'
# MAGIC     WHEN UPPER(TRIM(Claim_Status)) IN ('IN REVIEW', 'UNDER REVIEW') THEN 'In Review'
# MAGIC
# MAGIC     ELSE INITCAP(TRIM(Claim_Status))
# MAGIC END AS claim_status,
# MAGIC CASE
# MAGIC     WHEN Fraud_Flag IS NULL THEN 'Unknown'
# MAGIC     WHEN TRIM(Fraud_Flag) = '' THEN 'Unknown'
# MAGIC
# MAGIC     WHEN UPPER(TRIM(Fraud_Flag)) IN ('YES', 'Y', '1') THEN 'Yes'
# MAGIC     WHEN UPPER(TRIM(Fraud_Flag)) IN ('NO', 'N', '0') THEN 'No'
# MAGIC
# MAGIC     ELSE INITCAP(TRIM(Fraud_Flag))
# MAGIC END AS fraud_flag
# MAGIC FROM insurance_data_raw

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * 
# MAGIC FROM insurance_stage

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   SUM(CASE WHEN age_raw IS NULL THEN 1 ELSE 0 END) AS null_age_after_cleaning,
# MAGIC   SUM(CASE WHEN age_raw < 18 OR age_raw > 100 THEN 1 ELSE 0 END) AS invalid_age_after_cleaning,
# MAGIC
# MAGIC   SUM(CASE WHEN premium_amount IS NULL THEN 1 ELSE 0 END) AS null_premium_after_cleaning,
# MAGIC   SUM(CASE WHEN premium_amount <= 0 THEN 1 ELSE 0 END) AS invalid_premium_after_cleaning,
# MAGIC
# MAGIC   SUM(CASE WHEN claim_amount_clean IS NULL THEN 1 ELSE 0 END) AS null_claim_after_cleaning,
# MAGIC   SUM(CASE WHEN claim_amount_clean < 0 THEN 1 ELSE 0 END) AS negative_claims_after_cleaning,
# MAGIC
# MAGIC   SUM(CASE WHEN claim_date_clean IS NULL THEN 1 ELSE 0 END) AS null_dates_after_cleaning
# MAGIC
# MAGIC FROM insurance_stage;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW insurance_clean AS
# MAGIC WITH deduped AS (
# MAGIC   SELECT *,
# MAGIC          ROW_NUMBER() OVER (
# MAGIC            PARTITION BY policy_id, customer_id, claim_id
# MAGIC            ORDER BY policy_id
# MAGIC          ) AS rn
# MAGIC   FROM insurance_stage
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC   policy_id,
# MAGIC   customer_id,
# MAGIC   claim_id,
# MAGIC
# MAGIC   age_raw AS age,  -- since we filter in WHERE
# MAGIC
# MAGIC   gender,
# MAGIC   province,
# MAGIC   join_date_clean AS join_date,
# MAGIC   policy_type,
# MAGIC   premium_amount,
# MAGIC
# MAGIC   CASE
# MAGIC     WHEN claim_amount_clean IS NULL THEN 0
# MAGIC     WHEN claim_amount_clean >= 0 THEN claim_amount_clean
# MAGIC     ELSE NULL
# MAGIC   END AS claim_amount,
# MAGIC
# MAGIC   policy_status,
# MAGIC   claim_status,
# MAGIC   claim_date_clean AS claim_date,
# MAGIC   fraud_flag,
# MAGIC   income_clean AS income
# MAGIC
# MAGIC FROM deduped
# MAGIC WHERE rn = 1
# MAGIC   AND age_raw BETWEEN 18 AND 100
# MAGIC   AND (claim_amount_clean IS NULL OR claim_amount_clean >= 0);

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   COUNT(*) AS cleaned_rows,
# MAGIC   COUNT(DISTINCT policy_id) AS distinct_policy_ids,
# MAGIC   SUM(CASE WHEN age IS NULL THEN 1 ELSE 0 END) AS null_age,
# MAGIC   SUM(CASE WHEN premium_amount IS NULL THEN 1 ELSE 0 END) AS null_premium_amount,
# MAGIC   SUM(CASE WHEN claim_amount < 0 THEN 1 ELSE 0 END) AS negative_claim_amount,
# MAGIC   SUM(CASE WHEN join_date IS NULL THEN 1 ELSE 0 END) AS null_policy_start_date
# MAGIC FROM insurance_clean;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT distinct policy_type
# MAGIC FROM insurance_clean
# MAGIC -- LIMIT 20;

# COMMAND ----------

# MAGIC %sql
# MAGIC select *
# MAGIC from insurance_clean

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC   policy_type,
# MAGIC   COUNT(*) AS total_policies,
# MAGIC   ROUND(AVG(premium_amount), 2) AS avg_premium
# MAGIC FROM insurance_clean
# MAGIC GROUP BY policy_type
# MAGIC ORDER BY total_policies DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   province,
# MAGIC   ROUND(SUM(claim_amount), 2) AS total_claim_amount
# MAGIC FROM insurance_clean
# MAGIC GROUP BY province
# MAGIC ORDER BY total_claim_amount DESC;