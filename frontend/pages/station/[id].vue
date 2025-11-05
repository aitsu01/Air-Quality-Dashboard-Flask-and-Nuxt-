<template>
  <div class="p-6">
    <button
      @click="$router.push('/')"
      class="text-blue-600 hover:underline mb-4 inline-block"
    >
      ← Torna alla lista
    </button>

    <div v-if="loading" class="text-center text-gray-600">Caricamento dati...</div>
    <div v-if="error" class="text-center text-red-600">{{ error }}</div>

    <div v-if="stationData" class="space-y-8">
      <div class="text-center">
        <h1 class="text-3xl font-bold">{{ stationData.name }}</h1>
        <p class="text-gray-600">{{ stationData.site }}</p>
        <p class="text-gray-500">{{ stationData.address }}</p>
      </div>

      <div
        v-for="metric in stationData.metrics"
        :key="metric.name"
        class="bg-white shadow rounded-2xl p-5 border border-gray-200"
      >
        <div class="flex justify-between items-center mb-2">
          <h2 class="text-xl font-semibold">{{ metric.name }}</h2>
          <span
            v-if="metric.weighted_avg"
            class="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm"
          >
            Media ponderata: {{ metric.weighted_avg.toFixed(2) }}
            {{ metric.unit_of_measurement }}
          </span>
        </div>

        <p class="text-gray-500 text-sm mb-3" v-html="metric.description"></p>

        <div class="overflow-x-auto">
          <table class="min-w-full border border-gray-300 rounded-lg text-sm">
            <thead class="bg-gray-100">
              <tr>
                <th class="border p-2">Data</th>
                <th class="border p-2">Min</th>
                <th class="border p-2">Media</th>
                <th class="border p-2">Max</th>
                <th class="border p-2">Sample Size</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(day, i) in metric.data_points"
                :key="i"
                class="hover:bg-gray-50"
              >
                <td class="border p-2">{{ day.date }}</td>
                <td class="border p-2">{{ day.min }}</td>
                <td class="border p-2">{{ day.average.toFixed(2) }}</td>
                <td class="border p-2">{{ day.max }}</td>
                <td class="border p-2">{{ day.sample_size }}</td>
              </tr>
            </tbody>
          </table>
        </div>
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
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await fetch(`http://localhost:5000/api/stations/${stationId}`)
    const data = await res.json()

    if (data.error) throw new Error(data.error)
    stationData.value = data
    console.log('Dati stazione:', data)
  } catch (err) {
    error.value = 'Errore nel caricamento della stazione.'
  } finally {
    loading.value = false
  }
})
</script>


