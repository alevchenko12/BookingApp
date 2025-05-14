package com.nasti.frontend.ui.booking

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
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
import com.nasti.frontend.ui.components.BottomNavigationBar
import com.nasti.frontend.ui.mybookings.BookingListViewModel
import com.nasti.frontend.data.model.BookingUiModel
import com.nasti.frontend.ui.search.calculateNights
import com.nasti.frontend.utils.SessionManager
import com.nasti.frontend.data.api.RetrofitClient
import kotlinx.coroutines.launch
import android.widget.Toast

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BookingListScreen(
    navController: NavController,
    viewModel: BookingListViewModel = viewModel()
) {
    val context = LocalContext.current
    val session = remember { SessionManager(context) }

    LaunchedEffect(Unit) {
        val token = session.getToken()
        if (!token.isNullOrBlank()) {
            viewModel.loadBookings(token)
        }
    }

    val bookings by viewModel.bookings.collectAsState()
    val selectedStatus by viewModel.selectedStatus.collectAsState()

    val statuses = listOf("all", "pending", "confirmed", "completed", "cancelled")

    Scaffold(
        topBar = { TopAppBar(title = { Text("My Bookings") }) },
        bottomBar = { BottomNavigationBar(navController = navController, selected = "bookings") }
    ) { padding ->
        Column(
            modifier = Modifier
                .padding(padding)
                .fillMaxSize()
        ) {
            ScrollableTabRow(
                selectedTabIndex = statuses.indexOf(selectedStatus),
                edgePadding = 8.dp
            ) {
                statuses.forEach { status ->
                    Tab(
                        selected = selectedStatus == status,
                        onClick = { viewModel.setSelectedStatus(status) },
                        text = { Text(status.replaceFirstChar { it.uppercaseChar() }) }
                    )
                }
            }

            val filtered = viewModel.getFilteredBookings()

            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(8.dp)
            ) {
                items(filtered) { booking ->
                    BookingCard(
                        booking = booking,
                        onCancelSuccess = {
                            val token = session.getToken()
                            if (!token.isNullOrBlank()) {
                                viewModel.loadBookings(token)
                            }
                            Toast.makeText(context, it, Toast.LENGTH_LONG).show()
                        }
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                }
            }
        }
    }
}

@Composable
fun BookingCard(
    booking: BookingUiModel,
    onCancelSuccess: (String) -> Unit
) {
    val context = LocalContext.current
    val session = remember { SessionManager(context) }
    val scope = rememberCoroutineScope()

    val nights = if (!booking.checkIn.isNullOrBlank() && !booking.checkOut.isNullOrBlank()) {
        calculateNights(booking.checkIn, booking.checkOut)
    } else 1

    var isCancelling by remember { mutableStateOf(false) }

    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 3.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {

            booking.coverImageUrl?.let { imageUrl ->
                Image(
                    painter = rememberAsyncImagePainter(imageUrl),
                    contentDescription = null,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(160.dp)
                        .clip(RoundedCornerShape(10.dp))
                )
                Spacer(modifier = Modifier.height(8.dp))
            }

            Text(booking.hotelName, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
            Text("${booking.address}, ${booking.city}, ${booking.country}", style = MaterialTheme.typography.bodySmall)

            Spacer(modifier = Modifier.height(6.dp))

            Text("📅 Booking Date: ${booking.bookingDate}", style = MaterialTheme.typography.bodySmall)
            Text("✅ Check-in: ${booking.checkIn}", style = MaterialTheme.typography.bodySmall)
            Text("🚪 Check-out: ${booking.checkOut}", style = MaterialTheme.typography.bodySmall)
            Text("🛏️ $nights night${if (nights > 1) "s" else ""} | 💲 ${booking.totalPrice}", style = MaterialTheme.typography.bodySmall)

            booking.cancellationPolicy?.let {
                Text("🛡️ Policy: $it", style = MaterialTheme.typography.bodySmall)
            }

            Text("🔖 Status: ${booking.status.replaceFirstChar { it.uppercaseChar() }}", color = MaterialTheme.colorScheme.primary)

            // Cancel button for eligible statuses
            if (booking.status.lowercase() in listOf("pending", "confirmed")) {
                Spacer(modifier = Modifier.height(10.dp))
                Button(
                    onClick = {
                        scope.launch {
                            isCancelling = true
                            try {
                                val token = session.getToken()
                                val response = com.nasti.frontend.data.api.RetrofitClient.api.cancelBooking(
                                    token = "Bearer $token",
                                    bookingId = booking.id
                                )
                                if (response.isSuccessful) {
                                    val msg = if (booking.cancellationPolicy.equals("Flexible", ignoreCase = true)) {
                                        val halfRefund = booking.totalPrice?.replace("$", "")?.toDoubleOrNull()?.div(2)
                                        "✅ Booking cancelled. You'll be refunded $${"%.2f".format(halfRefund)}. This is the hotel's policy."
                                    } else {
                                        "⚠️ Booking cancelled. This booking is non-refundable. This is the hotel's policy."
                                    }
                                    onCancelSuccess(msg)
                                } else {
                                    onCancelSuccess("❌ Cancellation failed. Please try again.")
                                }
                            } catch (e: Exception) {
                                onCancelSuccess("❌ Error: ${e.localizedMessage}")
                            } finally {
                                isCancelling = false
                            }
                        }
                    },
                    enabled = !isCancelling
                ) {
                    Text("Cancel")
                }
            }
        }
    }
}
