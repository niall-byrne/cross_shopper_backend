/**
 * TypeScript interface for the Report Summary API response.
 */

export interface ReportSummaryStore {
  id: number;
  franchise_name: string;
}

export interface HistoricalPriceSummary {
  average: string | null;
  high: string | null;
  low: string | null;
}

export interface CurrentPriceSummary {
  average: string | null;
  best: string | null;
  per_store: Record<string, string | null>;
}

export interface ItemPriceSummary {
  last_52_weeks: HistoricalPriceSummary;
  selected_week: CurrentPriceSummary;
}

export interface PackagingSummary {
  quantity: string | null;
  unit: string;
  container: string | null;
}

export interface ReportSummaryItem {
  id: number;
  name: string;
  brand: string;
  is_bulk: boolean;
  is_organic: boolean;
  is_non_gmo: boolean;
  packaging: PackagingSummary;
  prices: ItemPriceSummary;
}

export interface ReportSummary {
  id: number;
  name: string;
  year: string;
  week: string;
  generated_at: string;
  stores: ReportSummaryStore[];
  items: ReportSummaryItem[];
}
