package com.nasti.frontend.ui.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.State
import com.nasti.frontend.data.repository.AuthRepository
import com.nasti.frontend.data.model.TokenResponse

class LoginViewModel(private val repository: AuthRepository) : ViewModel() {

    private val _loginState = mutableStateOf<Result<TokenResponse>?>(null)
    val loginState: State<Result<TokenResponse>?> = _loginState

    private val _errorMessage = mutableStateOf<String?>(null)
    val errorMessage: State<String?> = _errorMessage

    fun login(email: String, password: String) {
        viewModelScope.launch {
            try {
                val result = repository.login(email, password)
                _loginState.value = Result.success(result)
                _errorMessage.value = null
            } catch (e: Exception) {
                _loginState.value = null
                _errorMessage.value = when {
                    e.message?.contains("Invalid credentials", true) == true ->
                        "Invalid email or password"
                    else -> "Login failed. Please try again."
                }
            }
        }
    }
}
