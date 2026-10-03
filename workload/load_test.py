import requests
import time
import csv
import statistics
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

URL = "http://localhost:8000/orders"

CONCURRENCY_LEVELS = [1, 2, 4, 8, 16]
REQUESTS_PER_LEVEL = 50

CONTAINERS = [
    "order-service",
    "user-service",
    "food-service"
]


def get_docker_stats():

    stats = {}

    try:
        result = subprocess.run(
            [
                "docker",
                "stats",
                "--no-stream",
                "--format",
                "{{.Name}},{{.CPUPerc}},{{.MemUsage}}"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        for line in result.stdout.strip().splitlines():

            parts = line.split(",", 2)

            if len(parts) != 3:
                continue

            name = parts[0]
            cpu = parts[1].replace("%", "").strip()

            memory = parts[2].split("/")[0].strip()

            stats[name] = {
                "cpu": cpu,
                "memory": memory
            }

    except Exception:
        pass

    return stats


def monitor_resources(stop_event, resource_samples):

    while not stop_event.is_set():

        stats = get_docker_stats()

        if stats:
            resource_samples.append(stats)

        time.sleep(0.2)


def send_request():

    start = time.perf_counter()

    try:

        response = requests.post(
            URL,
            params={
                "user_id": 1,
                "food_id": 1
            },
            timeout=10
        )

        end = time.perf_counter()

        return {
            "success": response.status_code == 200,
            "response_time": end - start
        }

    except Exception:

        end = time.perf_counter()

        return {
            "success": False,
            "response_time": end - start
        }


def run_test(concurrency):

    results = []
    resource_samples = []

    stop_event = threading.Event()

    monitor_thread = threading.Thread(
        target=monitor_resources,
        args=(stop_event, resource_samples)
    )

    monitor_thread.start()

    test_start = time.perf_counter()

    with ThreadPoolExecutor(
        max_workers=concurrency
    ) as executor:

        futures = []

        for i in range(REQUESTS_PER_LEVEL):
            futures.append(
                executor.submit(send_request)
            )

        for future in as_completed(futures):
            results.append(future.result())

    test_end = time.perf_counter()

    stop_event.set()
    monitor_thread.join()

    total_time = test_end - test_start

    successful = sum(
        1 for result in results
        if result["success"]
    )

    failed = len(results) - successful

    response_times = [
        result["response_time"]
        for result in results
    ]

    average_response = statistics.mean(
        response_times
    )

    throughput = successful / total_time

    return {
        "concurrency": concurrency,
        "total_requests": len(results),
        "successful_requests": successful,
        "failed_requests": failed,
        "average_response_time_ms":
            average_response * 1000,
        "throughput_requests_per_sec":
            throughput,
        "total_test_time_sec":
            total_time,
        "resource_samples":
            resource_samples
    }


def get_max_resources(samples, container):

    cpu_values = []
    memory_values = []

    for sample in samples:

        if container not in sample:
            continue

        data = sample[container]

        try:
            cpu_values.append(
                float(data["cpu"])
            )
        except ValueError:
            pass

        memory_text = data["memory"]

        try:

            if "MiB" in memory_text:
                memory_values.append(
                    float(
                        memory_text.replace(
                            "MiB", ""
                        ).strip()
                    )
                )

            elif "GiB" in memory_text:
                memory_values.append(
                    float(
                        memory_text.replace(
                            "GiB", ""
                        ).strip()
                    ) * 1024
                )

        except ValueError:
            pass

    max_cpu = max(cpu_values) if cpu_values else 0
    max_memory = (
        max(memory_values)
        if memory_values
        else 0
    )

    return max_cpu, max_memory


def main():

    print("=" * 80)
    print("FOOD ONLINE MICROSERVICES")
    print("WORKLOAD + RESOURCE MONITORING TEST")
    print("=" * 80)

    print(
        f"Requests per workload level: "
        f"{REQUESTS_PER_LEVEL}"
    )

    print()

    results = []

    for concurrency in CONCURRENCY_LEVELS:

        print(
            f"Testing concurrency = "
            f"{concurrency}"
        )

        result = run_test(concurrency)

        samples = result.pop(
            "resource_samples"
        )

        for container in CONTAINERS:

            max_cpu, max_memory = (
                get_max_resources(
                    samples,
                    container
                )
            )

            result[
                f"{container}_max_cpu_percent"
            ] = max_cpu

            result[
                f"{container}_max_memory_mib"
            ] = max_memory

        results.append(result)

        print(
            f"Successful: "
            f"{result['successful_requests']} | "
            f"Failed: "
            f"{result['failed_requests']}"
        )

        print(
            f"Average Response: "
            f"{result['average_response_time_ms']:.2f} ms"
        )

        print(
            f"Throughput: "
            f"{result['throughput_requests_per_sec']:.2f} requests/sec"
        )

        print(
            f"Order CPU: "
            f"{result['order-service_max_cpu_percent']:.2f}% | "
            f"Memory: "
            f"{result['order-service_max_memory_mib']:.2f} MiB"
        )

        print(
            f"User CPU: "
            f"{result['user-service_max_cpu_percent']:.2f}% | "
            f"Memory: "
            f"{result['user-service_max_memory_mib']:.2f} MiB"
        )

        print(
            f"Food CPU: "
            f"{result['food-service_max_cpu_percent']:.2f}% | "
            f"Memory: "
            f"{result['food-service_max_memory_mib']:.2f} MiB"
        )

        print()

        time.sleep(2)

    output_file = (
        "results/raw/"
        "workload_resource_results.csv"
    )

    with open(
        output_file,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )

        writer.writeheader()
        writer.writerows(results)

    print("=" * 80)
    print("TEST COMPLETED")
    print("=" * 80)

    print()
    print("Results saved to:")
    print(output_file)


if __name__ == "__main__":
    main()