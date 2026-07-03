### Amazon Customer Reviews Analytics & Sentiment Analysis

## Executive Summary

Every day, millions of customers leave product reviews on Amazon. These reviews influence purchasing decisions, product rankings, and customer trust. While star ratings provide a quick measure of customer satisfaction, they often fail to explain the reasons behind customer opinions.

In this project, I built an end-to-end analytics pipeline using Databricks, Apache Spark, and Natural Language Processing (NLP) to analyze customer reviews at scale. By combining structured review data with sentiment analysis, I generated insights into customer satisfaction, review quality, verified purchase behavior, and product performance.

The objective was not only to visualize data but also to provide actionable business recommendations that could help improve customer trust and support better business decision


## Business Problem

Amazon receives millions of customer reviews every year. While numerical ratings provide an overall indication of customer satisfaction, they do not always capture the complete customer experience. Business teams require deeper insights into customer feedback to improve products, increase customer trust, and enhance the shopping experience.

This project focuses on answering several key business questions:

Are verified purchase reviews more trustworthy?
Which products receive the highest customer engagement?
What characteristics make reviews more helpful?
How does customer sentiment compare with star ratings?
How do customer opinions evolve over time?

Without these insights, organizations risk making product decisions based solely on numerical ratings rather than understanding the voice of the customer.


## Business Objectives

The primary objective of this project was to design and implement an end-to-end data analytics pipeline capable of transforming large-scale customer review data into meaningful business insights.

Specifically, I aimed to:

Analyze customer rating behavior across products.
Compare verified and non-verified purchases.
Evaluate review helpfulness.
Identify temporal trends in product ratings.
Perform sentiment analysis on customer review text.
Generate business recommendations based on analytical findings.


## Business Questions

The analysis was designed to answer the following questions:

1. Customer Trust

   Do verified purchase reviews receive more helpful votes than non-verified reviews?

2. Customer Satisfaction
   
How are customer ratings distributed?
Are customers generally satisfied with the products?

3. Product Performance

Which products generate the highest customer engagement?

4. Customer Behavior
   
How do product ratings change over time?

5. Customer Voice
   
Does textual sentiment align with numerical ratings?

6. Review Quality
   
What characteristics distinguish highly helpful reviews from less helpful ones?


### Analysis and Findings:

Influence of Verified Purchase Status on Review Helpfulness:
Our analysis confirms that verified purchase status has substantial positive influence on review helpfulness. For the product categories that we worked on, we noted that the products with most verified reviews has more helpful votes than the non-verified reviews. This was consistent for all ratings from 1 to 5. This implies that boosting verified reviews would be helpful for promoting user trust and decision quality.

Temporal Trends in Product Ratings and Correlation with Review Volume:
For high-volume categories, product ratings exhibit a gentle but consistent downward trend over time. In our categories, the appliances category shpwed an average rating decrease per year between 2003 and 2007. These could be due to post-launch spikes, seasonal patterns, and event-driven drops.

