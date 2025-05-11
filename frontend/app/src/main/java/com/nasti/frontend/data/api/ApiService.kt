package com.nasti.frontend.data.api

import com.nasti.frontend.data.model.*
import retrofit2.Response
import retrofit2.http.*

interface ApiService {

    // Authentication
    @POST("users/login")
    suspend fun login(
        @Body request: LoginRequest
    ): Response<TokenResponse>

    // Registration
    @POST("users/register")
    suspend fun register(
        @Body request: RegisterRequest
    ): Response<TokenResponse>

    // Get current user's profile
    @GET("users/me")
    suspend fun getProfile(): Response<User>

    // Update profile
    @PUT("users/me")
    suspend fun updateProfile(
        @Body request: UserUpdateRequest
    ): Response<User>

    // Change password
    @PUT("users/me/password")
    suspend fun changePassword(
        @Body request: PasswordChangeRequest
    ): Response<Unit>

    // Delete account
    @DELETE("users/me")
    suspend fun deleteAccount(): Response<Unit>

    // Verify registration
    @GET("users/verify-registration")
    suspend fun verifyEmail(
        @Query("token") token: String
    ): retrofit2.Response<Unit>

    // Register initiating
    @POST("users/register-initiate")
    suspend fun registerInitiate(
        @Body request: RegisterRequest
    ): Response<Unit>

    // Forgot password
    @POST("users/forgot-password")
    suspend fun forgotPassword(
        @Body request: ForgotPasswordRequest
    ): Response<Unit>

    // Verify email code
    @POST("users/verify-code")
    suspend fun verifyCode(
        @Body request: Map<String, String>
    ): Response<Unit>

    // Reset password
    @POST("users/reset-password")
    suspend fun resetPassword(@Body request: ResetPasswordRequest): Response<Unit>

    // Search location
    @GET("locations/search")
    suspend fun searchLocations(@Query("q") query: String): Response<List<Map<String, Any>>>

    @POST("hotels/search-available")
    suspend fun searchAvailableHotels(
        @Body request: HotelSearchRequest
    ): Response<List<HotelSearchResult>>

    @GET("hotels/{hotelId}/details")
    suspend fun getHotelDetails(@Path("hotelId") hotelId: Int): Response<HotelDetailResponse>

}
