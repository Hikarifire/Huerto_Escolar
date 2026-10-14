import os

files = {
    # Gradle y Configuración
    "gradle/libs.versions.toml": """[versions]
agp = "8.7.2"
kotlin = "2.0.21"
coreKtx = "1.15.0"
junit = "4.13.2"
junitVersion = "1.2.1"
espressoCore = "3.6.1"
lifecycleRuntimeKtx = "2.8.7"
activityCompose = "1.9.3"
composeBom = "2024.10.01"
room = "2.6.1"
ksp = "2.0.21-1.0.27"
coil = "3.3.0"
navigationCompose = "2.8.5"

[libraries]
androidx-core-ktx = { group = "androidx.core", name = "core-ktx", version.ref = "coreKtx" }
junit = { group = "junit", name = "junit", version.ref = "junit" }
androidx-junit = { group = "androidx.test.ext", name = "junit", version.ref = "junitVersion" }
androidx-espresso-core = { group = "androidx.test.espresso", name = "espresso-core", version.ref = "espressoCore" }
androidx-lifecycle-runtime-ktx = { group = "androidx.lifecycle", name = "lifecycle-runtime-ktx", version.ref = "lifecycleRuntimeKtx" }
androidx-activity-compose = { group = "androidx.activity", name = "activity-compose", version.ref = "activityCompose" }
androidx-compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "composeBom" }
androidx-ui = { group = "androidx.compose.ui", name = "ui" }
androidx-ui-graphics = { group = "androidx.compose.ui", name = "ui-graphics" }
androidx-ui-tooling = { group = "androidx.compose.ui", name = "ui-tooling" }
androidx-ui-tooling-preview = { group = "androidx.compose.ui", name = "ui-tooling-preview" }
androidx-material3 = { group = "androidx.compose.material3", name = "material3" }
androidx-room-runtime = { module = "androidx.room:room-runtime", version.ref = "room" }
androidx-room-compiler = { module = "androidx.room:room-compiler", version.ref = "room" }
androidx-room-ktx = { module = "androidx.room:room-ktx", version.ref = "room" }
coil-compose = { module = "io.coil-kt.coil3:coil-compose", version.ref = "coil" }
androidx-navigation-compose = { group = "androidx.navigation", name = "navigation-compose", version.ref = "navigationCompose" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
kotlin-compose = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
""",

    "build.gradle.kts": """// Top-level build file
plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.kotlin.android) apply false
    alias(libs.plugins.kotlin.compose) apply false
    alias(libs.plugins.ksp) apply false
}
""",

    "app/build.gradle.kts": """plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.ksp)
}

android {
    namespace = "cl.duoc.fotomotion"
    compileSdk = 35

    defaultConfig {
        applicationId = "cl.duoc.fotomotion"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    kotlinOptions {
        jvmTarget = "11"
    }
    buildFeatures {
        compose = true
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.activity.compose)
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.ui)
    implementation(libs.androidx.ui.graphics)
    implementation(libs.androidx.ui.tooling.preview)
    implementation(libs.androidx.material3)
    
    // Room Database
    implementation(libs.androidx.room.runtime)
    implementation(libs.androidx.room.ktx)
    ksp(libs.androidx.room.compiler)

    // Coil & Navigation
    implementation(libs.coil.compose)
    implementation(libs.androidx.navigation.compose)

    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    debugImplementation(libs.androidx.ui.tooling)
}
""",

    "app/src/main/AndroidManifest.xml": """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="Huerto Escolar"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.Material3.DayNight.NoActionBar">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.Material3.DayNight.NoActionBar">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="${applicationId}.fileprovider"
            android:exported="false"
            android:grantUriPermissions="true">
            <meta-data
                android:name="android.support.FILE_PROVIDER_PATHS"
                android:resource="@xml/file_paths" />
        </provider>

    </application>

</manifest>
""",

    "app/src/main/res/xml/file_paths.xml": """<?xml version="1.0" encoding="utf-8"?>
<paths xmlns:android="http://schemas.android.com/apk/res/android">
    <cache-path
        name="fotos"
        path="fotos/" />
</paths>
""",

    # Domain Models (Paso 1)
    "app/src/main/java/cl/duoc/fotomotion/domain/model/Modelos.kt": """package cl.duoc.fotomotion.domain.model

enum class PerfilUsuario { ADMINISTRADOR, ESTUDIANTE }
enum class EstadoLectura { NORMAL, ALTO, BAJO }

data class Usuario(
    val id: String,
    val nombreFicticio: String,
    val perfil: PerfilUsuario,
    val tallerAsignado: String,
    val funcionesAutorizadas: List<String>,
    val estadoCuenta: Boolean
)

data class LecturaSensor(
    val id: String,
    val sectorId: String,
    val fechaHoraLectura: String,
    val humedadSueloSimulada: Double,
    val temperaturaAmbientalSimulada: Double,
    val humedadAmbientalSimulada: Double,
    val origenDato: String = "simulación académica",
    val estadoLectura: EstadoLectura
)
""",

    # Entities (Paso 2)
    "app/src/main/java/cl/duoc/fotomotion/model/Entidades.kt": """package cl.duoc.fotomotion.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "sectores")
data class SectorEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val nombre: String,
    val descripcion: String,
    val ubicacion: String,
    val estado: String,
    val responsableId: String,
    val fechaCreacion: String,
    val fechaActualizacion: String
)

@Entity(tableName = "cultivos")
data class CultivoEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val nombreComun: String,
    val descripcion: String,
    val sectorId: Int,
    val fechaSiembra: String?,
    val fechaTrasplante: String?,
    val fechaEstimadaCosecha: String?,
    val frecuenciaRiegoDias: Int,
    val estado: String,
    val observaciones: String,
    val fotografiaReferencialFicticia: String?
)

@Entity(tableName = "tareas")
data class TareaEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val tipo: String,
    val descripcion: String,
    val sectorId: Int,
    val cultivoId: Int?,
    val fechaCreacion: String,
    val fechaProgramada: String,
    val responsableId: String,
    val creadorId: String,
    val estado: String,
    val fechaHoraRealizacion: String?,
    val fotografiaAdjunta: String?,
    val comentarioEstudiante: String?,
    val comentarioDocente: String?,
    val validadorId: String?,
    val fechaHoraValidacion: String?
)
""",

    # DAOs & Database (Paso 2)
    "app/src/main/java/cl/duoc/fotomotion/data/Daos.kt": """package cl.duoc.fotomotion.data

import androidx.room.*
import cl.duoc.fotomotion.model.*
import kotlinx.coroutines.flow.Flow

@Dao
interface SectorDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE) suspend fun insertar(sector: SectorEntity)
    @Query("SELECT * FROM sectores ORDER BY id DESC") fun obtenerSectores(): Flow<List<SectorEntity>>
}

@Dao
interface CultivoDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE) suspend fun insertar(cultivo: CultivoEntity)
    @Query("SELECT * FROM cultivos ORDER BY id DESC") fun obtenerTodosLosCultivos(): Flow<List<CultivoEntity>>
}

@Dao
interface TareaDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE) suspend fun insertar(tarea: TareaEntity)
    @Update suspend fun actualizar(tarea: TareaEntity)
    @Query("SELECT * FROM tareas ORDER BY id DESC") fun obtenerTodasLasTareas(): Flow<List<TareaEntity>>
}
""",

    "app/src/main/java/cl/duoc/fotomotion/data/AppDatabase.kt": """package cl.duoc.fotomotion.data

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import cl.duoc.fotomotion.model.*

@Database(entities = [SectorEntity::class, CultivoEntity::class, TareaEntity::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun sectorDao(): SectorDao
    abstract fun cultivoDao(): CultivoDao
    abstract fun tareaDao(): TareaDao

    companion object {
        @Volatile private var INSTANCE: AppDatabase? = null
        fun getInstance(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                Room.databaseBuilder(context.applicationContext, AppDatabase::class.java, "huerto_db.db")
                    .fallbackToDestructiveMigration()
                    .build().also { INSTANCE = it }
            }
        }
    }
}
""",

    "app/src/main/java/cl/duoc/fotomotion/data/HuertoRepository.kt": """package cl.duoc.fotomotion.data

import cl.duoc.fotomotion.model.*
import kotlinx.coroutines.flow.Flow

class HuertoRepository(
    private val sectorDao: SectorDao,
    private val cultivoDao: CultivoDao,
    private val tareaDao: TareaDao
) {
    fun obtenerSectores(): Flow<List<SectorEntity>> = sectorDao.obtenerSectores()
    suspend fun guardarSector(sector: SectorEntity) = sectorDao.insertar(sector)

    fun obtenerCultivos(): Flow<List<CultivoEntity>> = cultivoDao.obtenerTodosLosCultivos()
    suspend fun guardarCultivo(cultivo: CultivoEntity) = cultivoDao.insertar(cultivo)

    fun obtenerTodasLasTareas(): Flow<List<TareaEntity>> = tareaDao.obtenerTodasLasTareas()
    suspend fun guardarTarea(tarea: TareaEntity) = tareaDao.insertar(tarea)
    suspend fun actualizarTarea(tarea: TareaEntity) = tareaDao.actualizar(tarea)
}
""",

    # CamaraUtils (Paso 5)
    "app/src/main/java/cl/duoc/fotomotion/util/CamaraUtils.kt": """package cl.duoc.fotomotion.util

import android.content.Context
import android.net.Uri
import androidx.core.content.FileProvider
import java.io.File

fun crearUriFotografia(context: Context): Uri {
    val carpeta = File(context.cacheDir, "fotos")
    carpeta.mkdirs()
    val archivo = File.createTempFile("evidencia_", ".jpg", carpeta)
    return FileProvider.getUriForFile(
        context,
        "${context.packageName}.fileprovider",
        archivo
    )
}
""",

    # Auth UI (Paso 3)
    "app/src/main/java/cl/duoc/fotomotion/ui/auth/AuthUiState.kt": """package cl.duoc.fotomotion.ui.auth

import cl.duoc.fotomotion.domain.model.PerfilUsuario
import cl.duoc.fotomotion.domain.model.Usuario

data class AuthUiState(
    val usuarioLogueado: Usuario? = null,
    val usuariosFicticiosPrueba: List<Usuario> = listOf(
        Usuario("USR-001", "Profesor Carlos Silva", PerfilUsuario.ADMINISTRADOR, "Taller de Ecología", listOf("TODAS"), true),
        Usuario("USR-002", "Estudiante Mateo Rojas", PerfilUsuario.ESTUDIANTE, "Taller de Ecología", listOf("CONSULTAR"), true)
    )
)
""",

    "app/src/main/java/cl/duoc/fotomotion/ui/auth/AuthViewModel.kt": """package cl.duoc.fotomotion.ui.auth

import androidx.lifecycle.ViewModel
import cl.duoc.fotomotion.domain.model.Usuario
import kotlinx.coroutines.flow.*

class AuthViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(AuthUiState())
    val uiState: StateFlow<AuthUiState> = _uiState.asStateFlow()

    fun seleccionarUsuario(usuario: Usuario) { _uiState.update { it.copy(usuarioLogueado = usuario) } }
    fun cerrarSesion() { _uiState.update { it.copy(usuarioLogueado = null) } }
}
""",

    "app/src/main/java/cl/duoc/fotomotion/ui/auth/LoginScreen.kt": """package cl.duoc.fotomotion.ui.auth

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
""",

    # Sectores y Cultivos UI (Paso 4)
    "app/src/main/java/cl/duoc/fotomotion/ui/sectores/SectoresCultivosUiState.kt": """package cl.duoc.fotomotion.ui.sectores

import cl.duoc.fotomotion.model.CultivoEntity
import cl.duoc.fotomotion.model.SectorEntity

data class SectoresCultivosUiState(
    val sectores: List<SectorEntity> = emptyList(),
    val cultivos: List<CultivoEntity> = emptyList(),
    val nuevoNombreSector: String = "",
    val nuevaUbicacionSector: String = "",
    val nuevoNombreCultivo: String = "",
    val sectorSeleccionadoId: Int? = null
)
""",

    "app/src/main/java/cl/duoc/fotomotion/ui/sectores/SectoresCultivosViewModel.kt": """package cl.duoc.fotomotion.ui.sectores

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import cl.duoc.fotomotion.data.*
import cl.duoc.fotomotion.model.*
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

class SectoresCultivosViewModel(application: Application) : AndroidViewModel(application) {
    private val db = AppDatabase.getInstance(application)
    private val repo = HuertoRepository(db.sectorDao(), db.cultivoDao(), db.tareaDao())

    private val _uiState = MutableStateFlow(SectoresCultivosUiState())
    val uiState: StateFlow<SectoresCultivosUiState> = _uiState.asStateFlow()

    init {
        viewModelScope.launch { repo.obtenerSectores().collect { s -> _uiState.update { it.copy(sectores = s) } } }
        viewModelScope.launch { repo.obtenerCultivos().collect { c -> _uiState.update { it.copy(cultivos = c) } } }
    }

    fun cambiarNombreSector(v: String) { _uiState.update { it.copy(nuevoNombreSector = v) } }
    fun cambiarUbicacionSector(v: String) { _uiState.update { it.copy(nuevaUbicacionSector = v) } }

    fun guardarSector() {
        val st = _uiState.value
        if (st.nuevoNombreSector.isBlank()) return
        viewModelScope.launch {
            repo.guardarSector(SectorEntity(nombre = st.nuevoNombreSector, descripcion = "", ubicacion = st.nuevaUbicacionSector, estado = "EN_USO", responsableId = "DOC-001", fechaCreacion = "2026-10-14", fechaActualizacion = "2026-10-14"))
            _uiState.update { it.copy(nuevoNombreSector = "", nuevaUbicacionSector = "") }
        }
    }

    fun cambiarNombreCultivo(v: String) { _uiState.update { it.copy(nuevoNombreCultivo = v) } }
    fun cambiarSectorSeleccionado(id: Int) { _uiState.update { it.copy(sectorSeleccionadoId = id) } }

    fun guardarCultivo() {
        val st = _uiState.value
        if (st.nuevoNombreCultivo.isBlank() || st.sectorSeleccionadoId == null) return
        viewModelScope.launch {
            repo.guardarCultivo(CultivoEntity(nombreComun = st.nuevoNombreCultivo, descripcion = "", sectorId = st.sectorSeleccionadoId!!, fechaSiembra = "2026-10-14", fechaTrasplante = null, fechaEstimadaCosecha = "2026-12-01", frecuenciaRiegoDias = 1, estado = "SEMBRADO", observaciones = "", fotografiaReferencialFicticia = null))
            _uiState.update { it.copy(nuevoNombreCultivo = "", sectorSeleccionadoId = null) }
        }
    }
}
""",

    "app/src/main/java/cl/duoc/fotomotion/ui/sectores/SectoresScreen.kt": """package cl.duoc.fotomotion.ui.sectores

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
""",

    "app/src/main/java/cl/duoc/fotomotion/ui/cultivos/CultivosScreen.kt": """package cl.duoc.fotomotion.ui.cultivos

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
""",

    # Tareas UI (Paso 5)
    "app/src/main/java/cl/duoc/fotomotion/ui/tareas/TareasUiState.kt": """package cl.duoc.fotomotion.ui.tareas

import android.net.Uri
import cl.duoc.fotomotion.model.TareaEntity

data class TareasUiState(
    val tareas: List<TareaEntity> = emptyList(),
    val tareaEnEjecucion: TareaEntity? = null,
    val imagenEvidenciaUri: Uri? = null,
    val comentarioEstudiante: String = ""
)
""",

    "app/src/main/java/cl/duoc/fotomotion/ui/tareas/TareasViewModel.kt": """package cl.duoc.fotomotion.ui.tareas

import android.app.Application
import android.net.Uri
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import cl.duoc.fotomotion.data.*
import cl.duoc.fotomotion.model.TareaEntity
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

class TareasViewModel(application: Application) : AndroidViewModel(application) {
    private val db = AppDatabase.getInstance(application)
    private val repo = HuertoRepository(db.sectorDao(), db.cultivoDao(), db.tareaDao())

    private val _uiState = MutableStateFlow(TareasUiState())
    val uiState: StateFlow<TareasUiState> = _uiState.asStateFlow()

    init {
        viewModelScope.launch { repo.obtenerTodasLasTareas().collect { t -> _uiState.update { it.copy(tareas = t) } } }
    }

    fun seleccionarTarea(t: TareaEntity) { _uiState.update { it.copy(tareaEnEjecucion = t) } }
    fun setUri(uri: Uri?) { _uiState.update { it.copy(imagenEvidenciaUri = uri) } }

    fun enviarTarea() {
        val t = _uiState.value.tareaEnEjecucion ?: return
        viewModelScope.launch {
            repo.actualizarTarea(t.copy(estado = "PENDIENTE_DE_VALIDACION", fechaHoraRealizacion = "2026-10-14 14:00", fotografiaAdjunta = _uiState.value.imagenEvidenciaUri?.toString()))
            _uiState.update { it.copy(tareaEnEjecucion = null, imagenEvidenciaUri = null) }
        }
    }

    fun validar(t: TareaEntity, aprobada: Boolean) {
        viewModelScope.launch {
            repo.actualizarTarea(t.copy(estado = if (aprobada) "VALIDADA" else "RECHAZADA", fechaHoraValidacion = "2026-10-14 14:30"))
        }
    }
}
""",

    "app/src/main/java/cl/duoc/fotomotion/ui/tareas/TareasScreen.kt": """package cl.duoc.fotomotion.ui.tareas

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
""",

    # Alertas UI (Paso 6)
    "app/src/main/java/cl/duoc/fotomotion/ui/alertas/AlertasSensoresUiState.kt": """package cl.duoc.fotomotion.ui.alertas

import cl.duoc.fotomotion.domain.model.LecturaSensor
import cl.duoc.fotomotion.model.TareaEntity

data class AlertasSensoresUiState(
    val lecturasSensores: List<LecturaSensor> = emptyList(),
    val historial: List<TareaEntity> = emptyList()
)
""",

    "app/src/main/java/cl/duoc/fotomotion/ui/alertas/AlertasSensoresViewModel.kt": """package cl.duoc.fotomotion.ui.alertas

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import cl.duoc.fotomotion.data.*
import cl.duoc.fotomotion.domain.model.EstadoLectura
import cl.duoc.fotomotion.domain.model.LecturaSensor
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

class AlertasSensoresViewModel(application: Application) : AndroidViewModel(application) {
    private val db = AppDatabase.getInstance(application)
    private val repo = HuertoRepository(db.sectorDao(), db.cultivoDao(), db.tareaDao())

    private val _uiState = MutableStateFlow(AlertasSensoresUiState())
    val uiState: StateFlow<AlertasSensoresUiState> = _uiState.asStateFlow()

    init {
        viewModelScope.launch {
            repo.obtenerTodasLasTareas().collect { t -> _uiState.update { it.copy(historial = t) } }
        }
        _uiState.update {
            it.copy(
                lecturasSensores = listOf(
                    LecturaSensor("SENS-01", "Sector A1 (Invernadero)", "2026-10-14 10:00", 22.0, 25.5, 50.0, "simulación académica", EstadoLectura.BAJO),
                    LecturaSensor("SENS-02", "Sector B2 (Exterior)", "2026-10-14 10:00", 65.0, 22.0, 62.0, "simulación académica", EstadoLectura.NORMAL)
                )
            )
        }
    }
}
""",

    "app/src/main/java/cl/duoc/fotomotion/ui/alertas/AlertasSensoresScreen.kt": """package cl.duoc.fotomotion.ui.alertas

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
""",

    # Navigation (Paso 3)
    "app/src/main/java/cl/duoc/fotomotion/ui/navigation/Navegacion.kt": """package cl.duoc.fotomotion.ui.navigation

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
""",

    # MainActivity
    "app/src/main/java/cl/duoc/fotomotion/MainActivity.kt": """package cl.duoc.fotomotion

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.material3.MaterialTheme
import cl.duoc.fotomotion.ui.auth.AuthViewModel
import cl.duoc.fotomotion.ui.navigation.AppNavegacion

class MainActivity : ComponentActivity() {
    private val authViewModel: AuthViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MaterialTheme {
                AppNavegacion(authViewModel = authViewModel)
            }
        }
    }
}
"""
}

def create_project():
    print("Iniciando la creación del proyecto Huerto Escolar...")
    for path, content in files.items():
        folder = os.path.dirname(path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Creado: {path}")
    print("\n¡Proyecto generado exitosamente!")
    print("Abre esta carpeta en Android Studio, deja que cargue Gradle y ejecuta la app.")

if __name__ == "__main__":
    create_project()