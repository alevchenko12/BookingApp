package com.nasti.bookingapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.nasti.bookingapp.ui.theme.MyApplicationTheme
import com.nasti.bookingapp.viewmodel.UserViewModel

class MainActivity : ComponentActivity() {
    private val userViewModel: UserViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MyApplicationTheme {
                // Call loadUsers() inside a LaunchedEffect to trigger the fetching when the composable is first loaded
                LaunchedEffect(Unit) {
                    userViewModel.loadUsers()  // This will call the loadUsers function
                }
                UserScreen(userViewModel)
            }
        }
    }
}

@Composable
fun UserScreen(userViewModel: UserViewModel) {
    // Observe the users state
    val users by userViewModel.users.collectAsState(initial = emptyList())

    // Print users list to the terminal
    println("Users List: $users")  // This will print the users list in the terminal

    Scaffold { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            Text(text = "Users:", style = MaterialTheme.typography.headlineMedium)
            users.forEach { user ->
                Text(text = "${user.name} - ${user.email}")
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun UserScreenPreview() {
    MyApplicationTheme {
        UserScreen(userViewModel = UserViewModel())
    }
}
