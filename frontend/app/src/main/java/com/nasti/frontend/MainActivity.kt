package com.nasti.frontend

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavHostController
import androidx.navigation.compose.*
import com.nasti.frontend.ui.auth.LoginScreen
import com.nasti.frontend.ui.auth.RegisterScreen
import com.nasti.frontend.ui.theme.BookingAppTheme
import com.nasti.frontend.utils.SessionManager

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val sessionManager = SessionManager(applicationContext)
        val isLoggedIn = sessionManager.isLoggedIn()

        setContent {
            BookingAppTheme {
                val navController = rememberNavController()
                AppNavHost(navController = navController, startDestination = if (isLoggedIn) "home" else "login")
            }
        }
    }
}

@Composable
fun AppNavHost(navController: NavHostController, startDestination: String) {
    NavHost(
        navController = navController,
        startDestination = startDestination
    ) {
        composable("login") {
            LoginScreen(
                onLoginSuccess = {
                    navController.navigate("home") {
                        popUpTo("login") { inclusive = true }
                    }
                }
            )
        }

        composable("register") {
            RegisterScreen(
                onRegisterSuccess = {
                    navController.navigate("home") {
                        popUpTo("register") { inclusive = true }
                    }
                }
            )
        }

        composable("home") {
            HomeScreen()
        }
    }
}

@Composable
fun HomeScreen() {
    Text(
        text = "Welcome to Booking App!",
        style = MaterialTheme.typography.headlineMedium,
        modifier = Modifier.padding(32.dp)
    )
}
