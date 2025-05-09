package com.nasti.frontend.data.model

data class CitySuggestion(
    val id: Int,
    val name: String,
    val country: CountryResponse?
)

data class CountryResponse(
    val id: Int,
    val name: String
)

