package com.nasti.frontend.data.model

data class BookingResponse(
    val id: Int,
    val booking_date: String,
    val check_in_date: String,
    val check_out_date: String,
    val status: String,
    val additional_info: String?
)
