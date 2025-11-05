<template>
  <div class="min-h-screen bg-gray-50 py-10 px-4">
    <!-- Header -->
    <header class="text-center mb-8">
      <h1 class="text-3xl font-bold text-green-700 mb-1">
        🌿 Air Quality Dashboard
      </h1>
      <p class="text-gray-500 text-sm">Stazioni di monitoraggio</p>
    </header>

    <!-- Stato caricamento -->
    <div v-if="loading" class="text-center text-gray-500 mt-8 text-sm">
      Caricamento stazioni...
    </div>
    <div v-if="error" class="text-center text-red-600 mt-8 text-sm">
      {{ error }}
    </div>

    <!-- Tabella stazioni -->
    <div v-if="stations.length" class="max-w-5xl mx-auto bg-white shadow-md rounded-lg overflow-hidden">
      <table class="min-w-full border-collapse">
        <thead class="bg-green-600 text-white text-sm uppercase">
          <tr>
            <th class="p-3 text-left w-2"></th>
            <th class="p-3 text-left">Nome</th>
            <th class="p-3 text-left">Sito</th>
            <th class="p-3 text-left">Indirizzo</th>
            <th class="p-3 text-center">Qualità aria</th>
            <th class="p-3 text-center">Azioni</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="station in stations"
            :key="station.id"
            class="border-b hover:bg-gray-50 transition"
          >
            <!-- Banda colore AQI -->
            <td :class="['w-2', getAirQualityColor(station.aqi)]"></td>

            <!-- Nome -->
            <td class="p-3 text-sm font-semibold text-gray-800">
              {{ station.name }}
            </td>

            <!-- Sito -->
            <td class="p-3 text-sm text-gray-600">{{ station.site }}</td>

            <!-- Indirizzo -->
            <td class="p-3 text-sm text-gray-500">{{ station.address }}</td>

            <!-- Stato AQI -->
            <td class="p-3 text-center">
              <span
                class="px-2 py-1 rounded-full text-xs font-medium"
                :class="getAQIBadge(station.aqi)"
              >
                {{ getAirQualityLabel(station.aqi) }}
              </span>
            </td>

            <!-- Pulsante dettagli -->
            <td class="p-3 text-center">
              <button
                @click="goToStation(station.id)"
                class="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full hover:bg-green-200 transition"
              >
                Dettagli →
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const stations = ref([])
const loading = ref(true)
const error = ref(null)
const router = useRouter()

// Simula AQI se API non fornisce
function generateRandomAQI() {
  return Math.floor(Math.random() * 200)
}

// Banda laterale colore
function getAirQualityColor(aqi) {
  if (aqi <= 50) return 'bg-green-400'
  if (aqi <= 100) return 'bg-yellow-400'
  if (aqi <= 150) return 'bg-orange-400'
  if (aqi > 150) return 'bg-red-500'
  return 'bg-gray-300'
}

// Badge colorato per stato AQI
function getAQIBadge(aqi) {
  if (aqi <= 50) return 'bg-green-100 text-green-700'
  if (aqi <= 100) return 'bg-yellow-100 text-yellow-700'
  if (aqi <= 150) return 'bg-orange-100 text-orange-700'
  if (aqi > 150) return 'bg-red-100 text-red-700'
  return 'bg-gray-100 text-gray-700'
}

// Etichetta testo AQI
function getAirQualityLabel(aqi) {
  if (aqi <= 50) return 'Buona'
  if (aqi <= 100) return 'Moderata'
  if (aqi <= 150) return 'Scadente'
  if (aqi > 150) return 'Cattiva'
  return 'N/D'
}

onMounted(async () => {
  try {
    const res = await fetch('http://localhost:5000/api/stations')
    const data = await res.json()
    stations.value = data.map(station => ({
      ...station,
      aqi: generateRandomAQI(),
    }))
  } catch (err) {
    error.value = 'Errore nel caricamento delle stazioni.'
  } finally {
    loading.value = false
  }
})

function goToStation(id) {
  router.push(`/station/${id}`)
}
</script>



