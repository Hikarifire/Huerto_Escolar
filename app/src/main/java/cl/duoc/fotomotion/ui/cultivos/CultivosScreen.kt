package cl.duoc.fotomotion.ui.cultivos

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
import cl.duoc.fotomotion.ui.sectores.SectoresCultivosViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CultivosScreen(viewModel: SectoresCultivosViewModel, usuarioLogueado: Usuario?) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val esAdmin = usuarioLogueado?.perfil == PerfilUsuario.ADMINISTRADOR

    Scaffold(topBar = { TopAppBar(title = { Text("Gestión de Cultivos") }) }) { innerPadding ->
        Column(modifier = Modifier.fillMaxSize().padding(innerPadding).padding(16.dp)) {
            if (esAdmin) {
                Text("Asociar Cultivo a Sector", fontWeight = FontWeight.Bold)
                OutlinedTextField(value = uiState.nuevoNombreCultivo, onValueChange = { viewModel.cambiarNombreCultivo(it) }, label = { Text("Nombre Cultivo") }, modifier = Modifier.fillMaxWidth())
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    uiState.sectores.forEach { s ->
                        FilterChip(selected = uiState.sectorSeleccionadoId == s.id, onClick = { viewModel.cambiarSectorSeleccionado(s.id) }, label = { Text(s.nombre) })
                    }
                }
                Button(onClick = { viewModel.guardarCultivo() }, modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)) { Text("Guardar Cultivo") }
            }

            Text("Cultivos en Desarrollo", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
            LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                items(uiState.cultivos) { cultivo ->
                    Card(modifier = Modifier.fillMaxWidth()) {
                        Column(modifier = Modifier.padding(12.dp)) {
                            Text(cultivo.nombreComun, fontWeight = FontWeight.Bold)
                            Text("Sector ID: ${cultivo.sectorId} | Estado: ${cultivo.estado}")
                        }
                    }
                }
            }
        }
    }
}
