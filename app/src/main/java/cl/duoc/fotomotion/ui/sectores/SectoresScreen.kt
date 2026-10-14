package cl.duoc.fotomotion.ui.sectores

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import cl.duoc.fotomotion.domain.model.PerfilUsuario
import cl.duoc.fotomotion.domain.model.Usuario

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SectoresScreen(viewModel: SectoresCultivosViewModel, usuarioLogueado: Usuario?) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val esAdmin = usuarioLogueado?.perfil == PerfilUsuario.ADMINISTRADOR

    Scaffold(topBar = { TopAppBar(title = { Text("Gestión de Sectores") }) }) { innerPadding ->
        Column(modifier = Modifier.fillMaxSize().padding(innerPadding).padding(16.dp)) {
            if (esAdmin) {
                Text("Crear Nuevo Sector", fontWeight = FontWeight.Bold)
                OutlinedTextField(value = uiState.nuevoNombreSector, onValueChange = { viewModel.cambiarNombreSector(it) }, label = { Text("Nombre Sector") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = uiState.nuevaUbicacionSector, onValueChange = { viewModel.cambiarUbicacionSector(it) }, label = { Text("Ubicación") }, modifier = Modifier.fillMaxWidth())
                Button(onClick = { viewModel.guardarSector() }, modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)) { Text("Guardar Sector") }
            }

            Text("Sectores Registrados", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
            LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                items(uiState.sectores) { sector ->
                    Card(modifier = Modifier.fillMaxWidth()) {
                        Column(modifier = Modifier.padding(12.dp)) {
                            Text(sector.nombre, fontWeight = FontWeight.Bold)
                            Text("Ubicación: ${sector.ubicacion}")
                        }
                    }
                }
            }
        }
    }
}
