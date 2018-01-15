class CreatePurchasers < ActiveRecord::Migration[5.1]
  def change
    create_table :purchasers do |t|
      t.string :purchaser_name
      t.integer :purchaser_count
      t.string :item_description
      t.decimal :item_price
      t.string :merchant_name
      t.string :merchant_address

      t.timestamps
    end
  end
end
