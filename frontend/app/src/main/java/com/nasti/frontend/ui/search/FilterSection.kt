package com.nasti.frontend.ui.search

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun FilterSection(
    viewModel: SearchViewModel,
    onApply: () -> Unit // <-- new callback
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text("Filter by facilities", style = MaterialTheme.typography.titleSmall)

        FilterCheckbox("Has Wi-Fi", viewModel.hasWifi ?: false) {
            viewModel.hasWifi = it
        }

        FilterCheckbox("Allows Pets", viewModel.allowsPets ?: false) {
            viewModel.allowsPets = it
        }

        FilterCheckbox("Has Kitchen", viewModel.hasKitchen ?: false) {
            viewModel.hasKitchen = it
        }

        FilterCheckbox("Has Air Conditioning", viewModel.hasAirConditioning ?: false) {
            viewModel.hasAirConditioning = it
        }

        FilterCheckbox("Has TV", viewModel.hasTv ?: false) {
            viewModel.hasTv = it
        }

        FilterCheckbox("Has Safe", viewModel.hasSafe ?: false) {
            viewModel.hasSafe = it
        }

        FilterCheckbox("Has Balcony", viewModel.hasBalcony ?: false) {
            viewModel.hasBalcony = it
        }

        Text("Minimum Stars", style = MaterialTheme.typography.titleSmall)

        var starsInput by remember { mutableStateOf(viewModel.minStars?.toString() ?: "") }
        OutlinedTextField(
            value = starsInput,
            onValueChange = {
                starsInput = it
                viewModel.minStars = it.toIntOrNull()
            },
            modifier = Modifier.fillMaxWidth(),
            label = { Text("1 - 5") }
        )

        Button(
            onClick = {
                viewModel.triggerSearch()
                onApply() // <-- hide filter panel
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Apply Filters")
        }
    }
}

@Composable
private fun FilterCheckbox(label: String, checked: Boolean, onCheckedChange: (Boolean) -> Unit) {
    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
        Text(label)
        Switch(checked = checked, onCheckedChange = onCheckedChange)
    }
}