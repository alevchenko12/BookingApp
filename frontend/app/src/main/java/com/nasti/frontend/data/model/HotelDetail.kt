package com.nasti.frontend.data.model

data class HotelDetailResponse(
    val id: Int,
    val name: String,
    val address: String,
    val description: String?,
    val stars: Int?,
    val city: String,
    val country: String,
    val latitude: Double?,
    val longitude: Double?,
    val photos: List<String>,
    val rooms: List<RoomDetail>,
    val reviews: List<ReviewDetail>
)

data class RoomDetail(
    val id: Int,
    val name: String,
    val room_type: String,
    val price_per_night: Double,
    val capacity: Int,
    val description: String?,
    val cancellation_policy: String?,
    val has_wifi: Boolean,
    val allows_pets: Boolean,
    val has_air_conditioning: Boolean,
    val has_tv: Boolean,
    val has_minibar: Boolean,
    val has_balcony: Boolean,
    val has_kitchen: Boolean,
    val has_safe: Boolean
)

data class ReviewDetail(
    val id: Int,
    val rating: Int,
    val text: String?,
    val user_name: String?
)
