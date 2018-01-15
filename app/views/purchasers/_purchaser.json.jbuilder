json.extract! purchaser, :id, :purchaser_name, :purchaser_count, :item_description, :item_price, :merchant_name, :merchant_address, :created_at, :updated_at
json.url purchaser_url(purchaser, format: :json)
