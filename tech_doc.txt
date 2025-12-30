# IMDb 2025 Movie Classification Script

## 1. Purpose and Overview

This script processes IMDb’s `title.basics.tsv` dataset to analyze movies released in the year 2025. It filters raw IMDb data to movie titles only, derives several heuristic classification flags, assigns each movie a primary source category, and visualizes the distribution of those categories.

The goal is not perfect attribution, but a **data-driven approximation** of whether 2025 movies are original works, reboots/remakes, based on true stories, or adapted from books.

---

## 2. Input Data

**Source file:** `title.basics.tsv`

This is an IMDb-provided TSV file containing metadata for all known titles. Relevant columns used in this script include:

* `titleType`: Identifies whether the entry is a movie, TV show, short, etc.
* `primaryTitle`: The primary release title of the work
* `startYear`: The release year
* `genres`: A comma-separated list of genres

IMDb uses the string `\\N` to represent missing values, which must be handled explicitly.

---

## 3. Library Dependencies

The script relies on two Python libraries:

* **pandas** – for data loading, filtering, transformation, and analysis
* **matplotlib** – for visualization of category counts

These libraries are industry-standard for lightweight data analysis workflows.

---

## 4. Data Loading Phase

The script begins by loading the IMDb TSV file into a pandas DataFrame:

* The tab separator is specified explicitly using `sep="\t"`
* `low_memory=False` ensures pandas performs full type inference upfront

This phase produces a raw DataFrame containing all IMDb title records.

---

## 5. Movie Filtering and Data Normalization

### 5.1 Movie-Only Filtering

IMDb includes many non-movie entries. The script filters rows where:

* `titleType == "movie"`

A `.copy()` call is used to avoid chained-assignment side effects later in the pipeline.

### 5.2 Year Conversion

The `startYear` column is converted from string to numeric using:

* `pd.to_numeric(errors="coerce")`

This safely converts invalid or missing year values to `NaN`, enabling numeric comparisons.

---

## 6. 2025 Release Selection

The script isolates movies released in 2025 by applying a strict equality filter:

* `startYear == 2025`

This produces a focused dataset (`movies_2025`) that all subsequent analysis is performed on.

---

## 7. Classification Flag Generation

Each movie is assigned several boolean flags that represent possible sources or origins.

### 7.1 True Story Detection

* Movies are flagged as `is_true_story` if their genres include `Biography`
* This serves as a proxy for real-world or historical narratives

Limitations: Not all true stories are labeled as biographies, and some biographies are fictionalized.

### 7.2 Reboot / Remake Detection

The script detects reboots by:

1. Selecting all movies released **before 2025**
2. Counting how many times each `primaryTitle` appears historically
3. Marking a 2025 movie as a reboot if the same title appeared in an earlier year

This approach assumes identical titles imply reuse or remake.

Limitations:

* Title reuse does not always indicate a reboot
* Does not account for IMDb IDs or franchises

### 7.3 Book Adaptation Proxy

Movies are flagged as `is_book_adaptation` if their genres include:

* Drama
* History
* Biography
* Romance

These genres statistically correlate with literary adaptations but are not definitive proof.

---

## 8. Category Assignment Logic

### 8.1 Classification Function

The `classify_movie` function assigns a **single primary category** to each movie using a priority-based rule system:

1. Reboot / Remake
2. Based on True Story
3. Based on Book
4. Original

This priority order ensures mutually exclusive classification, even when multiple flags are true.

### 8.2 Application

The function is applied row-by-row using:

* `DataFrame.apply(axis=1)`

The resulting category is stored in the `category` column.

---

## 9. Output and Reporting

The script produces several outputs:

* A count of movies per category
* A sample of classified movies for inspection

These outputs are printed to the console for transparency and debugging.

---

## 10. Visualization

A bar chart is generated to show the distribution of 2025 movies by source category:

* X-axis: Category
* Y-axis: Number of movies

The visualization provides a high-level overview of originality trends in 2025 film releases.

---

## 11. Design Considerations and Tradeoffs

* The script prioritizes **clarity and explainability** over perfect accuracy
* All classifications are heuristic-based, not authoritative
* The structure is modular and easily extensible

Potential future improvements include:

* Using IMDb title IDs instead of titles for reboot detection
* Incorporating external datasets for adaptation verification
* Exporting results to CSV or database formats

---

## 12. Summary

This script demonstrates a clean, readable data analysis pipeline that:

* Filters and normalizes IMDb data
* Applies interpretable classification rules
* Produces both quantitative and visual insights

It is suitable for exploratory analysis, blog content, or portfolio demonstrations, and is intentionally structured for readability and extension.
