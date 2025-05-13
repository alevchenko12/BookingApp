package com.nasti.frontend.data.model

import com.google.gson.annotations.SerializedName

data class BookingUiModel(
    val id: Int,
    @SerializedName("hotel_name") val hotelName: String,
    val address: String,
    val city: String,
    val country: String,
    @SerializedName("check_in") val checkIn: String,
    @SerializedName("check_out") val checkOut: String,
    @SerializedName("booking_date") val bookingDate: String,
    @SerializedName("total_price") val totalPrice: String?,
    val status: String,
    @SerializedName("cancellation_policy") val cancellationPolicy: String?,
    @SerializedName("cover_image_url") val coverImageUrl: String?,
    @SerializedName("latitude") val latitude: Double?,   // optional
    @SerializedName("longitude") val longitude: Double?  // optional
)

