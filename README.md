# Cross Shopper

[![cicd-tools](https://img.shields.io/badge/ci/cd:-cicd_tools-blue)](https://github.com/cicd-tools-org/cicd-tools)

[![Cross Shopper CI/CD](https://github.com/niall-byrne/cross_shopper_backend/actions/workflows/workflow-push.yml/badge.svg?branch=main)](https://github.com/niall-byrne/cross_shopper_backend/actions/workflows/workflow-push.yml)

Cross Shopper is a grocery price data application designed to collect, track, and analyze grocery pricing across different stores.
It was created as a reaction to the ridiculous food inflation Canada has been suffering from since the onset of Covid 19.

It enables per-store item price tracking and trend analysis to help make informed pricing decisions.

It is NOT a web scraper, but more a data repository for pricing data collected from web scrapers.

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
- `DJANGO_GOOGLE_MAPS_API_KEY`:  An API key for Google Maps.

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

## Workflow

The django admin is used to create stores, reports, scrapers and items.

For a specific geographic area a report would be created, containing stores (instances of franchises), which carry various items.

Each item would then be associated with one or more scraper configurations.  These configurations contain the paths to the item's pricing on each franchise's website.  

Pricing in Canada tends to change on Thursdays.  Each Thursday the scrapers would be run to record prices and reports would be generated.

Advertised pricing varies widely in Canada based on region, so stores from the same franchise all need to be scraped individually to ensure accurate pricing.

One more important consideration: most of the stores in Canada are consolidated into just a handful of companies.  Studying the actual web content itself reveals this quite evidently.  A handful of well built web scrapers can cover 90% of the large grocery stores out there.

### Recording Data

- read report definitions from `/api/v1/reports/` to identify the items and target urls
- scrape each item's price and post it to `/api/v1/pricing/`
- in the event of a scraping error post it to `/api/v1/errors/`

### Generating Reports

- read a list of report targets from `/api/v1/reports/targets/`
- generate a report summary from `/api/v1/reports/summaries/`

Heat maps have been found to be a great way to visualize the "best deals" of a given week for a specific geographic area.
