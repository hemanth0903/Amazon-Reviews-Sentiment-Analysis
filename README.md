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


## 📈 Analysis and Findings

### ✅ Influence of Verified Purchase Status on Review Helpfulness

The analysis shows that verified purchase status has a substantial positive influence on review helpfulness. For the product categories examined, products with a higher share of verified reviews consistently received more helpful votes than non-verified reviews across ratings from 1 to 5. This suggests that increasing the share of verified reviews can strengthen user trust and improve the quality of purchase decisions.

<img width="665" height="335" alt="image" src="https://github.com/user-attachments/assets/8c42a288-17b2-4c24-ad08-070199a5b335" />




### ⏱️ Temporal Trends in Product Ratings and Review Volume

For high-volume categories, product ratings exhibit a gentle but consistent downward trend over time. In the categories analyzed, the appliances category showed an average rating decrease per year between 2003 and 2007, likely driven by post-launch enthusiasm, seasonal buying patterns, and event-driven drops (such as product issues or new competing releases). Understanding these trends helps businesses interpret rating changes in context rather than treating them as isolated signals.

<img width="593" height="327" alt="image" src="https://github.com/user-attachments/assets/470e6cfb-5e21-43c6-b76a-35ae12520220" />



## Sentiment vs Rating:

The first screenshot indicates that the customers prefer products which are highly rated having maximum number of customers and decreases as we go down the rating. 

<img width="853" height="415" alt="image" src="https://github.com/user-attachments/assets/6ad3ec9f-29d1-4666-bdf8-9042ee471a92" />

The average product rating starts at approximately 3.0 in the year 2000 and initially exhibited considerable fluctuations. Between 2000 and 2008, the average rating oscillated between 4.0 and 5.0, indicating varying levels of customer satisfaction during the early years. After 2008, the trend became relatively more stable, with the average rating generally remaining below 4.25 and showing fewer sharp fluctuations. A noticeable decline was observed around 2023, where the average rating dropped below its typical range. This could be due to the product did not get that much acceptance during it's launch. The more stable ratings after 2008 could be due to the products have reached their mature stage in the lifecycle. The decline over the years after that could be due to launch of new products in the market, changing customer expectations.

<img width="874" height="431" alt="image" src="https://github.com/user-attachments/assets/3c9633bf-1f4c-4df4-9ece-64046b7bad69" />


---



