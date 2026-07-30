"""
features.py — feature extraction for the malicious URL classifier.

One place that turns raw URLs into model-ready features, so the SAME
transformation is applied to train, test, and any future prediction.
That consistency is the whole point of a module: hand-writing features
separately in each notebook is how train/test drift apart and leakage
sneaks in.

Only the four features that survived exploratory analysis live here.
Rejected features (digit_count, digit_ratio, has_https) stay documented
in 01_eda.ipynb — this file is production logic, not exploration.
"""

import tldextract

# The feature set, defined in ONE place. Downstream code does
# X = df[FEATURE_COLUMNS] so the model always sees exactly these,
# in this order — no accidental inclusion of 'url', 'type', or 'label'.
FEATURE_COLUMNS = ["url_length", "has_at", "has_ip", "subdomain_count"]


def subdomain_count(url):
    """Count subdomain labels in a URL.

    tldextract parses the URL against the public-suffix list, so path
    dots and multi-part suffixes (.co.uk) don't corrupt the count.
    The empty-string guard matters: "".split(".") returns [''] with
    length 1, so a bare domain would wrongly count as 1 without it.
    """
    subdomain = tldextract.extract(url).subdomain
    if subdomain == "":
        return 0
    return len(subdomain.split("."))


def extract_features(df):
    """Return a copy of df with the four feature columns added.

    Takes a DataFrame with a 'url' column; returns a new DataFrame so the
    caller's data is never mutated in place (keeps this function pure —
    same input, same output, no side effects).
    """
    df = df.copy()  # DESIGN DECISION 1: copy so we never mutate the caller's df

    df["url_length"] = df["url"].str.len()
    df["has_at"] = df["url"].str.contains("@")
    df["has_ip"] = df["url"].str.contains(r"(?:\d{1,3}\.){3}\d{1,3}")
    df["subdomain_count"] = df["url"].apply(subdomain_count)

    # DESIGN DECISION 2: return the whole augmented df (flexible) rather
    # than just the feature matrix. Downstream selects X = df[FEATURE_COLUMNS].
    return df