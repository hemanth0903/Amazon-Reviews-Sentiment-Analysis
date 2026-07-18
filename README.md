# 📊 Amazon Customer Reviews Analytics & Sentiment Analysis

## 💼 Business Problem

Every day, millions of customers leave product reviews on Amazon, influencing purchasing decisions, product rankings, and customer trust. While star ratings provide a quick measure of satisfaction, they rarely explain the reasons behind customer opinions.

In this project, I built an end-to-end analytics pipeline using Databricks, Apache Spark, and Natural Language Processing (NLP) to analyze customer reviews at scale. By combining structured review data with sentiment analysis, I generated insights into customer satisfaction, review quality, verified purchase behavior, and product performance.

The objective was not only to visualize data but also to produce actionable business recommendations that improve customer trust and support better decision-making.

Business teams need deeper insights into customer feedback to:
- Improve products and services
- Increase customer trust
- Enhance the shopping experience

This project focuses on answering several key business questions:

- Are verified purchase reviews more trustworthy?
- Which products receive the highest customer engagement?
- What characteristics make reviews more helpful?
- How does customer sentiment compare with star ratings?
- How do customer opinions evolve over time?

Without these insights, organizations risk making product decisions based solely on numerical ratings rather than understanding the true voice of the customer.


## 🎯 Business Objectives

The primary objective was to design and implement an end-to-end data analytics pipeline capable of transforming large-scale customer review data into meaningful business insights.

Specifically, I aimed to:

- Analyze customer rating behavior across products.
- Compare verified and non-verified purchases.
- Evaluate review helpfulness.
- Identify temporal trends in product ratings.
- Perform sentiment analysis on customer review text.
- Generate business recommendations based on analytical findings.

---

## ❓ Business Questions

The analysis was designed to answer the following questions:

1. **Customer Trust**
   - Do verified purchase reviews receive more helpful votes than non-verified reviews?

2. **Customer Satisfaction**
   - How are customer ratings distributed?
   - Are customers generally satisfied with the products?

3. **Product Performance**
   - Which products generate the highest customer engagement?

4. **Customer Behavior**
   - How do product ratings change over time?

5. **Customer Voice**
   - Does textual sentiment align with numerical ratings?

6. **Review Quality**
   - What characteristics distinguish highly helpful reviews from less helpful ones?

---

## 📈 Analysis and Findings

### ✅ Influence of Verified Purchase Status on Review Helpfulness

The analysis shows that verified purchase status has a substantial positive influence on review helpfulness. For the product categories examined, products with a higher share of verified reviews consistently received more helpful votes than non-verified reviews across ratings from 1 to 5. This suggests that increasing the share of verified reviews can strengthen user trust and improve the quality of purchase decisions.

<img width="665" height="335" alt="image" src="https://github.com/user-attachments/assets/8c42a288-17b2-4c24-ad08-070199a5b335" />


### ⏱️ Temporal Trends in Product Ratings and Review Volume

For high-volume categories, product ratings exhibit a gentle but consistent downward trend over time. In the categories analyzed, the appliances category showed an average rating decrease per year between 2003 and 2007, likely driven by post-launch enthusiasm, seasonal buying patterns, and event-driven drops (such as product issues or new competing releases). Understanding these trends helps businesses interpret rating changes in context rather than treating them as isolated signals.

<img width="593" height="327" alt="image" src="https://github.com/user-attachments/assets/470e6cfb-5e21-43c6-b76a-35ae12520220" />

