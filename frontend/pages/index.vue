<template>
  <div class="min-h-screen bg-gray-50 py-10 px-4">

 

    <!-- Header -->
    <header class="text-center mb-8">
      <h1 class="text-3xl font-bold text-green-700 mb-1">
         Dashboard qualità dell'aria
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
     <div v-if="stations.length" class="max-w-6xl mx-auto bg-white shadow-lg rounded-xl overflow-hidden border border-gray-100">

  <!-- DESKTOP TABLE -->
  <div class="hidden md:block">
    <table class="w-full text-sm text-left text-gray-700 border-collapse">
      <thead class="bg-gradient-to-r from-green-600 to-green-500 text-white text-xs uppercase tracking-wide">
        <tr>
          <th class="px-5 py-3 text-center w-2 rounded-tl-xl">#</th>
          <th class="px-5 py-3">Nome</th>
          <th class="px-5 py-3">Sito</th>
          <th class="px-5 py-3">Indirizzo</th>
          <th class="px-5 py-3 text-center">Qualità aria</th>
          <th class="px-5 py-3 text-center rounded-tr-xl">Dettagli</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="station in stations"
          :key="station.id"
          class="border-b hover:bg-green-50 transition-colors duration-200 even:bg-gray-50"
        >
          <td :class="['w-2', getAirQualityColor(station.aqi)]"></td>
          <td class="px-5 py-3 font-semibold text-gray-900">{{ station.name }}</td>
          <td class="px-5 py-3 text-gray-600">{{ station.site }}</td>
          <td class="px-5 py-3 text-gray-500 truncate max-w-[220px]">{{ station.address }}</td>
          <td class="px-5 py-3 text-center">
            <span class="px-2.5 py-1 rounded-full text-xs font-medium" :class="getAQIBadge(station.aqi)">
              {{ getAirQualityLabel(station.aqi) }}
            </span>
          </td>
          <td class="px-5 py-3 text-center">
            <button
              @click="goToStation(station.id)"
              class="text-xs bg-green-100 text-green-700 px-3 py-1.5 rounded-full hover:bg-green-200 hover:scale-105 transition-transform duration-150"
            >
              Dettagli →
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- MOBILE CARD LIST -->
  <div class="md:hidden divide-y divide-gray-200">
    <div
      v-for="station in stations"
      :key="station.id"
      class="p-4 flex flex-col gap-2 hover:bg-green-50 transition"
    >
      <!-- Header -->
      <div class="flex justify-between items-center">
        <h2 class="font-semibold text-gray-900 text-base">{{ station.name }}</h2>
        <span class="px-2 py-0.5 text-xs rounded-full font-medium" :class="getAQIBadge(station.aqi)">
          {{ getAirQualityLabel(station.aqi) }}
        </span>
      </div>

      <!-- Info -->
      <p class="text-sm text-gray-600">{{ station.site }}</p>
      <p class="text-xs text-gray-500">{{ station.address }}</p>

      <!-- Bottom action -->
      <div class="flex justify-between items-center mt-2">
        <div class="flex items-center gap-2 text-xs">
          <span :class="['inline-block w-2 h-2 rounded-full', getAirQualityColor(station.aqi)]"></span>
          <span class="text-gray-500">AQI: {{ station.aqi }}</span>
        </div>

        <button
          @click="goToStation(station.id)"
          class="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full hover:bg-green-200 transition"
        >
          Dettagli →
        </button>
      </div>
    </div>
  </div>
</div>


    <!--fine tabella stazioni-->




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



