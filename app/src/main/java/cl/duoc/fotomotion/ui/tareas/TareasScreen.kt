package cl.duoc.fotomotion.ui.tareas

import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import io.coil3.compose.AsyncImage
import cl.duoc.fotomotion.domain.model.PerfilUsuario
import cl.duoc.fotomotion.domain.model.Usuario
import cl.duoc.fotomotion.util.crearUriFotografia

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TareasScreen(viewModel: TareasViewModel, usuarioLogueado: Usuario?) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val esAdmin = usuarioLogueado?.perfil == PerfilUsuario.ADMINISTRADOR

    var uriCamara by remember { mutableStateOf<Uri?>(null) }
    val launcherCamara = rememberLauncherForActivityResult(ActivityResultContracts.TakePicture()) { ok ->
        if (ok) viewModel.setUri(uriCamara)
    }

    Scaffold(topBar = { TopAppBar(title = { Text("Gestión Colaborativa de Tareas") }) }) { innerPadding ->
        Column(modifier = Modifier.fillMaxSize().padding(innerPadding).padding(16.dp)) {
            if (uiState.tareaEnEjecucion != null) {
                Card(modifier = Modifier.fillMaxWidth()) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Ejecutando Tarea: ${uiState.tareaEnEjecucion?.descripcion}", fontWeight = FontWeight.Bold)
                        AnimatedVisibility(visible = uiState.imagenEvidenciaUri != null) {
                            uiState.imagenEvidenciaUri?.let {
                                AsyncImage(model = it, contentDescription = "Foto Evidencia", modifier = Modifier.fillMaxWidth().height(160.dp).clip(RoundedCornerShape(8.dp)), contentScale = ContentScale.Crop)
                            }
                        }
                        Button(onClick = {
                            val u = crearUriFotografia(context)
                            uriCamara = u
                            launcherCamara.launch(u)
                        }, modifier = Modifier.padding(vertical = 8.dp)) { Text("Capturar Evidencia (Cámara)") }
                        Button(onClick = { viewModel.enviarTarea() }, modifier = Modifier.fillMaxWidth()) { Text("Enviar Tarea Realizada") }
                    }
                }
            }

            Text("Listado de Tareas", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
            LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                items(uiState.tareas) { tarea ->
                    Card(modifier = Modifier.fillMaxWidth()) {
                        Column(modifier = Modifier.padding(12.dp)) {
                            Text("[${tarea.tipo}] ${tarea.descripcion}", fontWeight = FontWeight.Bold)
                            Text("Estado: ${tarea.estado}")
                            if (!tarea.fotografiaAdjunta.isNullOrBlank()) {
                                AsyncImage(model = tarea.fotografiaAdjunta, contentDescription = "Evidencia", modifier = Modifier.fillMaxWidth().height(120.dp).clip(RoundedCornerShape(8.dp)), contentScale = ContentScale.Crop)
                            }
                            if (!esAdmin && tarea.estado == "PENDIENTE") {
                                Button(onClick = { viewModel.seleccionarTarea(tarea) }) { Text("Realizar Tarea") }
                            }
                            if (esAdmin && tarea.estado == "PENDIENTE_DE_VALIDACION") {
                                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                    Button(onClick = { viewModel.validar(tarea, true) }) { Text("Aprobar") }
                                    Button(onClick = { viewModel.validar(tarea, false) }) { Text("Rechazar") }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
