<template>
  <div class="p-8 max-w-6xl mx-auto">
    <!-- 🔙 Pulsante torna indietro -->
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

    <!-- 📊 Selezione metrica + grafico -->
    <div v-if="stationData?.metrics" class="bg-white rounded-xl shadow-md p-6 mb-8">
      <label class="text-gray-700 text-sm font-medium mr-2">Seleziona metrica:</label>
      <select v-model="selectedMetric" class="border rounded-md p-2 text-sm">
        <option v-for="m in stationData.metrics" :key="m.name" :value="m.name">
          {{ m.name }}
        </option>
      </select>

      <!-- Grafico Chart.js -->
      <div v-if="chartData" class="mt-6">
        <Line :data="chartData" :options="chartOptions" />

        <!-- 🔹 Legenda AQI -->
<div class="mt-4 flex justify-center gap-4 text-sm">
  <div class="flex items-center gap-2">
    <span class="inline-block w-4 h-4 rounded-full bg-green-400"></span>
    <span>Buona</span>
  </div>
  <div class="flex items-center gap-2">
    <span class="inline-block w-4 h-4 rounded-full bg-yellow-400"></span>
    <span>Moderata</span>
  </div>
  <div class="flex items-center gap-2">
    <span class="inline-block w-4 h-4 rounded-full bg-orange-400"></span>
    <span>Scadente</span>
  </div>
  <div class="flex items-center gap-2">
    <span class="inline-block w-4 h-4 rounded-full bg-red-500"></span>
    <span>Cattiva</span>
  </div>
</div>

      </div>
    </div>

    <!-- Loading / Error -->
    <div v-if="loading" class="text-center text-gray-600">Caricamento dati...</div>
    <div v-if="error" class="text-center text-red-600">{{ error }}</div>

    <!-- Tabella dati -->
    <div v-if="stationData?.metrics" class="space-y-12">
      <div
        v-for="metric in stationData.metrics"
        :key="metric.name"
        class="border border-gray-200 rounded-2xl p-6 shadow-sm bg-white"
      >
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-2xl font-semibold text-gray-800">
            {{ metric.name }}
            <span class="text-sm text-gray-500">
              ({{ metric.unit_of_measurement }})
            </span>
          </h2>

          <div
            v-if="weightedAverages[metric.name]"
            class="bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-medium border border-green-300"
          >
            Media ponderata (7gg): {{ weightedAverages[metric.name].toFixed(2) }}
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="min-w-full text-sm border border-gray-200 rounded-lg">
            <thead class="bg-gray-100 text-gray-700">
              <tr>
                <th class="border p-2 text-left">Giorno</th>
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

        <p
          v-if="metric.description"
          class="mt-3 text-sm text-gray-500"
          v-html="metric.description"
        ></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale)

const route = useRoute()
const stationId = route.params.id

const stationData = ref(null)
const selectedMetric = ref(null)
const weightedAverages = ref({})
const loading = ref(true)
const error = ref(null)

const formatDate = (date) => {
  const [y, m, d] = date.split('-')
  return `${d}/${m}/${y}`
}

const chartData = computed(() => {
  const metric = stationData.value?.metrics.find(m => m.name === selectedMetric.value)
  if (!metric) return null

  return {
    labels: metric.data_points.slice(-10).map(d => formatDate(d.date)),
    datasets: [
      { label: 'Min', data: metric.data_points.map(d => d.min), borderColor: '#60a5fa', tension: 0.3 },
      { label: 'Media', data: metric.data_points.map(d => d.average), borderColor: '#22c55e', tension: 0.3 },
      { label: 'Max', data: metric.data_points.map(d => d.max), borderColor: '#f97316', tension: 0.3 }
    ]
  }
})

const chartOptions = {
  responsive: true,
  plugins: { legend: { position: 'bottom' } },
  scales: { y: { beginAtZero: true } }
}

onMounted(async () => {
  try {
    const res = await fetch(`http://localhost:5000/api/stations/${stationId}`)
    const data = await res.json()
    if (data.error) throw new Error(data.error)

    stationData.value = data
    selectedMetric.value = data.metrics[0]?.name

    const avg = {}
    for (const metric of data.metrics) {
      const valid = metric.data_points.slice(-7).filter(v => v.sample_size > 0)
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






