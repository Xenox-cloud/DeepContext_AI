"""
Evaluation Visualization
"""

from pathlib import Path
import matplotlib.pyplot as plt
import os
import matplotlib

matplotlib.use("Agg")


print(
    "Current working directory:",
    os.getcwd()
)

OUTPUT_DIR = Path(
    "app/evaluation/charts"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

queries = [
    "Self-Attention",
    "Positional Encoding",
    "Transformers",
]

recalls = [
    1.0,
    1.0,
    0.33,
]

relevances = [
    1.0,
    1.0,
    1.0,
]

latencies = [
    4.15,
    2.91,
    1.63,
]


# Recall Chart
plt.figure(
    figsize=(8, 5)
)

plt.bar(
    queries,
    recalls,
)

plt.ylim(
    0,
    1.1,
)

plt.title(
    "RAG Recall Scores"
)

plt.ylabel(
    "Recall"
)

plt.xlabel(
    "Queries"
)

plt.tight_layout()

recall_path = (
    OUTPUT_DIR
    /
    "recall_chart.png"
)

plt.savefig(
    recall_path
)

plt.close()


# Relevance Chart
plt.figure(
    figsize=(8, 5)
)

plt.bar(
    queries,
    relevances,
)

plt.ylim(
    0,
    1.1,
)

plt.title(
    "RAG Context Relevance"
)

plt.ylabel(
    "Relevance"
)

plt.xlabel(
    "Queries"
)

plt.tight_layout()

relevance_path = (
    OUTPUT_DIR
    /
    "relevance_chart.png"
)

plt.savefig(
    relevance_path
)

plt.close()


# Latency Chart
plt.figure(
    figsize=(8, 5)
)

plt.bar(
    queries,
    latencies,
)

plt.title(
    "RAG Latency"
)

plt.ylabel(
    "Seconds"
)

plt.xlabel(
    "Queries"
)

plt.tight_layout()

latency_path = (
    OUTPUT_DIR
    /
    "latency_chart.png"
)

plt.savefig(
    latency_path
)

plt.close()

print(
    "\nCharts generated successfully.\n"
)

print(
    f"Recall chart: {recall_path}"
)

print(
    f"Relevance chart: {relevance_path}"
)

print(
    f"Latency chart: {latency_path}"
)
print(
    "Files inside charts directory:"
)

charts_dir = Path(
    "app/evaluation/charts"
)

if charts_dir.exists():

    for file in charts_dir.iterdir():

        print(file)
else:

    print(
        "Charts directory does not exist."
    )