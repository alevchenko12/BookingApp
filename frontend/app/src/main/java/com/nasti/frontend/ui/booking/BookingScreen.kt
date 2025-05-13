package com.nasti.frontend.ui.booking

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.nasti.frontend.ui.search.SearchViewModel
import com.nasti.frontend.utils.SessionManager
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*
import java.util.concurrent.TimeUnit

enum class PaymentMethodEnum(val displayName: String) {
    GooglePay("Google Pay"),
    Card("Card"),
    Cash("Cash")
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BookingScreen(
    navController: NavController,
    roomId: Int,
    searchViewModel: SearchViewModel
) {
    val context = LocalContext.current
    val session = remember { SessionManager(context) }
    val scope = rememberCoroutineScope()
    val dateFormat = remember { SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()) }

    val checkIn = searchViewModel.checkIn
    val checkOut = searchViewModel.checkOut
    val adults = searchViewModel.adults
    val rooms = searchViewModel.rooms
    val nights = calculateNights(checkIn, checkOut)
    val bookingDate = dateFormat.format(Date())
    val pricePerNight = searchViewModel.selectedRoomPrice
    val totalPrice = pricePerNight * nights


    var additionalInfo by remember { mutableStateOf(TextFieldValue("")) }
    var isSubmitting by remember { mutableStateOf(false) }
    var message by remember { mutableStateOf<String?>(null) }

    var showPaymentDialog by remember { mutableStateOf(false) }
    var latestBookingId by remember { mutableStateOf<Int?>(null) }



    Scaffold(
        topBar = { TopAppBar(title = { Text("Booking Summary") }) }
    ) { padding ->
        Column(
            modifier = Modifier
                .padding(padding)
                .padding(16.dp)
                .fillMaxSize(),
            verticalArrangement = Arrangement.Top
        ) {
            Text("📅 Check-In: $checkIn")
            Text("📅 Check-Out: $checkOut")
            Text("🛏️ $rooms room${if (rooms > 1) "s" else ""}, 👤 $adults adult${if (adults > 1) "s" else ""}")
            Text("🌙 $nights night${if (nights > 1) "s" else ""}")

            Spacer(modifier = Modifier.height(24.dp))

            OutlinedTextField(
                value = additionalInfo,
                onValueChange = { additionalInfo = it },
                label = { Text("Additional Info / Requests") },
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(24.dp))

            Button(
                onClick = {
                    scope.launch {
                        if (checkIn.isBlank() || checkOut.isBlank()) {
                            message = "❗ Please select check-in and check-out dates."
                            return@launch
                        }

                        isSubmitting = true
                        val token = session.getToken()

                        try {
                            val request = com.nasti.frontend.data.model.BookingCreateRequest(
                                room_id = roomId,
                                booking_date = bookingDate,
                                check_in_date = checkIn,
                                check_out_date = checkOut,
                                additional_info = additionalInfo.text.ifBlank { null }
                            )

                            val response = com.nasti.frontend.data.api.RetrofitClient.api.createBooking(
                                token = "Bearer $token",
                                request = request
                            )

                            if (response.isSuccessful) {
                                message = "✅ Booking successful!"
                                additionalInfo = TextFieldValue("")
                                latestBookingId = response.body()?.id // assuming response has booking ID
                                showPaymentDialog = true
                            } else {
                                message = "❌ Booking failed: ${response.code()}"
                            }
                        } catch (e: Exception) {
                            message = "⚠️ Error: ${e.localizedMessage}"
                        } finally {
                            isSubmitting = false
                        }
                    }
                },
                modifier = Modifier.fillMaxWidth(),
                enabled = !isSubmitting
            ) {
                Text("Confirm Booking")
            }

            message?.let {
                Spacer(modifier = Modifier.height(16.dp))
                Text(text = it, color = MaterialTheme.colorScheme.error)
            }

            if (showPaymentDialog && latestBookingId != null) {
                AlertDialog(
                    onDismissRequest = { showPaymentDialog = false },
                    title = { Text("Choose Payment Method") },
                    text = {
                        Column {
                            Text("How would you like to pay?")
                            Spacer(modifier = Modifier.height(12.dp))
                            PaymentMethodEnum.values().forEach { method ->
                                Button(
                                    onClick = {
                                        showPaymentDialog = false
                                        when (method) {
                                            PaymentMethodEnum.Cash -> navController.navigate("profile")
                                            else -> navController.navigate("paymentForm/${latestBookingId}/${method.displayName}")
                                        }
                                    },
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(vertical = 4.dp)
                                ) {
                                    Text(method.displayName)
                                }
                            }
                        }
                    },
                    confirmButton = {}
                )
            }
        }
    }
}

fun calculateNights(checkIn: String, checkOut: String): Int {
    return try {
        val sdf = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
        val start = sdf.parse(checkIn)
        val end = sdf.parse(checkOut)
        val diff = end.time - start.time
        TimeUnit.DAYS.convert(diff, TimeUnit.MILLISECONDS).toInt().coerceAtLeast(1)
    } catch (e: Exception) {
        1
    }
}
