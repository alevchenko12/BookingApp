package com.nasti.frontend

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.runtime.LaunchedEffect
import androidx.navigation.compose.rememberNavController
import com.nasti.frontend.ui.navigation.AppNavHost
import com.nasti.frontend.ui.theme.BookingAppTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            BookingAppTheme {
                val navController = rememberNavController()

                // Handle email verification deep link
                val deepLinkToken = intent?.data?.getQueryParameter("token")
                if (deepLinkToken != null) {
                    LaunchedEffect(deepLinkToken) {
                        navController.navigate("verify/$deepLinkToken")
                    }
                }

                AppNavHost(navController = navController)
            }
        }
    }
}
