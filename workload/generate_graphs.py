import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# File locations
input_file = Path("results/raw/workload_resource_results.csv")
output_dir = Path("results/figures")

output_dir.mkdir(parents=True, exist_ok=True)


# Read experimental results
df = pd.read_csv(input_file)


# --------------------------------------------------
# 1. Concurrent Requests vs Average Response Time
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    df["concurrency"],
    df["average_response_time_ms"],
    marker="o"
)

plt.xlabel("Concurrent Requests")
plt.ylabel("Average Response Time (ms)")
plt.title("Concurrent Requests vs Average Response Time")
plt.grid(True)

plt.savefig(
    output_dir / "concurrency_vs_response_time.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# --------------------------------------------------
# 2. Concurrent Requests vs Throughput
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    df["concurrency"],
    df["throughput_requests_per_sec"],
    marker="o"
)

plt.xlabel("Concurrent Requests")
plt.ylabel("Throughput (Requests/sec)")
plt.title("Concurrent Requests vs Throughput")
plt.grid(True)

plt.savefig(
    output_dir / "concurrency_vs_throughput.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# --------------------------------------------------
# 3. Concurrent Requests vs CPU Usage
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    df["concurrency"],
    df["order-service_max_cpu_percent"],
    marker="o",
    label="Order Service"
)

plt.plot(
    df["concurrency"],
    df["user-service_max_cpu_percent"],
    marker="o",
    label="User Service"
)

plt.plot(
    df["concurrency"],
    df["food-service_max_cpu_percent"],
    marker="o",
    label="Food Service"
)

plt.xlabel("Concurrent Requests")
plt.ylabel("Maximum Observed CPU Usage (%)")
plt.title("Concurrent Requests vs CPU Usage")
plt.legend()
plt.grid(True)

plt.savefig(
    output_dir / "concurrency_vs_cpu.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# --------------------------------------------------
# 4. Concurrent Requests vs Memory Usage
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    df["concurrency"],
    df["order-service_max_memory_mib"],
    marker="o",
    label="Order Service"
)

plt.plot(
    df["concurrency"],
    df["user-service_max_memory_mib"],
    marker="o",
    label="User Service"
)

plt.plot(
    df["concurrency"],
    df["food-service_max_memory_mib"],
    marker="o",
    label="Food Service"
)

plt.xlabel("Concurrent Requests")
plt.ylabel("Maximum Observed Memory (MiB)")
plt.title("Concurrent Requests vs Memory Usage")
plt.legend()
plt.grid(True)

plt.savefig(
    output_dir / "concurrency_vs_memory.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("=" * 60)
print("GRAPH GENERATION COMPLETED")
print("=" * 60)

print()
print("Graphs saved in:")
print(output_dir)

print()
for file in sorted(output_dir.glob("*.png")):
    print(file)