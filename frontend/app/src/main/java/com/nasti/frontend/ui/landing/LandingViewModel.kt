package com.nasti.frontend.ui.landing

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nasti.frontend.data.api.RetrofitClient
import com.nasti.frontend.data.model.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class LandingViewModel : ViewModel() {
    private val _destination = MutableStateFlow("")
    val destination: StateFlow<String> = _destination

    private val _suggestions = MutableStateFlow<List<LocationSuggestion>>(emptyList())
    val suggestions: StateFlow<List<LocationSuggestion>> = _suggestions

    fun updateDestination(query: String) {
        _destination.value = query

        if (query.length < 2) {
            _suggestions.value = emptyList()
            return
        }

        viewModelScope.launch {
            try {
                val response = RetrofitClient.api.searchLocations(query)
                if (response.isSuccessful) {
                    val result = response.body() ?: emptyList()
                    _suggestions.value = result.mapNotNull { item ->
                        when (item["type"]) {
                            "city" -> LocationSuggestion.CityItem(
                                id = (item["id"] as Double).toInt(),
                                name = item["name"] as String,
                                countryName = item["country_name"] as? String
                            )
                            "country" -> LocationSuggestion.CountryItem(
                                id = (item["id"] as Double).toInt(),
                                name = item["name"] as String
                            )
                            else -> null
                        }
                    }
                } else {
                    _suggestions.value = emptyList()
                }
            } catch (e: Exception) {
                _suggestions.value = emptyList()
            }
        }
    }

    fun selectSuggestion(suggestion: LocationSuggestion) {
        _destination.value = when (suggestion) {
            is LocationSuggestion.CityItem -> "${suggestion.name}, ${suggestion.countryName.orEmpty()}"
            is LocationSuggestion.CountryItem -> suggestion.name
        }
    }
}
