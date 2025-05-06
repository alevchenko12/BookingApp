package com.nasti.frontend.data.model

data class RegisterRequest(
    val first_name: String,
    val last_name: String,
    val email: String,
    val phone: String? = null,
    val password: String
)
