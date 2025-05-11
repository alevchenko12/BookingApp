package com.nasti.frontend.ui.search

import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import com.nasti.frontend.data.model.HotelSearchResult

class SearchViewModel : ViewModel() {
    private val _searchResults = MutableStateFlow<List<HotelSearchResult>>(emptyList())
    val searchResults: StateFlow<List<HotelSearchResult>> = _searchResults

    var checkIn: String = ""
    var checkOut: String = ""
    var adults: Int = 2
    var rooms: Int = 1

    fun setResults(results: List<HotelSearchResult>) {
        _searchResults.value = results
    }

    fun setSearchContext(
        checkIn: String,
        checkOut: String,
        adults: Int,
        rooms: Int
    ) {
        this.checkIn = checkIn
        this.checkOut = checkOut
        this.adults = adults
        this.rooms = rooms
    }
}
