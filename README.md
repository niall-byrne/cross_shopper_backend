# Cross Shopper

Cross Shopper is a grocery price data application designed to collect, track, and analyze grocery pricing across different stores and franchises. It enables users to compare per-store item pricing and monitor trends over time, helping to make informed pricing decisions.

## Features

- **Price Collection:** Aggregates pricing data from various web scrapers.
- **Trend Tracking:** Monitors grocery price fluctuations and historical data.
- **Reporting:** Generates detailed reports and summaries comparing item prices across different locations.
- **REST API:** Provides a robust API for programmatic access to pricing data and reports.

## Architecture

The project is built with Django and Django Rest Framework, organized into several specialized applications:

- **`items`**: Manages the catalog of grocery items, including brands, attributes, and packaging details.
- **`stores`**: Handles store locations, franchises, and geographic information.
- **`pricing`**: Records specific price points for items at various stores, including metadata like bulk pricing and dates.
- **`scrapers`**: Manages configurations and logs for web scrapers that collect pricing data.
- **`reports`**: Orchestrates the generation of pricing comparisons and summaries.
- **`api`**: Exposes the core functionality through a RESTful interface.
- **`utilities`**: Contains shared components, base classes, and helper functions used throughout the project.

## Getting Started

### Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/) for dependency management.

### Installation

1. Clone the repository.
2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

### Configuration

Create a `.env` file in the root directory or set the following environment variables:

- `DJANGO_SECRET_KEY`: A secure key for your Django installation.
- `DJANGO_SETTINGS_MODULE`: Set to `config.development` for local work.

### Database Setup

Run the migrations to initialize the SQLite database:

```bash
make dj-migrate
```

### Running the Application

Start the development server:

```bash
make dev
```

The application will be accessible at `http://localhost:8000`. You can access the Django Admin at `http://localhost:8000/admin/` and the API at `http://localhost:8000/api/v1/`.

## Development

The project includes a `Makefile` to streamline common development tasks:

- **Formatting:** `make fmt` (uses ruff and yapf)
- **Linting:** `make lint-python`
- **Type Checking:** `make types-python`
- **Testing:** `make test-python`
- **Coverage:** `make coverage`

For detailed information on coding standards and contribution guidelines, please refer to [CONTRIBUTING.md](CONTRIBUTING.md).
