package com.nasti.frontend.data.api

import okhttp3.Interceptor
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory


object RetrofitClient {
    private const val BASE_URL = "http://192.168.1.104:8000/"

    // Default client (used for login/register)
    private val retrofit: Retrofit by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    val api: ApiService by lazy {
        retrofit.create(ApiService::class.java)
    }

    // Authenticated client (used after login)
    fun createWithAuth(token: String): ApiService {
        val client = OkHttpClient.Builder()
            .addInterceptor(Interceptor { chain ->
                val newRequest = chain.request().newBuilder()
                    .addHeader("Authorization", "Bearer $token")
                    .build()
                chain.proceed(newRequest)
            })
            .build()

        return Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }

    object RetrofitClient {
        private const val BASE_URL = "http://192.168.1.104:8000/"

        private val retrofit: Retrofit by lazy {
            Retrofit.Builder()
                .baseUrl(BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build()
        }

        val api: ApiService by lazy {
            retrofit.create(ApiService::class.java)
        }
    }

}
