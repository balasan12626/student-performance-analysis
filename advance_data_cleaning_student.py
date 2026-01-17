
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

# Create images directory if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

df=pd.read_csv('StudentsPerformance0.csv')

print("Data loaded. Shape:", df.shape)

# Basic Info
# df.info()
# df.describe()
# df.isnull().sum()

# Handling Missing Values
for col in df.columns:
    if df[col].dtype == 'object':
        df[col].fillna(df[col].mode()[0], inplace=True)
    else:
        df[col].fillna(df[col].mean(), inplace=True)

# Remove Duplicates
df.drop_duplicates(inplace=True)

# Standardize Columns
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Visualization 1: Score Distribution
plt.figure(figsize=(10,5))
sns.boxplot(data=df[['math_score', 'reading_score', 'writing_score']])
plt.title("Score Distribution")
plt.savefig('images/score_distribution.png')
print("Saved images/score_distribution.png")
# plt.show()
plt.close()

# Clip Scores
score_cols = ['math_score', 'reading_score', 'writing_score']
for col in score_cols:
    df[col] = df[col].clip(0, 100)

# Clean Text Data
df['gender'] = df['gender'].str.lower().str.strip()
df['parental_level_of_education'] = df['parental_level_of_education'].str.lower()

# Calculate Average Score
df['average_score'] = df[score_cols].mean(axis=1)

# Save Cleaned Data
df.to_csv("cleaned_StudentsPerformance_Cleaned.csv", index=False)
print("Saved cleaned_StudentsPerformance_Cleaned.csv")

# Outlier Removal
z_scores = np.abs(stats.zscore(df[['math_score','reading_score','writing_score']]))
outliers = (z_scores > 3).any(axis=1)
df = df[~outliers]

# Visualization 2: Distribution of Average Score
plt.figure(figsize=(8,5))
sns.histplot(df['average_score'], kde=True)
plt.title("Distribution of Average Score")
plt.savefig('images/average_score_distribution.png')
print("Saved images/average_score_distribution.png")
# plt.show()
plt.close()

# Statistics
print("Skewness of Average Score:", df['average_score'].skew())

# Visualization 3: Correlation Matrix
plt.figure(figsize=(8,6))
sns.heatmap(df[['math_score','reading_score','writing_score','average_score']].corr(),
            annot=True, cmap='coolwarm')
plt.title("Score Correlation Matrix")
plt.savefig('images/correlation_matrix.png')
print("Saved images/correlation_matrix.png")
# plt.show()
plt.close()

# Visualization 4: Gender vs Average Score
plt.figure(figsize=(7,5))
sns.boxplot(x='gender', y='average_score', data=df)
plt.title("Gender vs Average Score")
plt.savefig('images/gender_vs_average_score.png')
print("Saved images/gender_vs_average_score.png")
# plt.show()
plt.close()

# Visualization 5: Test Preparation vs Performance
plt.figure(figsize=(7,5))
sns.barplot(x='test_preparation_course', y='average_score', data=df)
plt.title("Test Preparation vs Performance")
plt.savefig('images/test_preparation_impact.png')
print("Saved images/test_preparation_impact.png")
# plt.show()
plt.close()

# T-Test
prep = df[df['test_preparation_course'] == 'completed']['average_score']
no_prep = df[df['test_preparation_course'] == 'none']['average_score']
t_stat, p_val = stats.ttest_ind(prep, no_prep)
print(f"T-Test Results: statistic={t_stat}, pvalue={p_val}")

# Visualization 6: Pairplot
pair_plot = sns.pairplot(df,
             vars=['math_score','reading_score','writing_score'],
             hue='gender')
pair_plot.savefig('images/pairplot_gender.png')
print("Saved images/pairplot_gender.png")
# plt.show()
plt.close()

# Feature Engineering: Performance Level
def performance_label(score):
    if score >= 80:
        return "High"
    elif score >= 60:
        return "Medium"
    else:
        return "Low"

df['performance_level'] = df['average_score'].apply(performance_label)

# Visualization 7: Performance Levels
plt.figure(figsize=(8,5))
sns.countplot(x='performance_level', data=df)
plt.title("Student Performance Levels")
plt.savefig('images/performance_levels.png')
print("Saved images/performance_levels.png")
# plt.show()
plt.close()

# Save Final Analysis
df.to_csv("advance_StudentsPerformance_Advanced_Analysis.csv", index=False)
print("Saved advance_StudentsPerformance_Advanced_Analysis.csv")
print("Analysis Complete.")
