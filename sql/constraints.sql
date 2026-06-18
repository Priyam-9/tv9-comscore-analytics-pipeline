ALTER TABLE public.comscore_data
ADD CONSTRAINT uq_comscore_business_key
UNIQUE (
    property_name,
    segments,
    year,
    month_num
);

ALTER TABLE public.comscore_data
ADD CONSTRAINT chk_unique_users_non_negative
CHECK (unique_users >= 0);

ALTER TABLE public.comscore_data
ADD CONSTRAINT chk_valid_month
CHECK (month_num BETWEEN 1 AND 12);

ALTER TABLE public.comscore_data
ADD CONSTRAINT chk_valid_quarter
CHECK (quarter BETWEEN 1 AND 4);