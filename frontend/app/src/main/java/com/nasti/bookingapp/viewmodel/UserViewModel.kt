package com.nasti.bookingapp.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nasti.bookingapp.model.User
import com.nasti.bookingapp.repository.UserRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class UserViewModel : ViewModel() {
    private val repository = UserRepository()

    // Using MutableStateFlow instead of MutableLiveData
    private val _users = MutableStateFlow<List<User>>(emptyList())
    val users: StateFlow<List<User>> = _users.asStateFlow()

    fun loadUsers() {
        // Using println() to print when the loadUsers function is called
        println("UserViewModel: loadUsers() called")  // ✅ Check if ViewModel loads data
        viewModelScope.launch {
            val fetchedUsers = repository.fetchUsers()
            if (fetchedUsers != null) {
                // Print the fetched users to the terminal
                println("UserViewModel: Fetched users: $fetchedUsers")  // ✅ Check if data is received
                _users.value = fetchedUsers
            } else {
                // Print an error message if no users are fetched
                println("UserViewModel: Failed to fetch users")  // Error message in the terminal
            }
        }
    }
}
