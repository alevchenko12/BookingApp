package com.nasti.frontend.data.model

data class HotelSearchResult(
    val id: Int,
    val name: String,
    val address: String,
    val city: String,
    val country: String,
    val stars: Int?,
    val lowest_price: Double?,
    val cover_image_url: String?,
    val available_room_ids: List<Int>,

    // New fields to support filtering and sorting
    val review_count: Int = 0,
    val average_rating: Double? = null
)
