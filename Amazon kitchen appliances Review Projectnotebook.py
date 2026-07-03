# Databricks notebook source
# Section 1: Import required libraries
# We use:
# urllib.request to download the dataset
# matplotlib for visualization
#  PySpark functions for cleaning and feature creation

import urllib.request
import matplotlib.pyplot as plt
from pyspark.sql.functions import col, length, from_unixtime, to_timestamp, when

# COMMAND ----------

# Section 2: Load, clean, and prepare Home and Kitchen review data
# Steps:
# 1. Download the Home_and_Kitchen review file into Databricks storage
# 2. Read the JSONL file into Spark
# 3. Remove rows with missing rating
# 4. Take a 1% sample for faster analysis
# 5. Create review_length
# 6. Convert timestamp into readable review_time
# 7. Replace missing helpful_vote with 0
# 8. Save the cleaned sample table

url = "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/review_categories/Home_and_Kitchen.jsonl.gz"
out_file = "/Volumes/workspace/default/amazon_data/Home_and_Kitchen.jsonl.gz"

urllib.request.urlretrieve(url, out_file)
print("Downloaded to:", out_file)

home_df = spark.read.json("dbfs:/Volumes/workspace/default/amazon_data/Home_and_Kitchen.jsonl.gz")
display(home_df.limit(10))
home_df.printSchema()

home_sample_df = (
    home_df
    .filter(col("rating").isNotNull())
    .sample(withReplacement=False, fraction=0.01, seed=42)
    .withColumn("review_length", length(col("text")))
    .withColumn("review_time", to_timestamp(from_unixtime(col("timestamp") / 1000)))
    .withColumn("helpful_vote", when(col("helpful_vote").isNull(), 0).otherwise(col("helpful_vote")))
)

display(home_sample_df.limit(10))

home_sample_df.write.mode("overwrite").saveAsTable("workspace.default.home_kitchen_reviews_clean_sample")
print("Home and Kitchen cleaned sample table saved")

# COMMAND ----------

# Section 3: KPI Summary
# This section calculates:
# 1. Total number of reviews
# 2. Average rating
# 3. Average helpful votes

home_kpi_df = spark.sql("""
SELECT
  COUNT(*) AS total_reviews,
  ROUND(AVG(rating), 2) AS avg_rating,
  ROUND(AVG(helpful_vote), 2) AS avg_helpful_votes
FROM workspace.default.home_kitchen_reviews_clean_sample
""")

display(home_kpi_df)

# COMMAND ----------

home_kpi_pdf = home_kpi_df.toPandas()

# COMMAND ----------

# Chart 1: Total Reviews

plt.figure(figsize=(5,4))
plt.bar(["Total Reviews"], [home_kpi_pdf.loc[0, "total_reviews"]])
plt.xlabel("Metric")
plt.ylabel("Count")
plt.title("Home & Kitchen - Total Reviews")
plt.tight_layout()
plt.show()

# COMMAND ----------

# Chart 2: Average Rating

plt.figure(figsize=(5,4))
plt.bar(["Average Rating"], [home_kpi_pdf.loc[0, "avg_rating"]])
plt.xlabel("Metric")
plt.ylabel("Rating")
plt.title("Home & Kitchen - Average Rating")
plt.tight_layout()
plt.show()

# COMMAND ----------

# Chart 3: Average Helpful Votes

plt.figure(figsize=(5,4))
plt.bar(["Average Helpful Votes"], [home_kpi_pdf.loc[0, "avg_helpful_votes"]])
plt.xlabel("Metric")
plt.ylabel("Helpful Votes")
plt.title("Home & Kitchen - Average Helpful Votes")
plt.tight_layout()
plt.show()

# COMMAND ----------

# Section 4: Verified Purchase Impact
# This section compares verified and non-verified reviews using:
# 1. Review count
# 2. Average helpful votes

home_verified_df = spark.sql("""
SELECT
  verified_purchase,
  COUNT(*) AS review_count,
  ROUND(AVG(helpful_vote), 2) AS avg_helpful_votes
FROM workspace.default.home_kitchen_reviews_clean_sample
GROUP BY verified_purchase
""")

display(home_verified_df)

# COMMAND ----------

# Convert Spark DataFrame to Pandas for plotting

home_verified_pdf = home_verified_df.toPandas()

# COMMAND ----------

# Chart 4: Verified Purchase vs Average Helpful Votes

