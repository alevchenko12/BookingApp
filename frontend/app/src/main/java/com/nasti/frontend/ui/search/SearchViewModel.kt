package com.nasti.frontend.ui.search

import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import com.nasti.frontend.data.model.HotelSearchResult

class SearchViewModel : ViewModel() {
    private val _searchResults = MutableStateFlow<List<HotelSearchResult>>(emptyList())
    val searchResults: StateFlow<List<HotelSearchResult>> = _searchResults

    fun setResults(results: List<HotelSearchResult>) {
        _searchResults.value = results
    }
}
