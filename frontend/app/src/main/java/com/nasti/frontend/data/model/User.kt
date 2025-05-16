package com.nasti.frontend.data.model

data class User(
    val id: Int,
    val first_name: String,
    val last_name: String,
    val email: String,
    val phone: String? = null
)
