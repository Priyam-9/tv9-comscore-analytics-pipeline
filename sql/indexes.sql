CREATE INDEX idx_property_name
ON public.comscore_data(property_name);

CREATE INDEX idx_parent_network
ON public.comscore_data(parent_network);

CREATE INDEX idx_segments
ON public.comscore_data(segments);

CREATE INDEX idx_report_month
ON public.comscore_data(report_month);

CREATE INDEX idx_year_month
ON public.comscore_data(year, month_num);