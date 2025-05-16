package com.nasti.frontend.data.model

data class ResetPasswordRequest(
    val email: String,
    val new_password: String
)
