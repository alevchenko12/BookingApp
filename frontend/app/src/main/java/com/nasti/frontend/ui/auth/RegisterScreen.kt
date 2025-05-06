package com.nasti.frontend.ui.auth

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import com.nasti.frontend.data.api.RetrofitClient
import com.nasti.frontend.data.model.RegisterRequest
import com.nasti.frontend.data.repository.AuthRepository
import com.nasti.frontend.utils.SessionManager

@Composable
fun RegisterScreen(
    viewModel: RegisterViewModel = remember {
        RegisterViewModel(AuthRepository(RetrofitClient.api))
    },
    onRegisterSuccess: () -> Unit
) {
    val context = LocalContext.current
    val sessionManager = remember { SessionManager(context) }

    var firstName by remember { mutableStateOf("") }
    var lastName by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var phone by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }

    val registerResult = viewModel.registerState.value

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("Register", style = MaterialTheme.typography.headlineMedium)

        Spacer(modifier = Modifier.height(16.dp))
        OutlinedTextField(
            value = firstName,
            onValueChange = { firstName = it },
            label = { Text("First Name") },
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(8.dp))
        OutlinedTextField(
            value = lastName,
            onValueChange = { lastName = it },
            label = { Text("Last Name") },
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(8.dp))
        OutlinedTextField(
            value = email,
            onValueChange = { email = it },
            label = { Text("Email") },
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(8.dp))
        OutlinedTextField(
            value = phone,
            onValueChange = { phone = it },
            label = { Text("Phone (optional)") },
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
            onClick = {
                val request = RegisterRequest(
                    first_name = firstName,
                    last_name = lastName,
                    email = email,
                    phone = phone.ifBlank { null },
                    password = password
                )
                viewModel.register(request)
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Register")
        }

        if (registerResult != null) {
            Spacer(modifier = Modifier.height(16.dp))
            if (registerResult.isSuccess) {
                val token = registerResult.getOrNull()?.access_token ?: ""
                LaunchedEffect(token) {
                    sessionManager.saveToken(token)
                    onRegisterSuccess()
                }
            } else {
                Text(
                    text = registerResult.exceptionOrNull()?.message ?: "Registration failed",
                    color = MaterialTheme.colorScheme.error
                )
            }
        }
    }
}
