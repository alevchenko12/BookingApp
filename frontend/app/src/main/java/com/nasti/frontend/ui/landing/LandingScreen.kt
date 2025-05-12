package com.nasti.frontend.ui.landing

import android.widget.Toast
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
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.nasti.frontend.data.api.RetrofitClient
import com.nasti.frontend.data.model.HotelSearchRequest
import com.nasti.frontend.data.model.LocationSuggestion
import com.nasti.frontend.ui.components.BottomNavigationBar
import com.nasti.frontend.ui.search.SearchViewModel
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LandingScreen(
    navController: NavController,
    viewModel: LandingViewModel = viewModel(),
    searchViewModel: SearchViewModel = viewModel()
) {
    val destination by viewModel.destination.collectAsState()
    val suggestions by viewModel.suggestions.collectAsState()

    val context = LocalContext.current
    val formatter = remember { SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()) }
    val dateLabelFormatter = remember { SimpleDateFormat("dd MMM yyyy", Locale.getDefault()) }

    val datePickerState = rememberDateRangePickerState()
    var showDatePicker by remember { mutableStateOf(false) }

    val startMillis = datePickerState.selectedStartDateMillis
    val endMillis = datePickerState.selectedEndDateMillis

    val dateRangeText = when {
        startMillis != null && endMillis != null -> "${dateLabelFormatter.format(Date(startMillis))} - ${dateLabelFormatter.format(Date(endMillis))}"
        startMillis != null -> "${dateLabelFormatter.format(Date(startMillis))} - Select checkout"
        else -> "Select dates"
    }

    val today = Calendar.getInstance().apply {
        set(Calendar.HOUR_OF_DAY, 0)
        set(Calendar.MINUTE, 0)
        set(Calendar.SECOND, 0)
        set(Calendar.MILLISECOND, 0)
    }.timeInMillis

    var showGuestDialog by remember { mutableStateOf(false) }
    var rooms by remember { mutableStateOf(1) }
    var adults by remember { mutableStateOf(1) }

    val guests = "$rooms room${if (rooms > 1) "s" else ""}, $adults adult${if (adults > 1) "s" else ""}"

    val coroutineScope = rememberCoroutineScope()

    Scaffold(
        topBar = { TopAppBar(title = { Text("Booking App") }) },
        bottomBar = { BottomNavigationBar(navController = navController, selected = "search") }
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
                value = dateRangeText,
                onValueChange = {},
                label = { Text("Select dates") },
                readOnly = true,
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { showDatePicker = true }
            )

            if (showDatePicker) {
                DatePickerDialog(
                    onDismissRequest = { showDatePicker = false },
                    confirmButton = {
                        TextButton(onClick = {
                            if (startMillis == null || endMillis == null) {
                                Toast.makeText(context, "Please select valid dates", Toast.LENGTH_SHORT).show()
                            } else {
                                showDatePicker = false
                            }
                        }) { Text("OK") }
                    },
                    dismissButton = {
                        TextButton(onClick = { showDatePicker = false }) { Text("Cancel") }
                    }
                ) {
                    DateRangePicker(state = datePickerState)
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            OutlinedTextField(
                value = guests,
                onValueChange = {},
                label = { Text("Rooms & Guests") },
                readOnly = true,
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { showGuestDialog = true }
            )

            if (showGuestDialog) {
                AlertDialog(
                    onDismissRequest = { showGuestDialog = false },
                    confirmButton = {
                        TextButton(onClick = { showGuestDialog = false }) { Text("OK") }
                    },
                    dismissButton = {
                        TextButton(onClick = { showGuestDialog = false }) { Text("Cancel") }
                    },
                    title = { Text("Select Rooms & Guests") },
                    text = {
                        Column {
                            Text("Rooms")
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.SpaceBetween,
                                modifier = Modifier.fillMaxWidth()
                            ) {
                                IconButton(onClick = { if (rooms > 1) rooms-- }) { Text("-") }
                                Text("$rooms", style = MaterialTheme.typography.titleLarge)
                                IconButton(onClick = { rooms++ }) { Text("+") }
                            }
                            Spacer(modifier = Modifier.height(16.dp))
                            Text("Adults")
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.SpaceBetween,
                                modifier = Modifier.fillMaxWidth()
                            ) {
                                IconButton(onClick = { if (adults > 1) adults-- }) { Text("-") }
                                Text("$adults", style = MaterialTheme.typography.titleLarge)
                                IconButton(onClick = { adults++ }) { Text("+") }
                            }
                        }
                    }
                )
            }

            Spacer(modifier = Modifier.height(16.dp))

            Button(
                onClick = {
                    coroutineScope.launch {
                        try {
                            val checkInDate = formatter.format(Date(startMillis!!))
                            val checkOutDate = formatter.format(Date(endMillis!!))

                            val searchRequest = HotelSearchRequest(
                                destination = destination,
                                check_in = checkInDate,
                                check_out = checkOutDate,
                                rooms = rooms,
                                adults = adults,
                                min_stars = null,
                                has_wifi = null,
                                allows_pets = null,
                                has_kitchen = null,
                                has_air_conditioning = null,
                                has_tv = null,
                                has_safe = null,
                                has_balcony = null,
                                sort_by = null
                            )

                            val response = RetrofitClient.api.searchAvailableHotels(searchRequest)
                            if (response.isSuccessful) {
                                val hotels = response.body() ?: emptyList()

                                // Save context to SearchViewModel
                                searchViewModel.setSearchContext(
                                    destination = destination,
                                    checkIn = checkInDate,
                                    checkOut = checkOutDate,
                                    adults = adults,
                                    rooms = rooms
                                )

                                searchViewModel.setResults(hotels)
                                Toast.makeText(context, "Found ${hotels.size} hotels", Toast.LENGTH_SHORT).show()
                                navController.navigate("searchResults")
                            } else {
                                Toast.makeText(context, "Search failed", Toast.LENGTH_SHORT).show()
                            }
                        } catch (e: Exception) {
                            Toast.makeText(context, "Error: ${e.localizedMessage}", Toast.LENGTH_LONG).show()
                        }
                    }
                },
                enabled = destination.isNotBlank() &&
                        startMillis != null &&
                        endMillis != null &&
                        endMillis > startMillis &&
                        startMillis >= today,
                modifier = Modifier.fillMaxWidth()
            ) {
                Icon(Icons.Default.Search, contentDescription = null)
                Spacer(Modifier.width(8.dp))
                Text("Search")
            }
        }
    }
}