plt.figure(figsize=(6,4))
plt.bar(home_verified_pdf["verified_purchase"].astype(str), home_verified_pdf["avg_helpful_votes"])
plt.xlabel("Verified Purchase")
plt.ylabel("Average Helpful Votes")
plt.title("Home & Kitchen - Verified Purchase vs Average Helpful Votes")
plt.tight_layout()
plt.show()

# COMMAND ----------

# Chart 5: Review Count by Verification Status

plt.figure(figsize=(6,4))
plt.bar(home_verified_pdf["verified_purchase"].astype(str), home_verified_pdf["review_count"])
plt.xlabel("Verified Purchase")
plt.ylabel("Review Count")
plt.title("Home & Kitchen - Review Count by Verification Status")
plt.tight_layout()
plt.show()

# COMMAND ----------

# Section 5: Monthly Rating Trend
# This section calculates:
# 1. Monthly review count
# 2. Monthly average rating

home_trend_df = spark.sql("""
SELECT
  date_trunc('month', review_time) AS review_month,
  COUNT(*) AS review_count,
  ROUND(AVG(rating), 2) AS avg_rating
FROM workspace.default.home_kitchen_reviews_clean_sample
GROUP BY date_trunc('month', review_time)
ORDER BY review_month
""")

display(home_trend_df)

# COMMAND ----------

# Convert Spark DataFrame to Pandas for plotting

home_trend_pdf = home_trend_df.toPandas()

# COMMAND ----------

# Chart 6: Average Rating Trend Over Time

plt.figure(figsize=(12,5))
plt.plot(home_trend_pdf["review_month"], home_trend_pdf["avg_rating"])
plt.xlabel("Review Month")
plt.ylabel("Average Rating")
plt.title("Home & Kitchen - Average Rating Trend Over Time")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# COMMAND ----------

# Chart 7: Review Volume Trend Over Time

plt.figure(figsize=(12,5))
plt.plot(home_trend_pdf["review_month"], home_trend_pdf["review_count"])
plt.xlabel("Review Month")
plt.ylabel("Review Count")
plt.title("Home & Kitchen - Review Volume Trend Over Time")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# COMMAND ----------

# Section 6: Review Length Insight
# This section compares Helpful vs Not Helpful reviews using:
# 1. Review count
# 2. Average review length
# 3. Average rating

home_length_df = spark.sql("""
SELECT
  CASE
    WHEN helpful_vote >= 5 THEN 'Helpful'
    ELSE 'Not Helpful'
  END AS helpful_group,
  COUNT(*) AS review_count,
  ROUND(AVG(review_length), 2) AS avg_review_length,
  ROUND(AVG(rating), 2) AS avg_rating
FROM workspace.default.home_kitchen_reviews_clean_sample
GROUP BY
  CASE
    WHEN helpful_vote >= 5 THEN 'Helpful'
    ELSE 'Not Helpful'
  END
""")

display(home_length_df)

# COMMAND ----------

# Convert Spark DataFrame to Pandas for plotting

home_length_pdf = home_length_df.toPandas()

# COMMAND ----------

# Chart 9: Average Rating by Helpful Group

plt.figure(figsize=(6,4))
plt.bar(home_length_pdf["helpful_group"], home_length_pdf["avg_rating"])
plt.xlabel("Helpful Group")
plt.ylabel("Average Rating")
plt.title("Home & Kitchen - Average Rating by Helpful Group")
plt.tight_layout()
plt.show()

# COMMAND ----------

# Section 7: Rating Distribution
# This section counts how many reviews fall into each rating value.

home_rating_dist_df = spark.sql("""
SELECT
  rating,
  COUNT(*) AS review_count
FROM workspace.default.home_kitchen_reviews_clean_sample
GROUP BY rating
ORDER BY rating
""")

display(home_rating_dist_df)

# COMMAND ----------

# Convert Spark DataFrame to Pandas for plotting

home_rating_pdf = home_rating_dist_df.toPandas()

# COMMAND ----------

# Chart 10: Review Count by Rating

plt.figure(figsize=(8,4))
plt.bar(home_rating_pdf["rating"].astype(str), home_rating_pdf["review_count"])
plt.xlabel("Rating")
plt.ylabel("Review Count")
plt.title("Home & Kitchen - Review Count by Rating")
plt.tight_layout()
plt.show()



