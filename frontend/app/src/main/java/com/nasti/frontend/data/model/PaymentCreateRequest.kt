package com.nasti.frontend.data.model

data class PaymentCreateRequest(
    val booking_id: Int,
    val payment_date: String, // "yyyy-MM-dd"
    val payment_method: String, // "Cash", "Card", "Google Pay"
    val amount: Double
)
