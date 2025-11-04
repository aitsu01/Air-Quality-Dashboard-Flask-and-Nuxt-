<template>
  <div class="p-6">
    <NuxtLink to="/" class="text-blue-600 underline mb-4 inline-block">← Torna alla lista</NuxtLink>

    <div v-if="loading">Caricamento dati stazione...</div>
    <div v-if="error" class="text-red-600">{{ error }}</div>

    <div v-if="station">
      <h1 class="text-2xl font-bold mb-2">{{ station.station.name }}</h1>
      <p class="text-gray-600 mb-4">{{ station.station.site }} — {{ station.station.address }}</p>

      <!-- Mostra le metriche -->
      <div v-for="(values, key) in station.metrics" :key="key" class="mb-8">
        <!-- Mostra solo gli array, non i campi *_weighted_avg -->
        <div v-if="Array.isArray(values)">
          <h2 class="font-semibold text-lg mb-2">{{ key.toUpperCase() }}</h2>

          <!-- Mostra la media ponderata -->
          <div v-if="station.metrics[key + '_weighted_avg']" class="mb-2">
            <span class="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm">
              Media ponderata (7 giorni): {{ station.metrics[key + '_weighted_avg'].toFixed(2) }}
            </span>
          </div>

          <!-- Tabella dati -->
          <table class="w-full text-sm border border-gray-200">
            <thead class="bg-gray-100">
              <tr>
                <th class="border px-2 py-1">Data</th>
                <th class="border px-2 py-1">Min</th>
                <th class="border px-2 py-1">Average</th>
                <th class="border px-2 py-1">Max</th>
                <th class="border px-2 py-1">Sample Size</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in values" :key="row.date">
                <td class="border px-2 py-1">{{ row.date }}</td>
                <td class="border px-2 py-1">{{ row.min }}</td>
                <td class="border px-2 py-1">{{ row.average }}</td>
                <td class="border px-2 py-1">{{ row.max }}</td>
                <td class="border px-2 py-1">{{ row.sample_size }}</td>
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
const station = ref(null)
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await fetch(`http://127.0.0.1:5000/api/stations/${route.params.id}`)
    const data = await res.json()

    if (data.error) throw new Error(data.error)
    station.value = data
  } catch (err) {
    error.value = 'Errore nel caricamento dei dati della stazione.'
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>

