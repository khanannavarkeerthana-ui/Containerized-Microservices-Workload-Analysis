# Detailed Workload Analysis

## 1. Experiment Overview

The objective of this experiment was to evaluate the performance of a containerized microservice application under different concurrent workloads.

The application consists of three services:

* User Service
* Food Service
* Order Service

All services were deployed using Docker Compose and connected through a common Docker bridge network.

The workload was tested at five concurrency levels:

**1, 2, 4, 8, and 16**

Each workload level generated 50 requests.

---

## 2. Workload Results

| Concurrency | Total Requests | Successful | Failed | Average Response Time (ms) | Throughput (req/s) |
| ----------: | -------------: | ---------: | -----: | -------------------------: | -----------------: |
|           1 |             50 |         50 |      0 |                      18.26 |              54.20 |
|           2 |             50 |         50 |      0 |                      22.67 |              86.33 |
|           4 |             50 |         50 |      0 |                      26.35 |             144.39 |
|           8 |             50 |         50 |      0 |                      50.20 |             147.58 |
|          16 |             50 |         50 |      0 |                      87.19 |             160.70 |

A total of **250 requests** were executed.

All **250 requests were successful**, and no request failures were observed during the experiment.

---

## 3. Response Time Analysis

The average response time increased as concurrency increased.

| Concurrency | Average Response Time |
| ----------: | --------------------: |
|           1 |              18.26 ms |
|           2 |              22.67 ms |
|           4 |              26.35 ms |
|           8 |              50.20 ms |
|          16 |              87.19 ms |

At concurrency 1, the average response time was **18.26 ms**.

At concurrency 16, it increased to **87.19 ms**.

Therefore, higher concurrent workload resulted in increased request latency.

The increase was particularly noticeable between concurrency 4 and 8 and again between 8 and 16.

---

## 4. Throughput Analysis

The measured throughput was:

| Concurrency |   Throughput |
| ----------: | -----------: |
|           1 |  54.20 req/s |
|           2 |  86.33 req/s |
|           4 | 144.39 req/s |
|           8 | 147.58 req/s |
|          16 | 160.70 req/s |

Throughput increased as concurrency increased.

The largest increase occurred between concurrency 2 and 4.

Between concurrency 4 and 8, throughput increased only slightly:

**144.39 → 147.58 requests/sec**

During the same interval, response time increased from:

**26.35 → 50.20 ms**

This shows that additional concurrency at this point produced only a small throughput improvement while increasing latency considerably.

---

## 5. CPU Utilization Analysis

The maximum observed CPU values were:

| Concurrency | Order Service | User Service | Food Service |
| ----------: | ------------: | -----------: | -----------: |
|           1 |         0.30% |        8.25% |        8.03% |
|           2 |         0.22% |        6.85% |        0.30% |
|           4 |        20.49% |        6.08% |        0.37% |
|           8 |         0.37% |        0.28% |        5.97% |
|          16 |        20.11% |        5.82% |        0.27% |

The highest observed CPU value was **20.49% for the Order Service at concurrency 4**.

The Order Service performs additional processing because it receives the order request and communicates with both the User Service and Food Service.

The CPU measurements were obtained from periodic Docker statistics samples. Therefore, they represent maximum observed samples rather than continuous CPU averages.

---

## 6. Memory Utilization Analysis

The observed memory values were:

| Service       | Minimum Observed Memory | Maximum Observed Memory |
| ------------- | ----------------------: | ----------------------: |
| Order Service |               39.75 MiB |               41.36 MiB |
| User Service  |               34.04 MiB |               34.11 MiB |
| Food Service  |               34.21 MiB |               34.47 MiB |

Memory consumption remained relatively stable throughout the workload tests.

The Order Service used approximately 40 MiB of memory, while the User Service and Food Service used approximately 34 MiB.

No significant memory growth was observed as concurrency increased.

---

## 7. Failure Analysis

The results show:

* Total requests: **250**
* Successful requests: **250**
* Failed requests: **0**
* Failure rate: **0%**

Therefore, all tested concurrency levels completed without request failures.

The tested workload range did not produce service failures.

---

## 8. Resource-Heavy Service Observation

The Order Service recorded the highest individual CPU peak:

**20.49% at concurrency 4**

It also had the highest memory usage among the three services, reaching:

**41.36 MiB at concurrency 16**

This is consistent with its role as the coordinating service because it communicates with both downstream services during order creation.

However, the CPU measurements are sampled maximum values, so they should not be interpreted as continuous CPU utilization or as proof of a sustained CPU bottleneck.

---

## 9. Performance Degradation

The main performance change observed as concurrency increased was increased response time.

Response time changed from:

**18.26 ms at concurrency 1**

to:

**87.19 ms at concurrency 16**

This represents an increase of approximately **4.8 times**.

Throughput also increased from:

**54.20 requests/sec**

to:

**160.70 requests/sec**

However, throughput growth became smaller at higher concurrency levels while response time continued to increase.

This indicates that increasing concurrency improved the number of requests processed per second, but also introduced additional latency.

---

## 10. Overall Observations

The experiment produced the following observations:

1. All three microservices were successfully deployed using Docker.
2. Docker Compose successfully managed the three-container application.
3. All services communicated through the common Docker bridge network.
4. The Order Service successfully communicated with both downstream services.
5. Increasing concurrency increased throughput.
6. Increasing concurrency also increased average response time.
7. Memory usage remained relatively stable.
8. The Order Service recorded the highest observed CPU peak.
9. No request failures occurred during the tested workloads.
10. At higher concurrency, throughput improvement became smaller compared with the increase in response time.

---

## 11. Conclusion

The workload experiment demonstrates the behavior of a containerized microservice application under increasing concurrent requests.

The application successfully handled all 250 tested requests without failures.

The results show that increasing concurrency can improve throughput, but it also increases response time. At higher concurrency levels, the increase in throughput became smaller while latency increased significantly.

The Order Service recorded the highest observed CPU peak and the highest memory usage because it coordinates requests between the User Service and Food Service.

Overall, the experiment demonstrates how Dockerized microservices can be deployed, connected, monitored, and evaluated under varying workloads.
