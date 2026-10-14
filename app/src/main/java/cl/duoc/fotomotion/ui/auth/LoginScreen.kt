package cl.duoc.fotomotion.ui.auth

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import cl.duoc.fotomotion.domain.model.PerfilUsuario
import cl.duoc.fotomotion.domain.model.Usuario

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LoginScreen(authViewModel: AuthViewModel, onLoginExitoso: (Usuario) -> Unit) {
    val uiState by authViewModel.uiState.collectAsStateWithLifecycle()

    Scaffold(topBar = { TopAppBar(title = { Text("Huerto Escolar - Selección de Perfil") }) }) { innerPadding ->
        Column(modifier = Modifier.fillMaxSize().padding(innerPadding).padding(16.dp)) {
            Text("Seleccione una cuenta ficticia para ingresar:", style = MaterialTheme.typography.titleMedium)
            Spacer(modifier = Modifier.height(16.dp))
            LazyColumn(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                items(uiState.usuariosFicticiosPrueba) { usuario ->
                    Card(
                        colors = CardDefaults.cardColors(
                            containerColor = if (usuario.perfil == PerfilUsuario.ADMINISTRADOR) Color(0xFFE3F2FD) else Color(0xFFE8F5E9)
                        ),
                        modifier = Modifier.fillMaxWidth().clickable {
                            authViewModel.seleccionarUsuario(usuario)
                            onLoginExitoso(usuario)
                        }
                    ) {
                        Row(modifier = Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text(usuario.nombreFicticio, fontWeight = FontWeight.Bold)
                                Text("Rol: ${usuario.perfil.name}")
                            }
                            Button(onClick = {
                                authViewModel.seleccionarUsuario(usuario)
                                onLoginExitoso(usuario)
                            }) { Text("Ingresar") }
                        }
                    }
                }
            }
        }
    }
}
