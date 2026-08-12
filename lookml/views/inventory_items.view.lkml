view: inventory_items {
  sql_table_name: `bigquery-public-data.thelook_ecommerce.inventory_items` ;;
  drill_fields: [detail*]

  dimension: id {
    primary_key: yes
    type: number
    sql: ${TABLE}.id ;;
  }
  dimension: cost {
    type: number
    sql: 1.0 * ${TABLE}.cost * ${currency_conversion.conversion_rate} ;;
    value_format_name: decimal_2
    html: @{currency_html} ;;
  }
  dimension_group: created {
    type: time
    timeframes: [raw, time, date, week, month, quarter, year]
    sql: ${TABLE}.created_at ;;
  }
  dimension: product_brand {
    type: string
    sql: ${TABLE}.product_brand ;;
  }
  dimension: product_category {
    type: string
    sql: ${TABLE}.product_category ;;
  }
  dimension: product_department {
    type: string
    sql: ${TABLE}.product_department ;;
  }
  dimension: product_distribution_center_id {
    type: number
    sql: ${TABLE}.product_distribution_center_id ;;
  }
  dimension: product_id {
    type: number
    sql: ${TABLE}.product_id ;;
  }
  dimension: product_name {
    type: string
    sql: ${TABLE}.product_name ;;
  }
  dimension: product_retail_price {
    type: number
    sql: 1.0 * ${TABLE}.product_retail_price * ${currency_conversion.conversion_rate} ;;
    value_format_name: decimal_2
    html: @{currency_html} ;;
  }
  dimension: product_sku {
    type: string
    sql: ${TABLE}.product_sku ;;
  }
  dimension_group: sold {
    type: time
    timeframes: [raw, time, date, week, month, quarter, year]
    sql: ${TABLE}.sold_at ;;
  }
  dimension: is_sold {
    type: yesno
    sql: ${sold_raw} IS NOT NULL ;;
    description: "Whether the inventory item has been sold."
  }
  dimension: days_in_inventory {
    type: number
    sql: TIMESTAMP_DIFF(COALESCE(${sold_raw}, CURRENT_TIMESTAMP()), ${created_raw}, DAY) ;;
    description: "Number of days the item has been in inventory."
  }
  dimension: days_in_inventory_tier {
    type: tier
    tiers: [0, 30, 60, 90, 180, 365]
    style: integer
    sql: ${days_in_inventory} ;;
    description: "Tiered aging of inventory items by days in inventory."
  }
  measure: count {
    type: count
    drill_fields: [detail*]
  }

  set: detail {
    fields: [
      id,
      product_name,
      product_brand,
      product_category,
      cost,
      product_retail_price,
      created_date,
      sold_date
    ]
  }
}
