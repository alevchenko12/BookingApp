package com.nasti.frontend.ui.components

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.navigation.NavController

@Composable
fun BottomNavigationBar(navController: NavController, selected: String) {
    NavigationBar {
        NavigationBarItem(
            icon = { Icon(Icons.Default.Search, contentDescription = "Search") },
            label = { Text("Search") },
            selected = selected == "search",
            onClick = { navController.navigate("landing") }
        )
        NavigationBarItem(
            icon = { Icon(Icons.Default.Favorite, contentDescription = "Saved") },
            label = { Text("Saved") },
            selected = selected == "saved",
            onClick = { navController.navigate("saved") }
        )
        NavigationBarItem(
            icon = { Icon(Icons.Default.Luggage, contentDescription = "Bookings") },
            label = { Text("Bookings") },
            selected = selected == "bookings",
            onClick = { navController.navigate("bookings") }
        )
        NavigationBarItem(
            icon = { Icon(Icons.Default.Person, contentDescription = "Profile") },
            label = { Text("Profile") },
            selected = selected == "profile",
            onClick = { navController.navigate("profile") }
        )
    }
}
