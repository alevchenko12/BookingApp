package com.nasti.frontend.ui.booking

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.nasti.frontend.utils.SessionManager
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*
import com.nasti.frontend.data.api.RetrofitClient
import com.nasti.frontend.data.model.PaymentCreateRequest
import com.nasti.frontend.ui.search.SearchViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PaymentScreen(
    navController: NavController,
    bookingId: Int,
    method: String,
    searchViewModel: SearchViewModel
) {
    val context = LocalContext.current
    val session = remember { SessionManager(context) }
    val scope = rememberCoroutineScope()
    val today = remember { SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date()) }

    val nights = calculateNights(searchViewModel.checkIn, searchViewModel.checkOut)
    val totalAmount = remember { (searchViewModel.selectedRoomPrice * nights).coerceAtLeast(0.0) }

    var isSubmitting by remember { mutableStateOf(false) }
    var message by remember { mutableStateOf<String?>(null) }

    val validMethod = remember(method) {
        PaymentMethodEnum.values().firstOrNull { it.displayName.equals(method, ignoreCase = true) }?.displayName
            ?: "Card" 
    }

    Scaffold(
        topBar = { TopAppBar(title = { Text("Payment: $validMethod") }) }
    ) { padding ->
        Column(
            modifier = Modifier
                .padding(padding)
                .padding(16.dp)
                .fillMaxSize(),
            verticalArrangement = Arrangement.Top
        ) {
            Text("💳 Payment Method: $validMethod", style = MaterialTheme.typography.bodyLarge)
            Text("💰 Total Price: $${"%.2f".format(totalAmount)}", style = MaterialTheme.typography.bodyLarge)
            Spacer(modifier = Modifier.height(24.dp))

            OutlinedTextField(
                value = "%.2f".format(totalAmount),
                onValueChange = {},
                label = { Text("Amount (USD)") },
                modifier = Modifier.fillMaxWidth(),
                readOnly = true
            )

            Spacer(modifier = Modifier.height(24.dp))

            Button(
                onClick = {
                    scope.launch {
                        val token = session.getToken()

                        isSubmitting = true
                        message = null

                        try {
                            val paymentRequest = PaymentCreateRequest(
                                booking_id = bookingId,
                                payment_date = today,
                                payment_method = validMethod,
                                amount = totalAmount
                            )

                            val response = RetrofitClient.api.createPayment(
                                token = "Bearer $token",
                                request = paymentRequest
                            )

                            if (response.isSuccessful) {
                                message = "✅ Payment successful!"
                                navController.navigate("profile")
                            } else {
                                message = "❌ Payment failed: ${response.code()}"
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
                Text("Submit Payment")
            }

            message?.let {
                Spacer(modifier = Modifier.height(16.dp))
                Text(it, color = MaterialTheme.colorScheme.error)
            }
        }
    }
}
