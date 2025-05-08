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
import com.nasti.frontend.ui.auth.AuthLandingScreen
import com.nasti.frontend.ui.auth.RegisterScreen
import com.nasti.frontend.ui.auth.ForgotPasswordScreen
import com.nasti.frontend.ui.auth.EmailVerificationHandler
import com.nasti.frontend.ui.auth.VerifyCodeScreen
import com.nasti.frontend.ui.auth.ResetPasswordScreen
import com.nasti.frontend.ui.profile.UserProfileScreen
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

                // Handle deep link for email verification
                val deepLinkToken = intent?.data?.getQueryParameter("token")
                if (deepLinkToken != null) {
                    LaunchedEffect(deepLinkToken) {
                        navController.navigate("verify/$deepLinkToken")
                    }
                }

                AppNavHost(
                    navController = navController,
                    startDestination = if (isLoggedIn) "profile" else "auth"
                )
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
        composable("auth") {
            AuthLandingScreen(navController = navController)
        }

        composable("forgot") {
            ForgotPasswordScreen(navController = navController)
        }

        composable("register") {
            RegisterScreen(
                navController = navController,
                onRegisterSuccess = {
                    navController.navigate("profile") {
                        popUpTo("register") { inclusive = true }
                    }
                }
            )
        }

        composable("profile") {
            UserProfileScreen(navController = navController)
        }

        composable("verify/{token}") { backStackEntry ->
            val token = backStackEntry.arguments?.getString("token") ?: ""
            EmailVerificationHandler(token = token, navController = navController)
        }

        composable("verifyCode/{email}") { backStackEntry ->
            val email = backStackEntry.arguments?.getString("email") ?: ""
            VerifyCodeScreen(navController = navController, email = email)
        }

        composable("resetPassword/{email}") { backStackEntry ->
            val email = backStackEntry.arguments?.getString("email") ?: ""
            ResetPasswordScreen(navController = navController, email = email)
        }


        composable("home") {
            Text(
                text = "Welcome to Booking App!",
                style = MaterialTheme.typography.headlineMedium,
                modifier = Modifier.padding(32.dp)
            )
        }
    }
}
