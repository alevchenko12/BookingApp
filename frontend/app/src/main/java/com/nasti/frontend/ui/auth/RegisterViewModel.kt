package com.nasti.frontend.ui.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.State
import com.nasti.frontend.data.repository.AuthRepository
import com.nasti.frontend.data.model.RegisterRequest
import com.nasti.frontend.data.model.TokenResponse
import retrofit2.Response

class RegisterViewModel(private val repository: AuthRepository) : ViewModel() {

    private val _verificationMessage = mutableStateOf<String?>(null)
    val verificationMessage: State<String?> = _verificationMessage

    private val _errorMessage = mutableStateOf<String?>(null)
    val errorMessage: State<String?> = _errorMessage

    private val _registerState = mutableStateOf<Result<TokenResponse>?>(null)
    val registerState: State<Result<TokenResponse>?> = _registerState

    fun register(request: RegisterRequest) {
        viewModelScope.launch {
            try {
                val result = repository.register(request)
                _registerState.value = Result.success(result)
                _errorMessage.value = null
            } catch (e: Exception) {
                _registerState.value = null
                _errorMessage.value = when {
                    e.message?.contains("already registered", true) == true ->
                        "Email already in use"
                    else -> "Registration failed. Please try again."
                }
            }
        }
    }

    fun registerInitiate(request: RegisterRequest) {
        viewModelScope.launch {
            try {
                val response: Response<Unit> = repository.registerInitiate(request)
                if (response.isSuccessful) {
                    _verificationMessage.value = "✅ Verification email sent. Please check your inbox."
                    _errorMessage.value = null
                } else {
                    _verificationMessage.value = null
                    _errorMessage.value = "Registration failed. Please try again."
                }
            } catch (e: Exception) {
                _verificationMessage.value = null
                _errorMessage.value = e.message ?: "Unexpected error occurred."
            }
        }
    }
}
