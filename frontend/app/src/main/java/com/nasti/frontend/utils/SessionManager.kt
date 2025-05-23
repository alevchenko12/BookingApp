package com.nasti.frontend.utils

import android.content.Context
import android.content.SharedPreferences
import android.util.Base64
import org.json.JSONObject

class SessionManager(context: Context) {

    private val prefs: SharedPreferences =
        context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE)

    companion object {
        private const val PREF_NAME = "booking_app_session"
        private const val KEY_ACCESS_TOKEN = "access_token"
    }

    fun saveToken(token: String) {
        prefs.edit().putString(KEY_ACCESS_TOKEN, token).apply()
    }

    fun getToken(): String? {
        return prefs.getString(KEY_ACCESS_TOKEN, null)
    }

    fun clearSession() {
        prefs.edit().clear().apply()
    }

    fun isLoggedIn(): Boolean {
        val token = getToken() ?: return false
        return !isTokenExpired(token)
    }

    fun isTokenExpired(): Boolean {
        val token = getToken() ?: return true
        return isTokenExpired(token)
    }

    private fun isTokenExpired(token: String): Boolean {
        return try {
            val parts = token.split(".")
            if (parts.size != 3) return true

            val payload = String(Base64.decode(parts[1], Base64.URL_SAFE))
            val json = JSONObject(payload)

            val exp = json.optLong("exp", 0L)
            val currentTimeSec = System.currentTimeMillis() / 1000

            exp < currentTimeSec
        } catch (e: Exception) {
            true
        }
    }

    // Optional: Extract user ID from JWT if needed later
    fun getUserIdFromToken(): Int? {
        return try {
            val token = getToken() ?: return null
            val parts = token.split(".")
            if (parts.size != 3) return null

            val payload = String(Base64.decode(parts[1], Base64.URL_SAFE))
            val json = JSONObject(payload)

            json.optInt("sub", -1).takeIf { it >= 0 }
        } catch (e: Exception) {
            null
        }
    }
}
