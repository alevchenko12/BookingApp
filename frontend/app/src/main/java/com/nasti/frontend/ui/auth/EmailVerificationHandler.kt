package com.nasti.frontend.ui.auth

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.nasti.frontend.data.api.RetrofitClient
import kotlinx.coroutines.launch

@Composable
fun EmailVerificationHandler(token: String, navController: NavController) {
    val coroutineScope = rememberCoroutineScope()
    var message by remember { mutableStateOf("Verifying your email...") }
    var isSuccess by remember { mutableStateOf(false) }

    LaunchedEffect(token) {
        coroutineScope.launch {
            try {
                val response = RetrofitClient.api.verifyEmail(token)
                if (response.isSuccessful) {
                    message = "✅ Your email has been verified successfully!"
                    isSuccess = true
                } else {
                    message = "❌ Verification failed: ${response.errorBody()?.string()}"
                }
            } catch (e: Exception) {
                message = "❌ An error occurred: ${e.message}"
            }
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(text = message, style = MaterialTheme.typography.bodyLarge)

        Spacer(modifier = Modifier.height(24.dp))

        if (isSuccess) {
            Button(onClick = {
                navController.navigate("auth") {
                    popUpTo("verify/{token}") { inclusive = true }
                }
            }) {
                Text("Go to Login")
            }
        }
    }
}
