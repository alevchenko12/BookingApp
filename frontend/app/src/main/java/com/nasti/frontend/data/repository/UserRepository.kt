package com.nasti.frontend.data.repository

import com.nasti.frontend.data.api.ApiService
import com.nasti.frontend.data.model.*

class UserRepository(private val api: ApiService) {

    suspend fun getProfile(): User {
        val response = api.getProfile()
        if (response.isSuccessful && response.body() != null) {
            return response.body()!!
        } else {
            throw Exception("Failed to fetch profile: ${response.errorBody()?.string() ?: "Unknown error"}")
        }
    }

    suspend fun updateProfile(updateRequest: UserUpdateRequest): User {
        val response = api.updateProfile(updateRequest)
        if (response.isSuccessful && response.body() != null) {
            return response.body()!!
        } else {
            throw Exception("Update failed: ${response.errorBody()?.string() ?: "Unknown error"}")
        }
    }

    suspend fun changePassword(request: PasswordChangeRequest): Boolean {
        val response = api.changePassword(request)
        if (response.isSuccessful) {
            return true
        } else {
            throw Exception("Password change failed: ${response.errorBody()?.string() ?: "Unknown error"}")
        }
    }

    suspend fun deleteAccount(): Boolean {
        val response = api.deleteAccount()
        if (response.isSuccessful) {
            return true
        } else {
            throw Exception("Account deletion failed: ${response.errorBody()?.string() ?: "Unknown error"}")
        }
    }
}
