package cl.duoc.fotomotion.ui.alertas

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AlertasSensoresScreen(viewModel: AlertasSensoresViewModel) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    Scaffold(topBar = { TopAppBar(title = { Text("Panel de Alertas y Sensores Simulados") }) }) { innerPadding ->
        Column(modifier = Modifier.fillMaxSize().padding(innerPadding).padding(16.dp)) {
            Text("Lecturas Simuladas de Prueba", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
            LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                items(uiState.lecturasSensores) { s ->
                    Card(colors = CardDefaults.cardColors(containerColor = Color(0xFFE0F7FA)), modifier = Modifier.fillMaxWidth()) {
                        Column(modifier = Modifier.padding(12.dp)) {
                            Text(s.sectorId, fontWeight = FontWeight.Bold)
                            Text("Origen: ${s.origenDato}", color = Color.Gray)
                            Text("Humedad Suelo Simulada: ${s.humedadSueloSimulada}% (${s.estadoLectura.name})")
                        }
                    }
                }
            }
        }
    }
}
