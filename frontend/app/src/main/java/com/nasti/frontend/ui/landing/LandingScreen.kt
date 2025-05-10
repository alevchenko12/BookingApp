package com.nasti.frontend.ui.landing

import android.app.DatePickerDialog
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
import com.nasti.frontend.data.model.LocationSuggestion
import com.nasti.frontend.ui.components.BottomNavigationBar
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LandingScreen(
    navController: NavController,
    viewModel: LandingViewModel = viewModel()
) {
    val destination by viewModel.destination.collectAsState()
    val suggestions by viewModel.suggestions.collectAsState()

    var guests by remember { mutableStateOf("1 room, 2 adults") }

    val context = LocalContext.current
    val formatter = remember { SimpleDateFormat("dd/MM/yyyy", Locale.getDefault()) }

    var startDate by remember { mutableStateOf<Calendar?>(null) }
    var endDate by remember { mutableStateOf<Calendar?>(null) }
    var showStartPicker by remember { mutableStateOf(false) }
    var showEndPicker by remember { mutableStateOf(false) }

    val today = remember {
        Calendar.getInstance().apply {
            set(Calendar.HOUR_OF_DAY, 0)
            set(Calendar.MINUTE, 0)
            set(Calendar.SECOND, 0)
            set(Calendar.MILLISECOND, 0)
        }
    }

    val dateRangeText = when {
        startDate != null && endDate != null -> "${formatter.format(startDate!!.time)} - ${formatter.format(endDate!!.time)}"
        startDate != null -> "${formatter.format(startDate!!.time)} - Select checkout"
        else -> "Select dates"
    }

    // 🗓 Start date picker
    LaunchedEffect(showStartPicker) {
        if (showStartPicker) {
            DatePickerDialog(
                context,
                { _, year, month, day ->
                    startDate = Calendar.getInstance().apply {
                        set(year, month, day, 0, 0)
                    }
                    endDate = null // reset checkout
                    showStartPicker = false
                    showEndPicker = true
                },
                today.get(Calendar.YEAR),
                today.get(Calendar.MONTH),
                today.get(Calendar.DAY_OF_MONTH)
            ).apply {
                datePicker.minDate = today.timeInMillis
            }.show()
        }
    }

    // 🗓 End date picker
    LaunchedEffect(showEndPicker) {
        if (showEndPicker && startDate != null) {
            val minCheckout = (startDate!!.clone() as Calendar).apply { add(Calendar.DAY_OF_MONTH, 1) }
            DatePickerDialog(
                context,
                { _, year, month, day ->
                    endDate = Calendar.getInstance().apply {
                        set(year, month, day, 0, 0)
                    }
                    showEndPicker = false
                },
                minCheckout.get(Calendar.YEAR),
                minCheckout.get(Calendar.MONTH),
                minCheckout.get(Calendar.DAY_OF_MONTH)
            ).apply {
                datePicker.minDate = minCheckout.timeInMillis
            }.show()
        }
    }

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

            // Date Range Field
            OutlinedTextField(
                value = dateRangeText,
                onValueChange = {},
                label = { Text("Select dates") },
                readOnly = true,
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { showStartPicker = true }
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
                    // Trigger search using destination, date range, guests
                },
                enabled = destination.isNotBlank() && startDate != null && endDate != null,
                modifier = Modifier.fillMaxWidth()
            ) {
                Icon(Icons.Default.Search, contentDescription = null)
                Spacer(Modifier.width(8.dp))
                Text("Search")
            }
        }
    }
}
