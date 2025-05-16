package com.nasti.frontend.data.model

data class HotelSearchRequest(
    val destination: String,
    val check_in: String,
    val check_out: String,
    val rooms: Int,
    val adults: Int,

    // Optional filters
    val min_stars: Int? = null,
    val has_wifi: Boolean? = null,
    val allows_pets: Boolean? = null,
    val has_kitchen: Boolean? = null,
    val has_air_conditioning: Boolean? = null,
    val has_tv: Boolean? = null,
    val has_safe: Boolean? = null,
    val has_balcony: Boolean? = null,

    // Optional room type filter
    val room_type: String? = null, // e.g., "Single", "Double", "Suite"

    // Optional sorting
    val sort_by: String? = null // "price_asc", "price_desc", "rating", "reviews"
)
