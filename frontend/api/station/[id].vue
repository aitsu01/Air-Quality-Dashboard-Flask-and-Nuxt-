<template>
  <div class="p-8 max-w-6xl mx-auto">
    <!--  Pulsante torna indietro -->
    <button
      @click="$router.push('/')"
      class="text-blue-600 hover:text-blue-800 mb-6 font-medium"
    >
      ← Torna alla lista stazioni
    </button>

    <!-- Titolo e info -->
    <div v-if="stationData" class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">
        {{ stationData.name }}
      </h1>
      <p class="text-gray-500">
         {{ stationData.site }} – {{ stationData.address }}
      </p>
    </div>

    <!-- Loading / Error -->
    <div v-if="loading" class="text-center text-gray-600">Caricamento dati...</div>
    <div v-if="error" class="text-center text-red-600">{{ error }}</div>

    <!-- Se ci sono metriche -->
    <div v-if="stationData?.metrics" class="space-y-12">
      <!-- Loop su ogni metrica -->
      <div
        v-for="metric in stationData.metrics"
        :key="metric.name"
        class="border border-gray-200 rounded-2xl p-6 shadow-sm bg-white"
      >
        <!-- Titolo metrica -->
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-2xl font-semibold text-gray-800">
            {{ metric.name }} <span class="text-sm text-gray-500">({{ metric.unit_of_measurement }})</span>
          </h2>




          <!-- Box media ponderata -->
          <div
  class="px-4 py-2 rounded-full text-sm font-medium border"
  :class="weightedAverages[metric.name] !== null 
    ? 'bg-green-100 text-green-800 border-green-300' 
    : 'bg-gray-100 text-gray-400 border-gray-200 italic'"
>
  Media ponderata (7gg): 
  <span v-if="weightedAverages[metric.name] !== null">
    {{ weightedAverages[metric.name].toFixed(2) }}
  </span>
  <span v-else>n/d</span>
</div>





        <!-- Tabella dati -->
        <div class="overflow-x-auto">
          <table class="min-w-full text-sm border border-gray-200 rounded-lg">
            <thead class="bg-gray-100 text-gray-700">
              <tr>
                <th class="border p-2 text-left"> Giorno</th>
                <th class="border p-2 text-left">Min</th>
                <th class="border p-2 text-left">Media</th>
                <th class="border p-2 text-left">Max</th>
                <th class="border p-2 text-left">Campioni</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="day in metric.data_points"
                :key="day.date"
                class="hover:bg-gray-50 transition"
              >
                <td class="border p-2">{{ formatDate(day.date) }}</td>
                <td class="border p-2">{{ day.min.toFixed(2) }}</td>
                <td class="border p-2 font-semibold text-blue-600">
                  {{ day.average.toFixed(2) }}
                </td>
                <td class="border p-2">{{ day.max.toFixed(2) }}</td>
                <td class="border p-2 text-gray-500">{{ day.sample_size }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Descrizione -->
        <p v-if="metric.description" class="mt-3 text-sm text-gray-500" v-html="metric.description"></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const stationId = route.params.id

const stationData = ref(null)
const weightedAverages = ref({})
const loading = ref(true)
const error = ref(null)

//  Format date (YYYY-MM-DD → DD/MM/YYYY)
const formatDate = (date) => {
  const [y, m, d] = date.split('-')
  return `${d}/${m}/${y}`
}

onMounted(async () => {
  try {
    const res = await fetch(`http://localhost:5000/api/station/${stationId}`)
    const data = await res.json()

    if (data.error) throw new Error(data.error)
    stationData.value = data

    // Calcolo media ponderata (se il backend non la calcola già)
    const avg = {}
    for (const metric of data.metrics) {
      const valid = metric.data_points
        .slice(-7)
        .filter((v) => v.sample_size > 0)
      if (valid.length) {
        const total = valid.reduce((a, v) => a + v.average * v.sample_size, 0)
        const weight = valid.reduce((a, v) => a + v.sample_size, 0)
        avg[metric.name] = total / weight
      }
    }
    weightedAverages.value = avg
  } catch (err) {
    error.value = 'Errore nel caricamento della stazione.'
  } finally {
    loading.value = false
  }
})
</script>
