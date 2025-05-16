package com.nasti.frontend.ui.mybookings

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nasti.frontend.data.api.RetrofitClient
import com.nasti.frontend.data.model.BookingUiModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class BookingListViewModel : ViewModel() {

    // Full list of bookings
    private val _bookings = MutableStateFlow<List<BookingUiModel>>(emptyList())
    val bookings: StateFlow<List<BookingUiModel>> = _bookings

    // Selected status filter ("all", "pending", etc.)
    private val _selectedStatus = MutableStateFlow("all")
    val selectedStatus: StateFlow<String> = _selectedStatus

    fun setSelectedStatus(status: String) {
        _selectedStatus.value = status
    }

    fun loadBookings(token: String) {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.api.getMyBookings("Bearer $token")
                _bookings.value = response.body() ?: emptyList()
            } catch (e: Exception) {
                _bookings.value = emptyList() // fallback on failure
            }
        }
    }

    fun getFilteredBookings(): List<BookingUiModel> {
        val currentStatus = _selectedStatus.value
        return if (currentStatus == "all") {
            _bookings.value
        } else {
            _bookings.value.filter { it.status.equals(currentStatus, ignoreCase = true) }
        }
    }
}
