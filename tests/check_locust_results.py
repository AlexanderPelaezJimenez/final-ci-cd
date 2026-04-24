"""Parse Locust CSV output and fail if any threshold is breached."""

import csv
import sys

P95_LIMIT_MS = 500
ERROR_RATE_LIMIT = 0.01


def check_results(csv_path: str) -> bool:
    failed = False

    with open(csv_path) as f:
        for row in csv.DictReader(f):
            if row["Name"] == "Aggregated":
                continue

            name = f"{row['Type']} {row['Name']}"
            p95 = float(row["95%"])
            requests = int(row["Request Count"])
            failures = int(row["Failure Count"])
            error_rate = failures / requests if requests else 0

            p95_status = "FAIL" if p95 > P95_LIMIT_MS else "PASS"
            err_status = "FAIL" if error_rate > ERROR_RATE_LIMIT else "PASS"

            print(f"\n{name}")
            print(f"  p95: {p95:.0f}ms  (limit: {P95_LIMIT_MS}ms)  {p95_status}")
            print(
                f"  error rate: {error_rate*100:.2f}%"
                f"  (limit: {ERROR_RATE_LIMIT*100:.0f}%)  {err_status}"
            )

            if p95 > P95_LIMIT_MS:
                print(f"  => exceeded by {p95 - P95_LIMIT_MS:.0f}ms")
                failed = True
            if error_rate > ERROR_RATE_LIMIT:
                print(f"  => exceeded by {(error_rate - ERROR_RATE_LIMIT)*100:.2f}pp")
                failed = True

    return failed


if __name__ == "__main__":
    sys.exit(1 if check_results("locust-report_stats.csv") else 0)
