package com.example.keynova.data.api

import retrofit2.http.*
import com.example.keynova.data.model.*

interface ApiService {
    @POST("auth/token/login/")
    suspend fun login(@Body request: LoginRequest): TokenResponse

    @GET("users/me/")
    suspend fun getUser(@Header("Authorization") token: String): User
}