import csv
import json
import ssl
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    import certifi  # pyright: ignore[reportMissingImports]
except ImportError:  # pragma: no cover - only used if certifi is unavailable
    certifi = None

# Configuration for the ETL pipeline
API_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_CSV = Path("cleaned_users.csv")
OUTPUT_JSON = Path("cleaned_users.json")


def build_ssl_context():
    """Create a secure SSL context using certifi when it is available."""
    context = ssl.create_default_context()
    if certifi is not None:
        context.load_verify_locations(certifi.where())
    return context


def fetch_json_data(api_url: str):
    """Download JSON data from a URL and return it as a Python object."""
    request = Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
    context = build_ssl_context()

    try:
        with urlopen(request, timeout=10, context=context) as response:
            return json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"HTTP error {exc.code} while fetching data") from exc
    except URLError as exc:
        # Some systems raise SSL certificate errors inside URLError.reason.
        if isinstance(exc.reason, ssl.SSLError):
            return fetch_with_unverified_ssl(request)
        raise RuntimeError(f"Network error while fetching data: {exc.reason}") from exc


def fetch_with_unverified_ssl(request: Request):
    """Retry the request with an unverified SSL context as a fallback."""
    fallback_context = ssl._create_unverified_context()

    try:
        with urlopen(request, timeout=10, context=fallback_context) as response:
            return json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"HTTP error {exc.code} while fetching data") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error while fetching data: {exc.reason}") from exc


def extract(api_url: str):
    """Fetch raw data from the API and validate that it is a list."""
    data = fetch_json_data(api_url)

    if not isinstance(data, list):
        raise ValueError("Expected a list of records from the API")

    return data


def clean_record(record):
    """Clean and normalize one API record into a consistent dictionary."""
    if not isinstance(record, dict):
        return {}

    address = record.get("address") or {}
    company = record.get("company") or {}

    cleaned = {
        "id": int(record.get("id", 0) or 0),
        "name": str(record.get("name", "")).strip(),
        "username": str(record.get("username", "")).strip().lower(),
        "email": str(record.get("email", "")).strip().lower(),
        "phone": str(record.get("phone", "")).strip() or "N/A",
        "website": str(record.get("website", "")).strip().lower() or "N/A",
        "street": str(address.get("street", "")).strip() or "N/A",
        "city": str(address.get("city", "")).strip() or "N/A",
        "zipcode": str(address.get("zipcode", "")).strip() or "N/A",
        "company_name": str(company.get("name", "")).strip() or "N/A",
        "catch_phrase": str(company.get("catchPhrase", "")).strip() or "N/A",
    }

    return cleaned


def transform(raw_data):
    """Apply cleaning to all rows and remove any invalid records."""
    cleaned_data = [clean_record(item) for item in raw_data]
    return [item for item in cleaned_data if item]


def load_csv(rows, output_path: Path):
    """Write cleaned rows to a CSV file."""
    if not rows:
        return

    fieldnames = [
        "id",
        "name",
        "username",
        "email",
        "phone",
        "website",
        "street",
        "city",
        "zipcode",
        "company_name",
        "catch_phrase",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_json(rows, output_path: Path):
    """Write cleaned rows to a JSON file."""
    with output_path.open("w", encoding="utf-8") as file_handle:
        json.dump(rows, file_handle, indent=2)


def main():
    """Run the full ETL process: extract, transform, and load."""
    raw_data = extract(API_URL)
    cleaned_data = transform(raw_data)

    # Save the cleaned output to both file formats
    load_csv(cleaned_data, OUTPUT_CSV)
    load_json(cleaned_data, OUTPUT_JSON)

    print(f"Extracted {len(raw_data)} rows from {API_URL}")
    print(f"Saved {len(cleaned_data)} cleaned rows to {OUTPUT_CSV} and {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
