package com.nasti.frontend.ui.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.State
import com.nasti.frontend.data.model.LoginRequest
import com.nasti.frontend.data.model.TokenResponse
import com.nasti.frontend.data.repository.AuthRepository
import kotlinx.coroutines.launch

class LoginViewModel(private val repository: AuthRepository) : ViewModel() {

    private val _loginState = mutableStateOf<Result<TokenResponse>?>(null)
    val loginState: State<Result<TokenResponse>?> = _loginState

    fun login(email: String, password: String) {
        viewModelScope.launch {
            try {
                val result = repository.login(email, password)
                _loginState.value = Result.success(result)
            } catch (e: Exception) {
                _loginState.value = Result.failure(e)
            }
        }
    }
}
