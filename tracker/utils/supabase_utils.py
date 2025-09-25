from supabase import create_client, Client
from utils.env_utils import get_env_var

supabaseUrl: str = get_env_var("SUPABASE_URL")
supabaseKey: str = get_env_var("SUPABASE_KEY")
supabaseClient: Client = create_client(supabaseUrl, supabaseKey)

def insert_product(product_id, title, url):
    # Upsert product into 'products' table
    data = {
        "id": product_id,
        "title": title,
        "url": url
    }
    supabaseClient.table("products").upsert(data).execute()

def log_price(product_id, price, in_stock):
    # Insert price log into 'prices' table
    data = {
        "product_id": product_id,
        "price": price,
        "in_stock": in_stock
    }
    supabaseClient.table("prices").insert(data).execute()

# SQL CREATE TABLE statements for reference:

# -- Products table
# CREATE TABLE products (
#     id TEXT PRIMARY KEY,
#     title TEXT,
#     url TEXT
# ); 

# -- Prices table
# CREATE TABLE prices (
#     id BIGSERIAL PRIMARY KEY,
#     product_id TEXT REFERENCES products(id),
#     price INTEGER,
#     in_stock BOOLEAN,
#     checked_at TIMESTAMP DEFAULT NOW()
# );

# -- Allow all inserts
# CREATE POLICY "Allow all inserts" ON products
# FOR INSERT USING (true);

# -- Allow all updates
# CREATE POLICY "Allow all updates" ON products
# FOR UPDATE USING (true);
