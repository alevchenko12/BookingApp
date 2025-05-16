package com.nasti.frontend.data.model

sealed class LocationSuggestion {
    data class CityItem(
        val id: Int,
        val name: String,
        val countryName: String?
    ) : LocationSuggestion()

    data class CountryItem(
        val id: Int,
        val name: String
    ) : LocationSuggestion()
}
