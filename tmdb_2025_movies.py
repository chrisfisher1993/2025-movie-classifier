import pandas as pd
import matplotlib.pyplot as plt

# =====================================================
# 1. LOAD IMDb DATA
# =====================================================

print("Loading IMDb data...")

DATA_PATH = "title.basics.tsv"

# Load IMDb TSV file into a DataFrame
df = pd.read_csv(
    DATA_PATH,
    sep="\t",
    low_memory=False
)

print("Rows loaded:", len(df))
print(df.head())


# =====================================================
# 2. FILTER TO MOVIES ONLY
# =====================================================

# Keep only rows where the title is a movie
movies = df[df["titleType"] == "movie"].copy()

# Convert startYear to numeric (IMDb uses '\N' for missing values)
movies["startYear"] = pd.to_numeric(movies["startYear"], errors="coerce")


# =====================================================
# 3. FILTER TO 2025 RELEASES
# =====================================================

# Select movies released in 2025
movies_2025 = movies[movies["startYear"] == 2025].copy()

print("2025 movies:", len(movies_2025))
print(movies_2025[["primaryTitle", "startYear", "genres"]].head())


# =====================================================
# 4. CLASSIFICATION FLAGS
# =====================================================

# ---- True story detection (Biography genre proxy)
movies_2025["is_true_story"] = movies_2025["genres"].str.contains(
    "Biography",
    na=False
)

# ---- Reboot / remake detection
# Any movie with the same title released before 2025
older_movies = movies[movies["startYear"] < 2025]
title_counts = older_movies["primaryTitle"].value_counts()

movies_2025["is_reboot"] = movies_2025["primaryTitle"].map(
    lambda title: title_counts.get(title, 0) > 0
)

# ---- Book adaptation proxy
# Common genres frequently adapted from books
movies_2025["is_book_adaptation"] = movies_2025["genres"].str.contains(
    "Drama|History|Biography|Romance",
    regex=True,
    na=False
)


# =====================================================
# 5. FINAL CATEGORY ASSIGNMENT
# =====================================================

def classify_movie(row):
    """
    Assign a single primary category to each movie
    using a priority-based rule set.
    """
    if row["is_reboot"]:
        return "Reboot / Remake"
    if row["is_true_story"]:
        return "Based on True Story"
    if row["is_book_adaptation"]:
        return "Based on Book"
    return "Original"


movies_2025["category"] = movies_2025.apply(classify_movie, axis=1)

print("\nCategory counts:")
print(movies_2025["category"].value_counts())

print("\nSample classified movies:")
print(
    movies_2025[
        ["primaryTitle", "genres", "category"]
    ].head(10)
)


# =====================================================
# 6. VISUALIZATION
# =====================================================

movies_2025["category"].value_counts().plot(kind="bar")
plt.title("2025 Movies by Source Type (IMDb)")
plt.ylabel("Number of Movies")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.show()

