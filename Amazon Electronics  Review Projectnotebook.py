
# COMMAND ----------

with open("./retail_db_dbricks.sql") as f:
    sql = f.read()

for statement in sql.split(";"):
    if statement is None or statement.strip() == "":
        print("Not executing empty statement.")
    else:
        spark.sql(statement)

# COMMAND ----------

categories = spark.table('workspace.retail_db.categories')
display(categories)


# COMMAND ----------

import urllib.request

url = "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/review_categories/Electronics.jsonl.gz"
out_file = "/Volumes/workspace/default/amazon_data/Electronics.jsonl.gz"

urllib.request.urlretrieve(url, out_file)
print("Downloaded to:", out_file)

# COMMAND ----------

display(dbutils.fs.ls("/Volumes/workspace/default/amazon_data/"))

# COMMAND ----------

df = spark.read.json("dbfs:/Volumes/workspace/default/amazon_data/Electronics.jsonl.gz")
display(df.limit(10))
df.printSchema()

# COMMAND ----------

df.write.mode("overwrite").saveAsTable("workspace.default.amazon_reviews_raw")

# COMMAND ----------

from pyspark.sql.functions import col, length, from_unixtime, to_timestamp, when

sample_df = (
    df
    .filter(col("rating").isNotNull())
    .sample(withReplacement=False, fraction=0.02, seed=42)
    .withColumn("review_length", length(col("text")))
    .withColumn("review_time", to_timestamp(from_unixtime(col("timestamp") / 1000)))
    .withColumn("helpful_vote", when(col("helpful_vote").isNull(), 0).otherwise(col("helpful_vote")))
)

display(sample_df.limit(10))

# COMMAND ----------

sample_df.write.mode("overwrite").saveAsTable("workspace.default.amazon_reviews_clean_sample")
print("sample clean table saved")

# COMMAND ----------

# Section 1: Import required libraries
# We use matplotlib for visualization and pandas conversion for plotting.

import matplotlib.pyplot as plt

# COMMAND ----------

# Section 2: KPI Summary Query
# This query calculates the overall project metrics:
# 1. Total number of reviews
# 2. Average rating
# 3. Average helpful votes

kpi_df = spark.sql("""
SELECT
  COUNT(*) AS total_reviews,
  ROUND(AVG(rating), 2) AS avg_rating,
  ROUND(AVG(helpful_vote), 2) AS avg_helpful_votes
FROM workspace.default.amazon_reviews_clean_sample
""")

# Display the query result in tabular format
display(kpi_df)

# COMMAND ----------

# Section 3: KPI Summary Charts
# Convert Spark DataFrame to Pandas DataFrame for plotting

kpi_pdf = kpi_df.toPandas()

# COMMAND ----------

# Chart 1: Total Reviews

plt.figure(figsize=(5,4))
plt.bar(["Total Reviews"], [kpi_pdf.loc[0, "total_reviews"]])
plt.xlabel("Metric")
plt.ylabel("Count")
plt.title("Total Reviews")
plt.tight_layout()
plt.show()

# COMMAND ----------

# Chart 2: Average Rating

plt.figure(figsize=(5,4))
plt.bar(["Average Rating"], [kpi_pdf.loc[0, "avg_rating"]])
plt.xlabel("Metric")
plt.ylabel("Rating")
plt.title("Average Rating")
plt.tight_layout()
plt.show()

# COMMAND ----------

# Chart 3: Average Helpful Votes

plt.figure(figsize=(5,4))
plt.bar(["Average Helpful Votes"], [kpi_pdf.loc[0, "avg_helpful_votes"]])
plt.xlabel("Metric")
plt.ylabel("Helpful Votes")
plt.title("Average Helpful Votes")
plt.tight_layout()
plt.show()

# COMMAND ----------

# Section 4: Verified Purchase Impact Query
# This query compares verified and non-verified reviews using:
# 1. Review count
# 2. Average helpful votes

verified_df = spark.sql("""
SELECT
  verified_purchase,
  COUNT(*) AS review_count,
  ROUND(AVG(helpful_vote), 2) AS avg_helpful_votes
FROM workspace.default.amazon_reviews_clean_sample
GROUP BY verified_purchase
""")

# Display the result
display(verified_df)

# COMMAND ----------

# Section 5: Verified Purchase Impact Charts
# Convert Spark DataFrame to Pandas DataFrame for plotting

verified_pdf = verified_df.toPandas()

# COMMAND ----------

# Chart 4: Verified Purchase vs Average Helpful Votes

