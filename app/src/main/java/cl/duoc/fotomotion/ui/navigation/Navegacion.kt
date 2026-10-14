package cl.duoc.fotomotion.ui.navigation

import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Build
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.List
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.*
import cl.duoc.fotomotion.ui.alertas.*
import cl.duoc.fotomotion.ui.auth.*
import cl.duoc.fotomotion.ui.cultivos.CultivosScreen
import cl.duoc.fotomotion.ui.sectores.*
import cl.duoc.fotomotion.ui.tareas.*

sealed class Destino(val ruta: String, val titulo: String, val icono: androidx.compose.ui.graphics.vector.ImageVector) {
    object Login : Destino("login", "Inicio", Icons.Default.Home)
    object Sectores : Destino("sectores", "Sectores", Icons.Default.Home)
    object Cultivos : Destino("cultivos", "Cultivos", Icons.Default.List)
    object Tareas : Destino("tareas", "Tareas", Icons.Default.Build)
    object Alertas : Destino("alertas", "Alertas", Icons.Default.Warning)
}

@Composable
fun AppNavegacion(authViewModel: AuthViewModel) {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val rutaActual = navBackStackEntry?.destination?.route

    val authState by authViewModel.uiState.collectAsStateWithLifecycle()
    val usuario = authState.usuarioLogueado

    val sectoresVM: SectoresCultivosViewModel = viewModel()
    val tareasVM: TareasViewModel = viewModel()
    val alertasVM: AlertasSensoresViewModel = viewModel()

    val items = listOf(Destino.Sectores, Destino.Cultivos, Destino.Tareas, Destino.Alertas)

    Scaffold(
        bottomBar = {
            if (usuario != null && rutaActual != Destino.Login.ruta) {
                NavigationBar {
                    items.forEach { d ->
                        NavigationBarItem(
                            icon = { Icon(d.icono, contentDescription = d.titulo) },
                            label = { Text(d.titulo) },
                            selected = rutaActual == d.ruta,
                            onClick = { navController.navigate(d.ruta) }
                        )
                    }
                }
            }
        }
    ) { innerPadding ->
        NavHost(navController = navController, startDestination = Destino.Login.ruta, modifier = Modifier.padding(innerPadding)) {
            composable(Destino.Login.ruta) {
                LoginScreen(authViewModel = authViewModel, onLoginExitoso = {
                    navController.navigate(Destino.Tareas.ruta)
                })
            }
            composable(Destino.Sectores.ruta) { SectoresScreen(viewModel = sectoresVM, usuarioLogueado = usuario) }
            composable(Destino.Cultivos.ruta) { CultivosScreen(viewModel = sectoresVM, usuarioLogueado = usuario) }
            composable(Destino.Tareas.ruta) { TareasScreen(viewModel = tareasVM, usuarioLogueado = usuario) }
            composable(Destino.Alertas.ruta) { AlertasSensoresScreen(viewModel = alertasVM) }
        }
    }
}
