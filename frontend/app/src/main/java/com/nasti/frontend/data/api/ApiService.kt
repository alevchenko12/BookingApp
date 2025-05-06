package com.nasti.frontend.data.api

import com.nasti.frontend.data.model.*
import retrofit2.Response
import retrofit2.http.*

interface ApiService {

    @POST("users/login")
    suspend fun login(
        @Body request: LoginRequest
    ): Response<TokenResponse>

    @POST("users/register")
    suspend fun register(
        @Body request: RegisterRequest
    ): Response<TokenResponse>
}