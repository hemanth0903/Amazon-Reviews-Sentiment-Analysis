# Databricks notebook source
# Section 1: Import required libraries
# We use matplotlib for visualization.

import urllib.request
import matplotlib.pyplot as plt
from pyspark.sql.functions import col, length, from_unixtime, to_timestamp, when

# COMMAND ----------

# Section 2: Load, clean, and prepare Books review data
# Steps:
# 1. Download the Books review file into Databricks storage
# 2. Read the JSONL file into Spark
# 3. Remove rows with missing rating
# 4. Take a 1% sample for faster analysis
# 5. Create review_length
# 6. Convert timestamp into readable review_time
# 7. Replace missing helpful_vote with 0
# 8. Save the cleaned sample table

# Download Books dataset
url = "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/review_categories/Books.jsonl.gz"
out_file = "/Volumes/workspace/default/amazon_data/Books.jsonl.gz"

urllib.request.urlretrieve(url, out_file)
print("Downloaded to:", out_file)

# Read Books dataset
books_df = spark.read.json("dbfs:/Volumes/workspace/default/amazon_data/Books.jsonl.gz")
display(books_df.limit(10))
books_df.printSchema()

# Clean and sample Books data
books_sample_df = (
    books_df
    .filter(col("rating").isNotNull())
    .sample(withReplacement=False, fraction=0.01, seed=42)
    .withColumn("review_length", length(col("text")))
    .withColumn("review_time", to_timestamp(from_unixtime(col("timestamp") / 1000)))
    .withColumn("helpful_vote", when(col("helpful_vote").isNull(), 0).otherwise(col("helpful_vote")))
)

display(books_sample_df.limit(10))

# Save cleaned sample table
books_sample_df.write.mode("overwrite").saveAsTable("workspace.default.books_reviews_clean_sample")
print("Books cleaned sample table saved")

# COMMAND ----------

# Section 3: KPI Summary
# This section calculates:
# 1. Total number of reviews
# 2. Average rating
# 3. Average helpful votes

books_kpi_df = spark.sql("""
SELECT
  COUNT(*) AS total_reviews,
  ROUND(AVG(rating), 2) AS avg_rating,
  ROUND(AVG(helpful_vote), 2) AS avg_helpful_votes
FROM workspace.default.books_reviews_clean_sample
""")

display(books_kpi_df)

# COMMAND ----------

# Convert Spark DataFrame to Pandas for KPI charts
books_kpi_pdf = books_kpi_df.toPandas()

# COMMAND ----------

# Chart 1: Total Reviews
plt.figure(figsize=(5,4))
plt.bar(["Total Reviews"], [books_kpi_pdf.loc[0, "total_reviews"]])
plt.xlabel("Metric")
plt.ylabel("Count")
plt.title("Books - Total Reviews")
plt.tight_layout()
plt.show()

# COMMAND ----------

# Chart 2: Average Rating
plt.figure(figsize=(5,4))
plt.bar(["Average Rating"], [books_kpi_pdf.loc[0, "avg_rating"]])
plt.xlabel("Metric")
plt.ylabel("Rating")
plt.title("Books - Average Rating")
plt.tight_layout()
plt.show()

# COMMAND ----------

# Chart 3: Average Helpful Votes
plt.figure(figsize=(5,4))
plt.bar(["Average Helpful Votes"], [books_kpi_pdf.loc[0, "avg_helpful_votes"]])
plt.xlabel("Metric")
plt.ylabel("Helpful Votes")
plt.title("Books - Average Helpful Votes")
plt.tight_layout()
plt.show()

# COMMAND ----------

# Section 4: Verified Purchase Impact
# This section compares verified and non-verified reviews using:
# 1. Review count
# 2. Average helpful votes

books_verified_df = spark.sql("""
SELECT
  verified_purchase,
  COUNT(*) AS review_count,
  ROUND(AVG(helpful_vote), 2) AS avg_helpful_votes
FROM workspace.default.books_reviews_clean_sample
GROUP BY verified_purchase
""")

display(books_verified_df)

# COMMAND ----------

# Convert Spark DataFrame to Pandas for plotting
books_verified_pdf = books_verified_df.toPandas()

# COMMAND ----------

# Chart 4: Verified Purchase vs Average Helpful Votes
plt.figure(figsize=(6,4))
plt.bar(books_verified_pdf["verified_purchase"].astype(str), books_verified_pdf["avg_helpful_votes"])
plt.xlabel("Verified Purchase")
plt.ylabel("Average Helpful Votes")
plt.title("Books - Verified Purchase vs Average Helpful Votes")
plt.tight_layout()
plt.show()

# COMMAND ----------

