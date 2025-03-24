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
        viewModelScope.launch {
            val fetchedUsers = repository.fetchUsers()
            if (fetchedUsers != null) {
                _users.value = fetchedUsers
            }
        }
    }
}

