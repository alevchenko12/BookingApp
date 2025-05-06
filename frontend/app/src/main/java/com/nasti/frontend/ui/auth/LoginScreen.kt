package com.nasti.frontend.ui.auth

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.Alignment
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.tooling.preview.Preview
import com.nasti.frontend.data.api.RetrofitClient
import com.nasti.frontend.data.repository.AuthRepository
import com.nasti.frontend.utils.SessionManager

@Composable
fun LoginScreen(
    viewModel: LoginViewModel = remember {
        LoginViewModel(AuthRepository(RetrofitClient.api))
    },
    onLoginSuccess: () -> Unit
) {
    val context = LocalContext.current
    val sessionManager = remember { SessionManager(context) }

    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }

    val loginResult = viewModel.loginState.value

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("Login", style = MaterialTheme.typography.headlineMedium)

        Spacer(modifier = Modifier.height(16.dp))
        OutlinedTextField(
            value = email,
            onValueChange = { email = it },
            label = { Text("Email") },
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(8.dp))
        OutlinedTextField(
            value = password,
            onValueChange = { password = it },
            label = { Text("Password") },
            visualTransformation = PasswordVisualTransformation(),
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(16.dp))
        Button(
            onClick = { viewModel.login(email, password) },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Login")
        }

        if (loginResult != null) {
            Spacer(modifier = Modifier.height(16.dp))
            if (loginResult.isSuccess) {
                val token = loginResult.getOrNull()?.access_token ?: ""
                LaunchedEffect(token) {
                    sessionManager.saveToken(token)
                    onLoginSuccess()
                }
            } else {
                Text(
                    text = loginResult.exceptionOrNull()?.message ?: "Login failed",
                    color = MaterialTheme.colorScheme.error
                )
            }
        }
    }
}
