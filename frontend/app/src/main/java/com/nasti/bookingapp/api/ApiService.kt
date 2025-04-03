package com.nasti.bookingapp.api

import com.nasti.bookingapp.model.User
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET

interface ApiService {
    @GET("/users")  // Matches FastAPI endpoint
    suspend fun getUsers(): Response<List<User>>

    companion object {
        private const val BASE_URL = "http://10.0.2.2:8000/"

        fun create(): ApiService {
            val retrofit = Retrofit.Builder()
                .baseUrl(BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())  // Converts JSON to Kotlin objects
                .build()

            return retrofit.create(ApiService::class.java)
        }
    }
}
