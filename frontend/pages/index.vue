<template>




  <div class="min-h-screen bg-gray-50 py-10 px-4">



    <!-- Stato caricamento -->
    <div v-if="loading" class="text-center text-gray-500 mt-8 text-sm">
      Caricamento stazioni...
    </div>
    <div v-if="error" class="text-center text-red-600 mt-8 text-sm">
      {{ error }}
    </div>



  <!-- HERO SECTION -->
<section 
  class="text-center mb-10 opacity-0 translate-y-6 animate-fade-in-up"
>
  <h1 class="text-3xl font-bold text-green-700 mb-2 tracking-tight">
    Air Quality Monitoring Dashboard
  </h1>

  <p class="text-gray-600 max-w-2xl mx-auto text-sm sm:text-base">

    Dashboard interattiva per l’analisi della qualità dell’aria basata su dati ZeroC Green, con calcolo delle medie ponderate e indicatori ambientali aggiornati.

  </p>
</section>


    


    <!-- Tabella stazioni -->
     <div v-if="stations.length" class="max-w-6xl mx-auto bg-white shadow-lg rounded-xl overflow-hidden border border-gray-100">

  










  <!-- DESKTOP TABLE -->
<div class="hidden md:block">
  <table class="w-full text-sm text-left text-gray-700 border-collapse">
    <thead class="bg-gray-100 text-gray-700 text-xs uppercase tracking-wide border-b border-gray-200">
      <tr>
        <th class="px-5 py-3 text-left font-semibold">Stazione</th>
        <th class="px-5 py-3 text-left font-semibold">Sito</th>
        <th class="px-5 py-3 text-left font-semibold">Indirizzo</th>
        <th class="px-5 py-3 text-center font-semibold">Qualità aria</th>
        <th class="px-5 py-3 text-center font-semibold">Azioni</th>
      </tr>
    </thead>

    <tbody>
      <tr
        v-for="station in stations"
        :key="station.id"
        class="border-b hover:bg-gray-50 transition-colors duration-200 even:bg-gray-50"
      >
        <!-- Nome stazione + semaforo -->
         <td class="px-5 py-3 flex items-center gap-3 relative group">
  <!-- Semaforo con tooltip -->
  <div class="relative flex items-center justify-center">
    <span
      :class="[
        'w-3.5 h-3.5 rounded-full inline-block border border-gray-300 shadow-sm cursor-pointer transition-transform duration-150 group-hover:scale-110',
        getAirQualityColor(station.aqi)
      ]"
    ></span>

    <!-- Tooltip -->
    <div
      class="absolute bottom-6 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 bg-gray-800 text-white text-[11px] px-2 py-1 rounded whitespace-nowrap transition-opacity duration-300 shadow-md"
    >
      {{ getAirQualityLabel(station.aqi) }}
    </div>
  </div>

  <span class="font-semibold text-gray-900">{{ station.name }}</span>
</td>


        <!-- Sito -->
        <td class="px-5 py-3 text-gray-600">{{ station.site }}</td>

        <!-- Indirizzo -->
        <td class="px-5 py-3 text-gray-500 truncate max-w-[250px]">
          {{ station.address }}
        </td>

        <!-- Stato AQI -->
        <td class="px-5 py-3 text-center">
          <span
            class="px-2.5 py-1 rounded-full text-xs font-medium"
            :class="getAQIBadge(station.aqi)"
          >
            {{ getAirQualityLabel(station.aqi) }}
          </span>
        </td>

        <!-- Pulsante Dettagli -->
        <td class="px-5 py-3 text-center">
          <button
            @click="goToStation(station.id)"
            class="text-xs bg-gray-100 text-gray-700 px-3 py-1.5 rounded-full hover:bg-gray-200 hover:scale-105 transition-transform duration-150"
          >
            Dettagli →
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</div>


  <!-- END DESKTOP TABLE -->

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



