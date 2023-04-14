<script setup lang="ts">
import { onMounted, ref } from "vue";
import Chart from "chart.js/auto";
import type { ChartOptions, ChartData, ChartDataSet } from "chart.js";

const chartCanvas = ref<HTMLCanvasElement | null>(null);

const renderChart = () => {
  if (chartCanvas.value) {
    const ctx = chartCanvas.value.getContext("2d");

    if (ctx) {
      const chartData: ChartData<"scatter", ChartDataSet<"scatter">["data"]> = {
        datasets: [
          {
            label: "Sample Scatter Dataset",
            data: [
              { x: 10, y: 20 },
              { x: 15, y: 10 },
              { x: 25, y: 30 },
              { x: 35, y: 50 },
              { x: 40, y: 40 },
            ],
            backgroundColor: "rgba(255, 99, 132, 0.5)",
            borderColor: "rgba(255, 99, 132, 1)",
          },
        ],
      };

      const chartOptions: ChartOptions<"scatter"> = {
        scales: {
          x: {
            type: "linear",
            position: "bottom",
          },
          y: {
            type: "linear",
            position: "left",
          },
        },
      };

      new Chart(ctx, {
        type: "scatter",
        data: chartData,
        options: chartOptions,
      });
    }
  }
};

onMounted(() => {
  renderChart();
});
</script>
<template>
  <canvas ref="chartCanvas"></canvas>
</template>
