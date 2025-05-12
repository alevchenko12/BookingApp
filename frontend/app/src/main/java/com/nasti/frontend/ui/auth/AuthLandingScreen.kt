package com.nasti.frontend.ui.auth

import android.util.Patterns
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.nasti.frontend.data.api.RetrofitClient
import com.nasti.frontend.data.repository.AuthRepository
import com.nasti.frontend.ui.components.BottomNavigationBar
import com.nasti.frontend.utils.SessionManager

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AuthLandingScreen(
    navController: NavController,
    redirect: String = "profile", // ✅ Accept redirect
    viewModel: LoginViewModel = remember {
        LoginViewModel(AuthRepository(RetrofitClient.api))
    }
) {
    val context = LocalContext.current
    val sessionManager = remember { SessionManager(context) }

    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }

    var emailError by remember { mutableStateOf<String?>(null) }
    var passwordError by remember { mutableStateOf<String?>(null) }

    val loginResult = viewModel.loginState.value
    val errorMessage = viewModel.errorMessage.value

    fun validate(): Boolean {
        var isValid = true

        if (!Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
            emailError = "Invalid email format"
            isValid = false
        } else emailError = null

        if (password.length !in 6..100) {
            passwordError = "Password must be 6–100 characters"
            isValid = false
        } else passwordError = null

        return isValid
    }

    LaunchedEffect(loginResult) {
        if (loginResult?.isSuccess == true) {
            val token = loginResult.getOrNull()?.access_token ?: ""
            sessionManager.saveToken(token)
            navController.navigate(redirect) { // ✅ Navigate to the redirect
                popUpTo("auth") { inclusive = true }
            }
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Login") },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        },
        bottomBar = {
            BottomNavigationBar(navController = navController, selected = "search")
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(24.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            OutlinedTextField(
                value = email,
                onValueChange = { email = it },
                label = { Text("Email") },
                isError = emailError != null,
                modifier = Modifier.fillMaxWidth()
            )
            emailError?.let {
                Text(it, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
            }

            Spacer(modifier = Modifier.height(8.dp))

            OutlinedTextField(
                value = password,
                onValueChange = { password = it },
                label = { Text("Password") },
                visualTransformation = PasswordVisualTransformation(),
                isError = passwordError != null,
                modifier = Modifier.fillMaxWidth()
            )
            passwordError?.let {
                Text(it, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
            }

            Spacer(modifier = Modifier.height(16.dp))

            Button(
                onClick = {
                    if (validate()) {
                        viewModel.login(email, password)
                    }
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Login")
            }

            if (!errorMessage.isNullOrEmpty()) {
                Spacer(modifier = Modifier.height(12.dp))
                Text(
                    text = errorMessage,
                    color = MaterialTheme.colorScheme.error,
                    style = MaterialTheme.typography.bodyMedium
                )
            }

            Spacer(modifier = Modifier.height(24.dp))

            Text(
                text = "Forgot password?",
                style = MaterialTheme.typography.bodyLarge,
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier
                    .clickable { navController.navigate("forgot") }
                    .padding(top = 8.dp)
            )

            Spacer(modifier = Modifier.height(8.dp))

            Text(
                text = "Don't have an account? Register",
                style = MaterialTheme.typography.bodyLarge,
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier
                    .clickable { navController.navigate("register") }
                    .padding(top = 8.dp)
            )
        }
    }
}