# Chart 5: Review Count by Verification Status
plt.figure(figsize=(6,4))
plt.bar(books_verified_pdf["verified_purchase"].astype(str), books_verified_pdf["review_count"])
plt.xlabel("Verified Purchase")
plt.ylabel("Review Count")
plt.title("Books - Review Count by Verification Status")
plt.tight_layout()
plt.show()

# COMMAND ----------

# Section 5: Monthly Rating Trend
# This section calculates:
# 1. Monthly review count
# 2. Monthly average rating

books_trend_df = spark.sql("""
SELECT
  date_trunc('month', review_time) AS review_month,
  COUNT(*) AS review_count,
  ROUND(AVG(rating), 2) AS avg_rating
FROM workspace.default.books_reviews_clean_sample
WHERE review_time < '2023-10-01'
GROUP BY date_trunc('month', review_time)
ORDER BY review_month
""")
print(books_trend_pdf["review_month"].max())

# COMMAND ----------

# Convert Spark DataFrame to Pandas for plotting
books_trend_pdf = books_trend_df.toPandas()

# COMMAND ----------

# Chart 6: Average Rating Trend Over Time


books_trend_pdf = books_trend_df.toPandas()
books_trend_pdf["review_month"] = pd.to_datetime(books_trend_pdf["review_month"])

plt.figure(figsize=(12,5))
plt.plot(books_trend_pdf["review_month"], books_trend_pdf["avg_rating"])
plt.xlabel("Review Month")
plt.ylabel("Average Rating")
plt.title("Books - Average Rating Trend Over Time")
plt.xlim(pd.Timestamp("1996-01-01"), pd.Timestamp("2023-12-31"))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# COMMAND ----------

# Chart 7: Review Volume Trend Over Time
plt.figure(figsize=(12,5))
plt.plot(books_trend_pdf["review_month"], books_trend_pdf["review_count"])
plt.xlabel("Review Month")
plt.ylabel("Review Count")
plt.title("Books - Review Volume Trend Over Time")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# COMMAND ----------

# Section 6: Review Length Insight
# This section compares Helpful vs Not Helpful reviews using:
# 1. Review count
# 2. Average review length
# 3. Average rating

books_length_df = spark.sql("""
SELECT
  CASE
    WHEN helpful_vote >= 5 THEN 'Helpful'
    ELSE 'Not Helpful'
  END AS helpful_group,
  COUNT(*) AS review_count,
  ROUND(AVG(review_length), 2) AS avg_review_length,
  ROUND(AVG(rating), 2) AS avg_rating
FROM workspace.default.books_reviews_clean_sample
GROUP BY
  CASE
    WHEN helpful_vote >= 5 THEN 'Helpful'
    ELSE 'Not Helpful'
  END
""")

display(books_length_df)

# COMMAND ----------

# Convert Spark DataFrame to Pandas for plotting
books_length_pdf = books_length_df.toPandas()

# COMMAND ----------

# Chart 8: Helpful vs Not Helpful Review Length
plt.figure(figsize=(6,4))
plt.bar(books_length_pdf["helpful_group"], books_length_pdf["avg_review_length"])
plt.xlabel("Helpful Group")
plt.ylabel("Average Review Length")
plt.title("Books - Helpful vs Not Helpful Review Length")
plt.tight_layout()
plt.show()

# COMMAND ----------

# Chart 9: Average Rating by Helpful Group
plt.figure(figsize=(6,4))
plt.bar(books_length_pdf["helpful_group"], books_length_pdf["avg_rating"])
plt.xlabel("Helpful Group")
plt.ylabel("Average Rating")
plt.title("Books - Average Rating by Helpful Group")
plt.tight_layout()
plt.show()

# COMMAND ----------

# Section 7: Rating Distribution
# This section counts how many reviews fall into each rating value.

books_rating_dist_df = spark.sql("""
SELECT
  rating,
  COUNT(*) AS review_count
FROM workspace.default.books_reviews_clean_sample
GROUP BY rating
ORDER BY rating
""")

display(books_rating_dist_df)

# COMMAND ----------

# Convert Spark DataFrame to Pandas for plotting
books_rating_pdf = books_rating_dist_df.toPandas()

# COMMAND ----------

# Chart 10: Review Count by Rating
plt.figure(figsize=(8,4))
plt.bar(books_rating_pdf["rating"].astype(str), books_rating_pdf["review_count"])
plt.xlabel("Rating")
plt.ylabel("Review Count")
plt.title("Books - Review Count by Rating")
plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC # Section 8: Summary
# MAGIC # This notebook analyzes Amazon Books reviews using Spark SQL and Python visualization.
# MAGIC # Main insights covered:
# MAGIC # 1. Overall KPI metrics
# MAGIC # 2. Verified purchase impact
# MAGIC # 3. Monthly rating and review trends
# MAGIC # 4. Review length differences
# MAGIC # 5. Rating distribution

# COMMAND ----------

