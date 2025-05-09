package com.nasti.frontend.ui.landing

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.LocationCity
import androidx.compose.material.icons.filled.Public
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.nasti.frontend.data.model.LocationSuggestion
import com.nasti.frontend.ui.components.BottomNavigationBar

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LandingScreen(
    navController: NavController,
    viewModel: LandingViewModel = viewModel()
) {
    val destination by viewModel.destination.collectAsState()
    val suggestions by viewModel.suggestions.collectAsState()

    var dateRange by remember { mutableStateOf("Select dates") }
    var guests by remember { mutableStateOf("1 room, 2 adults") }

    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Booking App") })
        },
        bottomBar = {
            BottomNavigationBar(navController = navController, selected = "search")
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .padding(padding)
                .padding(16.dp)
                .fillMaxSize(),
            verticalArrangement = Arrangement.Top,
            horizontalAlignment = Alignment.Start
        ) {
            OutlinedTextField(
                value = destination,
                onValueChange = { viewModel.updateDestination(it) },
                label = { Text("Enter destination") },
                modifier = Modifier.fillMaxWidth()
            )

            if (suggestions.isNotEmpty()) {
                Column(modifier = Modifier.fillMaxWidth()) {
                    suggestions.forEach { item ->
                        val label = when (item) {
                            is LocationSuggestion.CityItem -> "${item.name}, ${item.countryName ?: "Unknown"}"
                            is LocationSuggestion.CountryItem -> item.name
                        }

                        val icon = when (item) {
                            is LocationSuggestion.CityItem -> Icons.Default.LocationCity
                            is LocationSuggestion.CountryItem -> Icons.Default.Public
                        }

                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable { viewModel.selectSuggestion(item) }
                                .padding(vertical = 8.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(icon, contentDescription = null, modifier = Modifier.padding(end = 8.dp))
                            Text(label, style = MaterialTheme.typography.bodyMedium)
                        }
                        Divider()
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                }
            }

            OutlinedTextField(
                value = dateRange,
                onValueChange = {},
                label = { Text("Select dates") },
                readOnly = true,
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(8.dp))

            OutlinedTextField(
                value = guests,
                onValueChange = {},
                label = { Text("Rooms & Guests") },
                readOnly = true,
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(16.dp))

            Button(
                onClick = {
                    // TODO: Trigger search using destination, date, guests
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Icon(Icons.Default.Search, contentDescription = null)
                Spacer(Modifier.width(8.dp))
                Text("Search")
            }
        }
    }
}
