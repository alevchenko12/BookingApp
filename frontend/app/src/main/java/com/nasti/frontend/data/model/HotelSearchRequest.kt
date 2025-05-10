package com.nasti.frontend.data.model

data class HotelSearchRequest(
    val destination: String,
    val check_in: String,
    val check_out: String,
    val rooms: Int,
    val adults: Int
)
