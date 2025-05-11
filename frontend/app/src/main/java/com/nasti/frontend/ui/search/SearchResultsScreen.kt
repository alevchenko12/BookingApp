package com.nasti.frontend.ui.search

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.clickable
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
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
import com.nasti.frontend.ui.components.BottomNavigationBar

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SearchResultsScreen(
    navController: NavController,
    viewModel: SearchViewModel = viewModel()
) {
    val hotels by viewModel.searchResults.collectAsState()

    var currentPage by remember { mutableStateOf(1) }
    val hotelsPerPage = 10
    val totalPages = (hotels.size + hotelsPerPage - 1) / hotelsPerPage
    val pagedHotels = hotels.drop((currentPage - 1) * hotelsPerPage).take(hotelsPerPage)

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Available Hotels") },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        },
        bottomBar = {
            BottomNavigationBar(navController = navController, selected = "search")
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
                pagedHotels.forEach { hotel ->
                    HotelCard(hotel = hotel, onClick = {
                        navController.navigate("hotelDetail/${hotel.id}")
                    })
                    Spacer(modifier = Modifier.height(16.dp))
                }

                // Page number buttons
                Row(
                    horizontalArrangement = Arrangement.Center,
                    modifier = Modifier.fillMaxWidth().padding(top = 12.dp)
                ) {
                    for (page in 1..totalPages) {
                        TextButton(
                            onClick = { currentPage = page }
                        ) {
                            Text(
                                text = page.toString(),
                                fontWeight = if (page == currentPage) FontWeight.Bold else FontWeight.Normal
                            )
                        }
                    }
                }
            }
        }
    }
}
@Composable
fun HotelCard(hotel: HotelSearchResult, onClick: () -> Unit) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(4.dp),
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(
            modifier = Modifier
                .clickable { onClick() }
                .padding(16.dp)
        ) {
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
                                imageVector = Icons.Default.Star,
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
