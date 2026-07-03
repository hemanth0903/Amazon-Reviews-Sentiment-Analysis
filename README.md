Amazon Customer Review Intelligence Platform

Executive Summary

Every day, millions of customers leave product reviews on Amazon.

These reviews influence purchasing decisions, product rankings, and customer trust. However, manually analyzing millions of reviews is impossible.

This project demonstrates how modern data analytics can transform raw customer reviews into actionable business insights using Databricks, Apache Spark, and Natural Language Processing (NLP).

Rather than simply building dashboards, this project focuses on answering important business questions regarding customer satisfaction, review quality, and purchasing behavior.



Business Problem

Amazon receives millions of customer reviews every year.

Although ratings provide a quick measure of customer satisfaction, they often fail to explain why customers feel a certain way.

Business teams need to understand:

Which products are actually satisfying customers?
Are verified purchases more trustworthy?
What characteristics make reviews helpful?
How does customer sentiment compare with star ratings?
How do customer opinions change over time?

Without these insights, businesses risk making product decisions based only on numerical ratings rather than actual customer feedback.


Business Objectives

The primary objective of this project was to build an end-to-end analytics pipeline capable of transforming customer reviews into actionable insights.

Specifically, this project aimed to:

Analyze customer rating behavior
Compare verified and non-verified reviews
Understand review helpfulness
Identify temporal rating trends
Perform sentiment analysis on customer feedback
Deliver business recommendations supported by data


Business Questions

The analysis focused on answering the following questions.

Customer Trust

Do verified purchases receive more helpful votes than non-verified purchases?

Customer Satisfaction

How are product ratings distributed?

Are customers generally satisfied?

Product Performance

Which products receive the highest customer engagement?

Customer Behavior

How do ratings change over time?

Customer Voice

Does review sentiment always match numerical ratings?

Review Quality

What characteristics make a review helpful?


Dataset

The project uses the Amazon Reviews 2023 Dataset.

The dataset includes:

Product ID (ASIN)
Customer ID
Review Text
Rating
Timestamp
Verified Purchase Status
Helpful Votes

The combination of structured and unstructured data makes the dataset suitable for advanced analytics.
