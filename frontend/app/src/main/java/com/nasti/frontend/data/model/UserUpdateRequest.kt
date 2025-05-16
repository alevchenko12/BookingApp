package com.nasti.frontend.data.model

data class UserUpdateRequest(
    val first_name: String? = null,
    val last_name: String? = null,
    val phone: String? = null
)
