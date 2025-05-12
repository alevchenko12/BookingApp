package com.nasti.frontend.ui.search

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nasti.frontend.data.api.RetrofitClient
import com.nasti.frontend.data.model.HotelSearchRequest
import com.nasti.frontend.data.model.HotelSearchResult
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class SearchViewModel : ViewModel() {

    private val _searchResults = MutableStateFlow<List<HotelSearchResult>>(emptyList())
    val searchResults: StateFlow<List<HotelSearchResult>> = _searchResults

    // Core search context
    var destination: String = ""
    var checkIn: String = ""
    var checkOut: String = ""
    var adults: Int = 2
    var rooms: Int = 1

    // Optional filters
    var minStars: Int? = null
    var hasWifi: Boolean? = null
    var allowsPets: Boolean? = null
    var hasKitchen: Boolean? = null
    var hasAirConditioning: Boolean? = null
    var hasTv: Boolean? = null
    var hasSafe: Boolean? = null
    var hasBalcony: Boolean? = null

    // Sorting
    var sortBy: String? = null // "price_asc", "price_desc", "rating", "reviews"

    fun setResults(results: List<HotelSearchResult>) {
        _searchResults.value = results
    }

    fun setSearchContext(
        destination: String,
        checkIn: String,
        checkOut: String,
        adults: Int,
        rooms: Int
    ) {
        this.destination = destination
        this.checkIn = checkIn
        this.checkOut = checkOut
        this.adults = adults
        this.rooms = rooms
    }

    fun setFiltersAndSorting(
        minStars: Int? = null,
        hasWifi: Boolean? = null,
        allowsPets: Boolean? = null,
        hasKitchen: Boolean? = null,
        hasAirConditioning: Boolean? = null,
        hasTv: Boolean? = null,
        hasSafe: Boolean? = null,
        hasBalcony: Boolean? = null,
        sortBy: String? = null
    ) {
        this.minStars = minStars
        this.hasWifi = hasWifi
        this.allowsPets = allowsPets
        this.hasKitchen = hasKitchen
        this.hasAirConditioning = hasAirConditioning
        this.hasTv = hasTv
        this.hasSafe = hasSafe
        this.hasBalcony = hasBalcony
        this.sortBy = sortBy
    }

    fun buildSearchRequest(): HotelSearchRequest {
        return HotelSearchRequest(
            destination = destination,
            check_in = checkIn,
            check_out = checkOut,
            adults = adults,
            rooms = rooms,
            min_stars = minStars,
            has_wifi = hasWifi,
            allows_pets = allowsPets,
            has_kitchen = hasKitchen,
            has_air_conditioning = hasAirConditioning,
            has_tv = hasTv,
            has_safe = hasSafe,
            has_balcony = hasBalcony,
            sort_by = sortBy
        )
    }

    fun performSearch(onError: (String) -> Unit = {}) {
        viewModelScope.launch {
            try {
                val request = buildSearchRequest()
                val response = RetrofitClient.api.searchAvailableHotels(request)
                if (response.isSuccessful) {
                    setResults(response.body() ?: emptyList())
                } else {
                    onError("Search failed: ${response.code()}")
                }
            } catch (e: Exception) {
                onError("Error: ${e.localizedMessage}")
            }
        }
    }

    fun triggerSearch() {
        val request = buildSearchRequest()
        viewModelScope.launch {
            val response = RetrofitClient.api.searchAvailableHotels(request)
            if (response.isSuccessful) {
                setResults(response.body() ?: emptyList())
            }
        }
    }

}
