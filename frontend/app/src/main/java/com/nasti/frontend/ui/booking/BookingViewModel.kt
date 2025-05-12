package com.nasti.frontend.ui.booking

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nasti.frontend.data.api.RetrofitClient
import com.nasti.frontend.data.model.BookingCreateRequest
import com.nasti.frontend.data.model.BookingResponse
import com.nasti.frontend.utils.SessionManager
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*

class BookingViewModel : ViewModel() {

    private val _bookingResult = MutableStateFlow<BookingResponse?>(null)
    val bookingResult: StateFlow<BookingResponse?> = _bookingResult

    private val _loading = MutableStateFlow(false)
    val loading: StateFlow<Boolean> = _loading

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error

    // Form data
    var roomId: Int = -1
    var checkIn: String = ""
    var checkOut: String = ""
    var additionalInfo: String = ""

    fun initialize(
        roomId: Int,
        checkIn: String,
        checkOut: String
    ) {
        this.roomId = roomId
        this.checkIn = checkIn
        this.checkOut = checkOut
    }

    fun submitBooking(token: String) {
        _loading.value = true
        _error.value = null

        val bookingDate = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date())

        val request = BookingCreateRequest(
            room_id = roomId,
            booking_date = bookingDate,
            check_in_date = checkIn,
            check_out_date = checkOut,
            additional_info = additionalInfo.ifBlank { null }
        )

        viewModelScope.launch {
            try {
                val response = RetrofitClient.api.createBooking("Bearer $token", request)
                if (response.isSuccessful) {
                    _bookingResult.value = response.body()
                } else {
                    _error.value = "Booking failed: ${response.code()}"
                }
            } catch (e: Exception) {
                _error.value = "Error: ${e.localizedMessage}"
            } finally {
                _loading.value = false
            }
        }
    }

    fun clearState() {
        _bookingResult.value = null
        _error.value = null
        _loading.value = false
    }
}