plt.figure(figsize=(6,4))
plt.bar(verified_pdf["verified_purchase"].astype(str), verified_pdf["avg_helpful_votes"])
plt.xlabel("Verified Purchase")
plt.ylabel("Average Helpful Votes")
plt.title("Verified Purchase vs Average Helpful Votes")
plt.tight_layout()
plt.show()

# COMMAND ----------

# Chart 5: Review Count by Verification Status

plt.figure(figsize=(6,4))
plt.bar(verified_pdf["verified_purchase"].astype(str), verified_pdf["review_count"])
plt.xlabel("Verified Purchase")
plt.ylabel("Review Count")
plt.title("Review Count by Verification Status")
plt.tight_layout()
plt.show()

# COMMAND ----------

# Section 6: Monthly Rating Trend Query
# This query calculates monthly review trends using:
# 1. Review count by month
# 2. Average rating by month

trend_df = spark.sql("""
SELECT
  date_trunc('month', review_time) AS review_month,
  COUNT(*) AS review_count,
  ROUND(AVG(rating), 2) AS avg_rating
FROM workspace.default.amazon_reviews_clean_sample
GROUP BY date_trunc('month', review_time)
ORDER BY review_month
""")

# Display the result
display(trend_df)

# COMMAND ----------

# Section 7: Monthly Rating Trend Charts
# Convert Spark DataFrame to Pandas DataFrame for plotting

trend_pdf = trend_df.toPandas()

# COMMAND ----------

# Chart 6: Average Rating Trend Over Time

plt.figure(figsize=(12,5))
plt.plot(trend_pdf["review_month"], trend_pdf["avg_rating"])
plt.xlabel("Review Month")
plt.ylabel("Average Rating")
plt.title("Average Rating Trend Over Time")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# COMMAND ----------

# Chart 7: Review Volume Trend Over Time

plt.figure(figsize=(12,5))
plt.plot(trend_pdf["review_month"], trend_pdf["review_count"])
plt.xlabel("Review Month")
plt.ylabel("Review Count")
plt.title("Review Volume Trend Over Time")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# COMMAND ----------

# Section 8: Review Length Insight Query
# This query compares helpful and not helpful reviews using:
# 1. Review count
# 2. Average review length
# 3. Average rating

length_df = spark.sql("""
SELECT
  CASE
    WHEN helpful_vote >= 5 THEN 'Helpful'
    ELSE 'Not Helpful'
  END AS helpful_group,
  COUNT(*) AS review_count,
  ROUND(AVG(review_length), 2) AS avg_review_length,
  ROUND(AVG(rating), 2) AS avg_rating
FROM workspace.default.amazon_reviews_clean_sample
GROUP BY
  CASE
    WHEN helpful_vote >= 5 THEN 'Helpful'
    ELSE 'Not Helpful'
  END
""")

# Display the result
display(length_df)

# COMMAND ----------

# Section 9: Review Length Insight Charts
# Convert Spark DataFrame to Pandas DataFrame for plotting

length_pdf = length_df.toPandas()

# COMMAND ----------

# Chart 8: Helpful vs Not Helpful Review Length

plt.figure(figsize=(6,4))
plt.bar(length_pdf["helpful_group"], length_pdf["avg_review_length"])
plt.xlabel("Helpful Group")
plt.ylabel("Average Review Length")
plt.title("Helpful vs Not Helpful Review Length")
plt.tight_layout()
plt.show()

# COMMAND ----------

# Chart 9: Average Rating by Helpful Group

plt.figure(figsize=(6,4))
plt.bar(length_pdf["helpful_group"], length_pdf["avg_rating"])
plt.xlabel("Helpful Group")
plt.ylabel("Average Rating")
plt.title("Average Rating by Helpful Group")
plt.tight_layout()
plt.show()

# COMMAND ----------

# Section 10: Rating Distribution Query
# This query counts the number of reviews for each rating value.

rating_dist_df = spark.sql("""
SELECT
  rating,
  COUNT(*) AS review_count
FROM workspace.default.amazon_reviews_clean_sample
GROUP BY rating
ORDER BY rating
""")

# Display the result
display(rating_dist_df)

# COMMAND ----------

rating_pdf = rating_dist_df.toPandas()

# COMMAND ----------

# Section 11: Rating Distribution Chart
rating_pdf = rating_dist_df.toPandas()

# COMMAND ----------

# Chart 10: Review Count by Rating

plt.figure(figsize=(8,4))
plt.bar(rating_pdf["rating"].astype(str), rating_pdf["review_count"])
plt.xlabel("Rating")
plt.ylabel("Review Count")
plt.title("Review Count by Rating")
plt.tight_layout()
plt.show()

