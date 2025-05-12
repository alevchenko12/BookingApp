package com.nasti.frontend.ui.search

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.clickable
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Star
import androidx.compose.material.icons.filled.SwapVert
import androidx.compose.material.icons.filled.Tune
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
import java.text.SimpleDateFormat
import java.util.*
import java.util.concurrent.TimeUnit

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

    var showFilters by remember { mutableStateOf(false) }
    var showSortMenu by remember { mutableStateOf(false) }
    var selectedSort by remember { mutableStateOf(viewModel.sortBy ?: "") }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Available Hotels") },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
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
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(bottom = 12.dp),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                Box {
                    TextButton(onClick = { showSortMenu = true }) {
                        Icon(Icons.Default.SwapVert, contentDescription = "Sort")
                        Spacer(modifier = Modifier.width(4.dp))
                        Text(
                            if (selectedSort.isNotBlank())
                                selectedSort.replace("_", " ").replaceFirstChar { it.uppercaseChar() }
                            else "Sort"
                        )
                    }

                    DropdownMenu(expanded = showSortMenu, onDismissRequest = { showSortMenu = false }) {
                        listOf("price_asc", "price_desc", "rating", "reviews").forEach { option ->
                            DropdownMenuItem(
                                text = { Text(option.replace("_", " ").replaceFirstChar { it.uppercaseChar() }) },
                                onClick = {
                                    selectedSort = option
                                    viewModel.sortBy = option
                                    viewModel.performSearch()
                                    showSortMenu = false
                                }
                            )
                        }
                    }
                }

                TextButton(onClick = { showFilters = !showFilters }) {
                    Icon(Icons.Default.Tune, contentDescription = "Filter")
                    Spacer(modifier = Modifier.width(4.dp))
                    Text(if (showFilters) "Hide Filters" else "Filter")
                }
            }

            if (showFilters) {
                FilterSection(viewModel = viewModel, onApply = {
                    showFilters = false
                    viewModel.performSearch()
                })
            }

            if (hotels.isEmpty()) {
                Text("No results found.", style = MaterialTheme.typography.bodyLarge)
            } else {
                pagedHotels.forEach { hotel ->
                    HotelCard(hotel = hotel, viewModel = viewModel) {
                        navController.navigate("hotelDetail/${hotel.id}")
                    }
                    Spacer(modifier = Modifier.height(16.dp))
                }

                Row(
                    horizontalArrangement = Arrangement.Center,
                    modifier = Modifier.fillMaxWidth().padding(top = 12.dp)
                ) {
                    for (page in 1..totalPages) {
                        TextButton(onClick = { currentPage = page }) {
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
fun HotelCard(hotel: HotelSearchResult, viewModel: SearchViewModel, onClick: () -> Unit) {
    val nights = calculateNights(viewModel.checkIn, viewModel.checkOut)

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

            Spacer(modifier = Modifier.height(4.dp))

            Row(
                horizontalArrangement = Arrangement.SpaceBetween,
                modifier = Modifier.fillMaxWidth()
            ) {
                Row {
                    repeat(hotel.stars ?: 0) {
                        Icon(Icons.Default.Star, contentDescription = "Star", tint = MaterialTheme.colorScheme.primary)
                    }
                }

                hotel.lowest_price?.let { pricePerNight ->
                    val totalPrice = pricePerNight * nights
                    Text(
                        text = "From $${"%.2f".format(totalPrice)} for $nights night${if (nights > 1) "s" else ""}",
                        style = MaterialTheme.typography.bodyMedium
                    )
                }
            }

            Row(modifier = Modifier.fillMaxWidth().padding(top = 4.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                hotel.average_rating?.let {
                    Text("⭐ %.1f".format(it), style = MaterialTheme.typography.bodySmall)
                }
                if (hotel.review_count > 0) {
                    Text("${hotel.review_count} review${if (hotel.review_count != 1) "s" else ""}", style = MaterialTheme.typography.bodySmall)
                }
            }
        }
    }
}

fun calculateNights(checkIn: String, checkOut: String): Int {
    return try {
        val sdf = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
        val date1 = sdf.parse(checkIn)
        val date2 = sdf.parse(checkOut)
        val diffInMillis = date2.time - date1.time
        TimeUnit.DAYS.convert(diffInMillis, TimeUnit.MILLISECONDS).toInt().coerceAtLeast(1)
    } catch (e: Exception) {
        1
    }
}
