package com.nasti.frontend.ui.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nasti.frontend.data.api.RetrofitClient
import kotlinx.coroutines.launch
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.State
import com.nasti.frontend.data.model.ForgotPasswordRequest
import retrofit2.HttpException

class ForgotPasswordViewModel : ViewModel() {

    private val _email = mutableStateOf("")
    val email: State<String> = _email

    private val _successMessage = mutableStateOf<String?>(null)
    val successMessage: State<String?> = _successMessage

    private val _errorMessage = mutableStateOf<String?>(null)
    val errorMessage: State<String?> = _errorMessage

    fun updateEmail(newEmail: String) {
        _email.value = newEmail
    }

    fun sendResetCode() {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.api.forgotPassword(ForgotPasswordRequest(email.value))
                if (response.isSuccessful) {
                    _successMessage.value = "Reset code sent to your email."
                    _errorMessage.value = null
                } else {
                    _errorMessage.value = "Failed to send reset code."
                    _successMessage.value = null
                }
            } catch (e: HttpException) {
                _errorMessage.value = "Server error: ${e.code()}"
                _successMessage.value = null
            } catch (e: Exception) {
                _errorMessage.value = "Network error: ${e.localizedMessage}"
                _successMessage.value = null
            }
        }
    }
}
