package com.nasti.frontend.data.model

import com.google.gson.annotations.SerializedName

data class ReviewCreateRequest(
    @SerializedName("booking_id")
    val bookingId: Int,
    val rating: Int,
    val text: String? = null
)
