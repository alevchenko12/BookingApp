package com.nasti.frontend.ui.hotel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nasti.frontend.data.api.RetrofitClient
import com.nasti.frontend.data.model.HotelDetailResponse
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class HotelDetailViewModel : ViewModel() {

    private val _hotel = MutableStateFlow<HotelDetailResponse?>(null)
    val hotel: StateFlow<HotelDetailResponse?> = _hotel

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error

    fun loadHotel(hotelId: Int) {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null

            try {
                val response = RetrofitClient.api.getHotelDetails(hotelId)
                if (response.isSuccessful) {
                    _hotel.value = response.body()
                } else {
                    _error.value = "Failed to load hotel"
                }
            } catch (e: Exception) {
                _error.value = "Error: ${e.localizedMessage ?: "Unknown error"}"
            } finally {
                _isLoading.value = false
            }
        }
    }
}
