package com.nasti.frontend.ui.landing

import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

class LandingViewModel : ViewModel() {
    private val _destination = MutableStateFlow("")
    val destination: StateFlow<String> = _destination

    fun updateDestination(value: String) {
        _destination.value = value
    }

    // TODO: Add state for dates and guests
}
