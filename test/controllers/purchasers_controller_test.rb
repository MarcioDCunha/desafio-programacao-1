require 'test_helper'

class PurchasersControllerTest < ActionDispatch::IntegrationTest
  setup do
    @purchaser = purchasers(:one)
  end

  test "should get index" do
    get purchasers_url
    assert_response :success
  end

  test "should get new" do
    get new_purchaser_url
    assert_response :success
  end

  test "should create purchaser" do
    assert_difference('Purchaser.count') do
      post purchasers_url, params: { purchaser: { item_description: @purchaser.item_description, item_price: @purchaser.item_price, merchant_address: @purchaser.merchant_address, merchant_name: @purchaser.merchant_name, purchaser_count: @purchaser.purchaser_count, purchaser_name: @purchaser.purchaser_name } }
    end

    assert_redirected_to purchaser_url(Purchaser.last)
  end

  test "should show purchaser" do
    get purchaser_url(@purchaser)
    assert_response :success
  end

  test "should get edit" do
    get edit_purchaser_url(@purchaser)
    assert_response :success
  end

  test "should update purchaser" do
    patch purchaser_url(@purchaser), params: { purchaser: { item_description: @purchaser.item_description, item_price: @purchaser.item_price, merchant_address: @purchaser.merchant_address, merchant_name: @purchaser.merchant_name, purchaser_count: @purchaser.purchaser_count, purchaser_name: @purchaser.purchaser_name } }
    assert_redirected_to purchaser_url(@purchaser)
  end

  test "should destroy purchaser" do
    assert_difference('Purchaser.count', -1) do
      delete purchaser_url(@purchaser)
    end

    assert_redirected_to purchasers_url
  end
end
