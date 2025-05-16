package com.nasti.frontend.data.model

data class TokenResponse(
    val access_token: String,
    val token_type: String,
    val user: User
)
