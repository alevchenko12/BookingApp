package com.nasti.bookingapp.repository

import com.nasti.bookingapp.api.ApiService
import com.nasti.bookingapp.model.User
import retrofit2.Response

class UserRepository {
    private val apiService = ApiService.create()

    suspend fun fetchUsers(): List<User>? {
        val response: Response<List<User>> = apiService.getUsers()
        return if (response.isSuccessful) response.body() else null
    }
}
