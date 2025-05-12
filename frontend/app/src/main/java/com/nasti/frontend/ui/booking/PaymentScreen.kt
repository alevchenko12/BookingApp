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

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PaymentScreen(
    navController: NavController,
    bookingId: Int,
    method: String // Expecting "Card" or "GooglePay"
) {
    val context = LocalContext.current
    val session = remember { SessionManager(context) }
    val scope = rememberCoroutineScope()
    val today = remember { SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date()) }

    var amount by remember { mutableStateOf(TextFieldValue("")) }
    var isSubmitting by remember { mutableStateOf(false) }
    var message by remember { mutableStateOf<String?>(null) }

    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Payment: $method") })
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .padding(padding)
                .padding(16.dp)
                .fillMaxSize(),
            verticalArrangement = Arrangement.Top
        ) {
            Text("Booking ID: $bookingId")
            Text("Payment Method: $method")
            Spacer(modifier = Modifier.height(16.dp))

            OutlinedTextField(
                value = amount,
                onValueChange = { amount = it },
                label = { Text("Amount (USD)") },
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(24.dp))

            Button(
                onClick = {
                    scope.launch {
                        val token = session.getToken()
                        val amountValue = amount.text.toDoubleOrNull()

                        if (amountValue == null || amountValue <= 0.0) {
                            message = "Please enter a valid amount"
                            return@launch
                        }

                        isSubmitting = true
                        message = null

                        try {
                            val paymentRequest = PaymentCreateRequest(
                                booking_id = bookingId,
                                payment_date = today,
                                payment_method = method,
                                amount = amountValue
                            )

                            val response = RetrofitClient.api.createPayment(
                                token = "Bearer $token",
                                request = paymentRequest
                            )

                            if (response.isSuccessful) {
                                message = "Payment successful!"
                                navController.navigate("profile")
                            } else {
                                message = "Payment failed: ${response.code()}"
                            }
                        } catch (e: Exception) {
                            message = "Error: ${e.localizedMessage}"
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
                Text(text = it, color = MaterialTheme.colorScheme.error)
            }
        }
    }
}
