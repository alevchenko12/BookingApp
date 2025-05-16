package com.nasti.frontend.data.model

data class PasswordChangeRequest(
    val old_password: String,
    val new_password: String
)
