package com.nasti.frontend.data.model

data class BookingCreateRequest(
    val room_id: Int,
    val booking_date: String,     // Format: "yyyy-MM-dd"
    val check_in_date: String,
    val check_out_date: String,
    val status: String = "pending", // Defaulted on backend, still useful for consistency
    val additional_info: String? = null
)
