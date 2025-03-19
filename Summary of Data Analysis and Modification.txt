**Summary of Data Analysis and Modification**

### 1. **Analysis Objective**
The work focused on analyzing the relationship between GDP (Gross Domestic Product) and PISA (Programme for International Student Assessment) scores for 15-year-old students across different years. Techniques such as data cleaning, estimation, and machine learning were applied to improve data quality and enable a more robust analysis.

### 2. **Data Cleaning and Estimation**
- **Identification and treatment of missing values (NaN):**
  - An initial check was performed to identify missing values.
  - The **KNN Imputer** (K=5) was applied to fill NaN values, ensuring the dataset was more complete for analysis.
  - Imputed values were converted to integers when necessary to maintain data consistency.

- **Normalization and Standardization:**
  - The **StandardScaler** was used to normalize the data before estimation, preventing scale differences from affecting the results.
  - After estimation, the data was converted back to its original scale.

- **Rounding Values:**
  - GDP values were rounded to 5 decimal places.
  - Imputed scores were rounded and converted into integers.

### 3. **Creation of New Variables**
- Mean scores were calculated for Mathematics, Science, and Reading for the years 2012, 2015, and 2018.
- The means were rounded to three decimal places to maintain precision without compromising readability.

### 4. **Machine Learning Model for Filling Missing Data**
- A **RandomForestRegressor** was used to predict and fill missing score values.
- The categorical variables "Country" and "Subject" were encoded using **LabelEncoder** to allow input into the model.
- A validation check was performed on the predicted values, and results were rounded to maintain data consistency.
- The model's error was evaluated using RMSE (Root Mean Squared Error).

### 5. **Data Storage and Exportation**
- The updated dataset was saved in CSV format for future use.
- A confirmation message was included to indicate successful processing.

### **Conclusion**
The work ensured that the dataset was more complete, consistent, and ready for analysis. Advanced estimation and modeling techniques were applied to handle missing values and improve dataset quality. The generated analysis will allow for a more precise and reliable examination of the relationship between GDP and student performance.

