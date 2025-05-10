package com.nasti.frontend.ui.navigation

import androidx.compose.foundation.layout.padding
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.navigation.*
import androidx.navigation.compose.*
import com.nasti.frontend.ui.auth.*
import com.nasti.frontend.ui.landing.LandingScreen
import com.nasti.frontend.ui.profile.UserProfileScreen
import com.nasti.frontend.ui.search.SearchResultsScreen
import com.nasti.frontend.utils.SessionManager
import androidx.lifecycle.viewmodel.compose.viewModel
import com.nasti.frontend.ui.search.SearchViewModel

@Composable
fun AppNavHost(navController: NavHostController) {
    val context = LocalContext.current
    val sessionManager = SessionManager(context)
    val isLoggedIn = sessionManager.isLoggedIn()

    // ✅ Create a single shared SearchViewModel instance
    val searchViewModel: SearchViewModel = viewModel()

    NavHost(navController = navController, startDestination = "landing") {

        composable("landing") {
            LandingScreen(navController = navController, searchViewModel = searchViewModel)
        }

        composable("auth") {
            AuthLandingScreen(navController)
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

        composable("forgot") {
            ForgotPasswordScreen(navController)
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

        composable("profile") {
            if (isLoggedIn) {
                UserProfileScreen(navController = navController)
            } else {
                LaunchedEffect(Unit) {
                    navController.navigate("auth") {
                        popUpTo("profile") { inclusive = true }
                    }
                }
            }
        }

        composable("searchResults") {
            // ✅ Use the shared SearchViewModel
            SearchResultsScreen(navController = navController, viewModel = searchViewModel)
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
