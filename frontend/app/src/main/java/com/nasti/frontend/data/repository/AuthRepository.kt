package com.nasti.frontend.data.repository

import com.nasti.frontend.data.api.ApiService
import com.nasti.frontend.data.model.LoginRequest
import com.nasti.frontend.data.model.RegisterRequest
import com.nasti.frontend.data.model.TokenResponse

class AuthRepository(private val api: ApiService) {

    suspend fun login(email: String, password: String): TokenResponse {
        val request = LoginRequest(email = email, password = password)
        val response = api.login(request)
        if (response.isSuccessful && response.body() != null) {
            return response.body()!!
        } else {
            throw Exception("Login failed: ${response.errorBody()?.string() ?: "Unknown error"}")
        }
    }

    suspend fun register(request: RegisterRequest): TokenResponse {
        val response = api.register(request)
        if (response.isSuccessful && response.body() != null) {
            return response.body()!!
        } else {
            throw Exception("Registration failed: ${response.errorBody()?.string() ?: "Unknown error"}")
        }
    }
}
