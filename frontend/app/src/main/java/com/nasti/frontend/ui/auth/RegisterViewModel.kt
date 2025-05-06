package com.nasti.frontend.ui.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.State
import com.nasti.frontend.data.repository.AuthRepository
import com.nasti.frontend.data.model.RegisterRequest
import com.nasti.frontend.data.model.TokenResponse

class RegisterViewModel(private val repository: AuthRepository) : ViewModel() {

    private val _registerState = mutableStateOf<Result<TokenResponse>?>(null)
    val registerState: State<Result<TokenResponse>?> = _registerState

    fun register(request: RegisterRequest) {
        viewModelScope.launch {
            try {
                val result = repository.register(request)
                _registerState.value = Result.success(result)
            } catch (e: Exception) {
                _registerState.value = Result.failure(e)
            }
        }
    }
}
