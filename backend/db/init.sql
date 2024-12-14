-- Schema: public.api_keys
CREATE TABLE IF NOT EXISTS public.api_keys (
    id serial PRIMARY KEY,
    api_key text NOT NULL UNIQUE,
    owner text NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP
);
-- Schema: public.api_usage
CREATE TABLE IF NOT EXISTS public.api_usage (
    id serial PRIMARY KEY,
    api_key text NOT NULL,
    endpoint text NOT NULL,
    timestamp timestamp DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT api_usage_api_key_fkey FOREIGN KEY (api_key) REFERENCES public.api_keys(api_key) ON DELETE CASCADE
);