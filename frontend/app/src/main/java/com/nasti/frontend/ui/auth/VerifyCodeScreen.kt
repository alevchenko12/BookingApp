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

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun VerifyCodeScreen(navController: NavController, email: String) {
    val scope = rememberCoroutineScope()

    var code by remember { mutableStateOf("") }
    var codeError by remember { mutableStateOf<String?>(null) }
    var errorMessage by remember { mutableStateOf<String?>(null) }

    fun validate(): Boolean {
        return if (code.length != 6 || !code.all { it.isDigit() }) {
            codeError = "Code must be 6 digits"
            false
        } else {
            codeError = null
            true
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Verify Code") })
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .padding(padding)
                .padding(24.dp)
                .fillMaxSize(),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text("Enter the 6-digit code sent to your email")

            Spacer(modifier = Modifier.height(16.dp))

            OutlinedTextField(
                value = code,
                onValueChange = { code = it },
                label = { Text("Verification Code") },
                isError = codeError != null,
                modifier = Modifier.fillMaxWidth()
            )
            codeError?.let {
                Text(it, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
            }

            Spacer(modifier = Modifier.height(16.dp))

            Button(
                onClick = {
                    if (validate()) {
                        scope.launch {
                            try {
                                val response = RetrofitClient.api.verifyCode(
                                    mapOf("email" to email, "code" to code)
                                )
                                if (response.isSuccessful) {
                                    navController.navigate("resetPassword/$email") {
                                        popUpTo("verifyCode/$email") { inclusive = true }
                                    }
                                } else {
                                    errorMessage = "Invalid or expired code."
                                }
                            } catch (e: Exception) {
                                errorMessage = "Network error: ${e.localizedMessage}"
                            }
                        }
                    }
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Verify")
            }

            errorMessage?.let {
                Spacer(modifier = Modifier.height(16.dp))
                Text(it, color = MaterialTheme.colorScheme.error)
            }
        }
    }
}
