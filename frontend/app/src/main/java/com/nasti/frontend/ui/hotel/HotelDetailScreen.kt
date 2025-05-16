package com.nasti.frontend.ui.hotel

import android.widget.Toast
import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import coil.compose.rememberAsyncImagePainter
import com.nasti.frontend.data.model.HotelDetailResponse
import com.nasti.frontend.ui.search.SearchViewModel
import com.nasti.frontend.utils.SessionManager

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HotelDetailScreen(
    navController: NavController,
    hotelId: Int,
    searchViewModel: SearchViewModel,
    viewModel: HotelDetailViewModel = viewModel()
) {
    val hotel by viewModel.hotel.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    val error by viewModel.error.collectAsState()

    LaunchedEffect(hotelId) {
        viewModel.loadHotel(hotelId)
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Hotel Details") },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Box(modifier = Modifier.padding(padding)) {
            when {
                isLoading -> CircularProgressIndicator(modifier = Modifier.padding(32.dp))
                error != null -> Text(
                    text = error ?: "Unknown error",
                    modifier = Modifier.padding(16.dp),
                    color = MaterialTheme.colorScheme.error
                )
                hotel != null -> HotelDetailContent(
                    hotel = hotel!!,
                    navController = navController,
                    searchViewModel = searchViewModel
                )
            }
        }
    }
}

@Composable
fun HotelDetailContent(
    hotel: HotelDetailResponse,
    navController: NavController,
    searchViewModel: SearchViewModel
) {
    val context = LocalContext.current
    val session = remember { SessionManager(context) }

    val checkIn = searchViewModel.checkIn
    val checkOut = searchViewModel.checkOut

    LazyColumn(modifier = Modifier.padding(16.dp)) {
        item {
            Text(hotel.name, style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
            Text("${hotel.address}, ${hotel.city}, ${hotel.country}", style = MaterialTheme.typography.bodyMedium)

            hotel.stars?.let {
                Row(modifier = Modifier.padding(top = 4.dp)) {
                    repeat(it) {
                        Icon(Icons.Default.Star, contentDescription = "Star", tint = MaterialTheme.colorScheme.primary)
                    }
                }
            }

            hotel.description?.let {
                Text(it, style = MaterialTheme.typography.bodySmall, modifier = Modifier.padding(top = 8.dp))
            }

            Spacer(modifier = Modifier.height(16.dp))
        }

        item {
            Text("Photos", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
            Row(
                modifier = Modifier
                    .horizontalScroll(rememberScrollState())
                    .padding(vertical = 8.dp)
            ) {
                hotel.photos.forEach { url ->
                    Image(
                        painter = rememberAsyncImagePainter(url),
                        contentDescription = null,
                        contentScale = ContentScale.Crop,
                        modifier = Modifier
                            .padding(end = 8.dp)
                            .size(200.dp)
                            .clip(MaterialTheme.shapes.medium)
                    )
                }
            }
        }

        item {
            Text("Rooms", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
            Spacer(modifier = Modifier.height(8.dp))
        }

        items(hotel.rooms) { room ->
            var expanded by remember { mutableStateOf(false) }

            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 4.dp)
                    .clickable { expanded = !expanded },
                elevation = CardDefaults.cardElevation(2.dp)
            ) {
                Column(modifier = Modifier.padding(12.dp)) {
                    Text("${room.name} - $${"%.2f".format(room.price_per_night)} / night, ${room.capacity} guests")
                    Text(
                        "Type: ${room.room_type}, Cancellation: ${room.cancellation_policy ?: "N/A"}",
                        style = MaterialTheme.typography.bodySmall
                    )

                    if (expanded) {
                        Spacer(modifier = Modifier.height(8.dp))
                        Text("Facilities:", style = MaterialTheme.typography.bodySmall, fontWeight = FontWeight.SemiBold)
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            if (room.has_wifi) Icon(Icons.Default.Wifi, contentDescription = "WiFi")
                            if (room.has_tv) Icon(Icons.Default.Tv, contentDescription = "TV")
                            if (room.has_air_conditioning) Icon(Icons.Default.AcUnit, contentDescription = "AC")
                            if (room.has_balcony) Icon(Icons.Default.Balcony, contentDescription = "Balcony")
                            if (room.has_minibar) Icon(Icons.Default.LocalBar, contentDescription = "Minibar")
                            if (room.has_safe) Icon(Icons.Default.Lock, contentDescription = "Safe")
                            if (room.has_kitchen) Icon(Icons.Default.Kitchen, contentDescription = "Kitchen")
                            if (room.allows_pets) Icon(Icons.Default.Pets, contentDescription = "Pets allowed")
                        }

                        Spacer(modifier = Modifier.height(12.dp))

                        Button(
                            onClick = {
                                val roomId = room.id
                                val route = "booking/$roomId"

                                if (checkIn.isBlank() || checkOut.isBlank()) {
                                    Toast.makeText(context, "Please select dates before booking", Toast.LENGTH_SHORT).show()
                                } else {
                                    searchViewModel.setSelectedRoomPrice(room.price_per_night)

                                    if (session.isLoggedIn()) {
                                        navController.navigate(route)
                                    } else {
                                        navController.navigate("auth?redirect=$route")
                                    }
                                }
                            },
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(top = 8.dp)
                        ) {
                            Text("Book Now")
                        }
                    }
                }
            }
        }

        item {
            Spacer(modifier = Modifier.height(16.dp))
            Text("Reviews", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
            Spacer(modifier = Modifier.height(8.dp))
        }

        items(hotel.reviews) { review ->
            Text("${review.user_name ?: "Anonymous"} • ${review.rating}/5", fontWeight = FontWeight.SemiBold)
            review.text?.let {
                Text(it, style = MaterialTheme.typography.bodySmall, modifier = Modifier.padding(bottom = 8.dp))
            }
        }
    }
}
