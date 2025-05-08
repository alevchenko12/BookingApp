package com.nasti.frontend.ui.profile

import android.app.AlertDialog
import android.content.Context
import android.widget.Toast
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.nasti.frontend.data.api.RetrofitClient
import com.nasti.frontend.data.model.User
import com.nasti.frontend.data.model.UserUpdateRequest
import com.nasti.frontend.data.repository.UserRepository
import com.nasti.frontend.utils.SessionManager
import kotlinx.coroutines.launch
import kotlin.coroutines.resume
import kotlin.coroutines.suspendCoroutine

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun UserProfileScreen(navController: NavController) {
    val context = LocalContext.current
    val sessionManager = remember { SessionManager(context) }
    val token = sessionManager.getToken()
    val userRepository = remember {
        UserRepository(RetrofitClient.createWithAuth(token ?: ""))
    }
    val coroutineScope = rememberCoroutineScope()

    var user by remember { mutableStateOf<User?>(null) }
    var isEditing by remember { mutableStateOf(false) }
    var firstName by remember { mutableStateOf("") }
    var lastName by remember { mutableStateOf("") }
    var phone by remember { mutableStateOf("") }

    var firstNameError by remember { mutableStateOf<String?>(null) }
    var lastNameError by remember { mutableStateOf<String?>(null) }
    var phoneError by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(Unit) {
        coroutineScope.launch {
            try {
                user = userRepository.getProfile()
                user?.let {
                    firstName = it.first_name
                    lastName = it.last_name
                    phone = it.phone ?: ""
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Failed to load profile", Toast.LENGTH_SHORT).show()
            }
        }
    }

    fun validateInputs(): Boolean {
        var isValid = true

        if (firstName.isBlank() || firstName.any { it.isDigit() }) {
            firstNameError = "First name must contain only letters"
            isValid = false
        } else firstNameError = null

        if (lastName.isBlank() || lastName.any { it.isDigit() }) {
            lastNameError = "Last name must contain only letters"
            isValid = false
        } else lastNameError = null

        if (phone.isNotBlank()) {
            if (phone.length !in 7..15 || !phone.all { it.isDigit() }) {
                phoneError = "Phone must be 7–15 digits"
                isValid = false
            } else phoneError = null
        } else phoneError = null

        return isValid
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("My Profile") },
                actions = {
                    IconButton(onClick = { isEditing = !isEditing }) {
                        Icon(Icons.Default.Edit, contentDescription = "Edit")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .padding(padding)
                .padding(24.dp)
                .fillMaxSize(),
            verticalArrangement = Arrangement.Top,
            horizontalAlignment = Alignment.Start
        ) {
            if (user != null) {
                OutlinedTextField(
                    value = firstName,
                    onValueChange = { firstName = it },
                    label = { Text("First Name") },
                    modifier = Modifier.fillMaxWidth(),
                    enabled = isEditing,
                    isError = firstNameError != null
                )
                firstNameError?.let {
                    Text(it, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
                }

                Spacer(modifier = Modifier.height(8.dp))

                OutlinedTextField(
                    value = lastName,
                    onValueChange = { lastName = it },
                    label = { Text("Last Name") },
                    modifier = Modifier.fillMaxWidth(),
                    enabled = isEditing,
                    isError = lastNameError != null
                )
                lastNameError?.let {
                    Text(it, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
                }

                Spacer(modifier = Modifier.height(8.dp))

                OutlinedTextField(
                    value = phone,
                    onValueChange = { phone = it },
                    label = { Text("Phone") },
                    modifier = Modifier.fillMaxWidth(),
                    enabled = isEditing,
                    isError = phoneError != null
                )
                phoneError?.let {
                    Text(it, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
                }

                if (isEditing) {
                    Spacer(modifier = Modifier.height(12.dp))
                    Button(onClick = {
                        if (validateInputs()) {
                            coroutineScope.launch {
                                try {
                                    userRepository.updateProfile(
                                        UserUpdateRequest(
                                            first_name = firstName,
                                            last_name = lastName,
                                            phone = phone.ifBlank { null }
                                        )
                                    )
                                    Toast.makeText(context, "Profile updated", Toast.LENGTH_SHORT).show()
                                    isEditing = false
                                } catch (e: Exception) {
                                    Toast.makeText(context, "Update failed", Toast.LENGTH_SHORT).show()
                                }
                            }
                        }
                    }) {
                        Text("Save Changes")
                    }
                }

                Spacer(modifier = Modifier.height(24.dp))
                Divider()
                Spacer(modifier = Modifier.height(8.dp))

                Text("Danger Zone", color = MaterialTheme.colorScheme.error)
                Button(
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error),
                    onClick = {
                        coroutineScope.launch {
                            try {
                                userRepository.deleteAccount()
                                sessionManager.clearSession()
                                navController.navigate("auth") {
                                    popUpTo("profile") { inclusive = true }
                                }
                            } catch (e: Exception) {
                                Toast.makeText(context, "Failed to delete account", Toast.LENGTH_SHORT).show()
                            }
                        }
                    }
                ) {
                    Icon(Icons.Default.Delete, contentDescription = "Delete")
                    Spacer(Modifier.width(8.dp))
                    Text("Delete Account")
                }

                Spacer(modifier = Modifier.height(32.dp))

                Button(
                    onClick = {
                        coroutineScope.launch {
                            val confirmed = showLogoutConfirmation(context)
                            if (confirmed) {
                                sessionManager.clearSession()
                                navController.navigate("auth") {
                                    popUpTo("profile") { inclusive = true }
                                }
                            }
                        }
                    },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Logout")
                }

                Spacer(modifier = Modifier.height(16.dp))

                Button(
                    onClick = {
                        navController.navigate("forgot")
                    },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Change Password")
                }
            }
        }
    }
}

suspend fun showLogoutConfirmation(context: Context): Boolean {
    return suspendCoroutine { continuation ->
        val alertDialog = AlertDialog.Builder(context)
            .setTitle("Logout")
            .setMessage("Are you sure you want to log out?")
            .setPositiveButton("Yes") { _, _ -> continuation.resume(true) }
            .setNegativeButton("No") { _, _ -> continuation.resume(false) }
            .setCancelable(true)
            .create()

        alertDialog.show()
    }
}
