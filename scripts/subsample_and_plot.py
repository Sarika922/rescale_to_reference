import pandas as pd
import matplotlib.pyplot as plt

reference = pd.read_csv("reference_normalized.txt", sep="\t")
query = pd.read_csv("query_distribution.txt", sep=" ", header=None, names=["FragmentLength", "Frequency", "NormalizedFrequency"])
merged = pd.merge(reference, query, on="FragmentLength", how="outer", suffixes=('_ref', '_query')).fillna(0)
scaling_factors = merged["NormalizedFrequency_ref"] / merged["NormalizedFrequency_query"]
scaling_factors = scaling_factors.fillna(0)
merged["ScaledFrequency_query"] = merged["Frequency_query"] * scaling_factors

plt.figure(figsize=(10, 6))
plt.plot(merged["FragmentLength"], merged["NormalizedFrequency_ref"], label="Reference", color="blue")
plt.plot(merged["FragmentLength"], merged["ScaledFrequency_query"] / merged["ScaledFrequency_query"].max(), label="Scaled Query", color="orange")
plt.xlabel("Fragment Length")
plt.ylabel("Normalized Frequency")
plt.legend()
plt.title("Comparison of Scaled Query and Reference Distributions")
plt.savefig("output/query_subsampled_plot.png")
