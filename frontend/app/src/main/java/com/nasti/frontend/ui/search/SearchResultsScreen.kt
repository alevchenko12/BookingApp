package com.nasti.frontend.ui.search

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.clickable
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import coil.compose.rememberAsyncImagePainter
import com.nasti.frontend.data.model.HotelSearchResult

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SearchResultsScreen(
    navController: NavController,
    viewModel: SearchViewModel = viewModel()
) {
    val hotels by viewModel.searchResults.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Available Hotels") })
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .padding(padding)
                .padding(16.dp)
        ) {
            if (hotels.isEmpty()) {
                Text("No results found.", style = MaterialTheme.typography.bodyLarge)
            } else {
                hotels.forEach { hotel ->
                    HotelCard(hotel = hotel, onClick = {
                        // TODO: Navigate to hotel details: navController.navigate("hotel/${hotel.id}")
                    })
                    Spacer(modifier = Modifier.height(16.dp))
                }
            }
        }
    }
}

@Composable
fun HotelCard(hotel: HotelSearchResult, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() },
        elevation = CardDefaults.cardElevation(4.dp),
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            hotel.cover_image_url?.let { imageUrl ->
                Image(
                    painter = rememberAsyncImagePainter(model = imageUrl),
                    contentDescription = "Hotel cover image",
                    contentScale = ContentScale.Crop,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(160.dp)
                        .clip(RoundedCornerShape(10.dp))
                )
                Spacer(modifier = Modifier.height(8.dp))
            }

            Text(hotel.name, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
            Text("${hotel.address}, ${hotel.city}, ${hotel.country}", style = MaterialTheme.typography.bodySmall)

            Row(
                horizontalArrangement = Arrangement.SpaceBetween,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 8.dp)
            ) {
                hotel.stars?.let {
                    Row {
                        repeat(it) {
                            Icon(
                                Icons.Default.Star,
                                contentDescription = "Star",
                                tint = MaterialTheme.colorScheme.primary
                            )
                        }
                    }
                }

                hotel.lowest_price?.let {
                    Text("From $${"%.2f".format(it)}", style = MaterialTheme.typography.bodyMedium)
                }
            }
        }
    }
}
