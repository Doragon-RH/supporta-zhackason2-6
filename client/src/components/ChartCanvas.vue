<script setup lang="ts">
import { onMounted, ref } from "vue";
import Chart from "chart.js/auto";
import type { ChartOptions, ChartData, ChartDataset } from "chart.js";
import "chartjs-adapter-date-fns";

const tab = ref("貸し手");
const tabs = ["貸し手", "借り手"];

const chartCanvas = ref<HTMLCanvasElement | null>(null);

const img1 = new Image(20, 20);
img1.src = "src/assets/face01.png";
const img2 = new Image(10, 10);
img2.src = "src/assets/face02.png";
const img3 = new Image(30, 30);
img3.src = "src/assets/face03.png";
const img4 = new Image(50, 50);
img4.src = "src/assets/face04.png";
const img5 = new Image(40, 40);
img5.src = "src/assets/face05.png";

const renderChart = () => {
  if (chartCanvas.value) {
    const ctx = chartCanvas.value.getContext("2d");

    if (ctx) {
      const chartData: ChartData<"scatter", ChartDataset<"scatter">["data"]> = {
        datasets: [
          {
            data: [
              { x: new Date("2023-04-01").valueOf(), y: 20 },
              { x: new Date("2023-04-02").valueOf(), y: 10 },
              { x: new Date("2023-04-08").valueOf(), y: 30 },
              { x: new Date("2023-04-11").valueOf(), y: 50 },
              { x: new Date("2023-04-25").valueOf(), y: 40 },
            ],
            pointStyle: [img1, img2, img3, img4, img5],
            pointRadius: [20, 10, 30, 50, 40],
            backgroundColor: "rgba(255, 99, 132, 0.5)",
            borderColor: "rgba(255, 99, 132, 1)",
          },
        ],
      };

      const today = new Date();
      const dates = chartData.datasets[0].data.map((point) => point.x);
      const minDate = new Date(Math.min(...dates));
      const maxDate = new Date(Math.max(...dates));

      let min, max;

      let diffDate;

      if (
        Math.abs(today.getTime() - minDate.getTime()) >
        Math.abs(today.getTime() - maxDate.getTime())
      ) {
        diffDate = minDate;
      } else {
        diffDate = maxDate;
      }
      if (diffDate < today) {
        min = diffDate;
        max = new Date(
          today.getTime() + (today.getTime() - diffDate.getTime())
        );
      } else {
        min = new Date(
          today.getTime() - (diffDate.getTime() - today.getTime())
        );
        max = diffDate;
      }
      min.setDate(min.getDate() - 5);
      max.setDate(max.getDate() + 5);

      const chartOptions: ChartOptions<"scatter"> = {
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          x: {
            type: "time",
            time: {
              parser: "YYYY-MM-DD",
              unit: "day",
              tooltipFormat: "YYYY/MM/DD",
            },
            min: min.valueOf(),
            max: max.valueOf(),
            position: "bottom",
            ticks: {
              callback: (value) => {
                const date = new Date(value);
                const diffInDays = Math.round(
                  (date.getTime() - today.getTime()) / (1000 * 60 * 60 * 24)
                );
                if (diffInDays === 0) {
                  return "今日";
                } else if (diffInDays < 0) {
                  return Math.abs(diffInDays) + "日前";
                } else {
                  return diffInDays + "日後";
                }
              },
              autoSkip: true,
              autoSkipPadding: 30,
              crossAlign: "near",
              includeBounds: true,
              maxRotation: 0,
              minRotation: 0,
              padding: 10,
              display: true,
              maxTicksLimit: 20,
            },
          },
          y: {
            type: "linear",
            position: "center",
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
  <v-tabs v-model="tab" color="pink-accent-4" align-tabs="center">
    <v-tab
      v-for="t in tabs"
      :key="t"
      :value="t"
      style="padding-left: 50px; padding-right: 50px"
    >
      <p class="font-weight-bold text-h6">{{ t }}</p>
    </v-tab>
  </v-tabs>
  <div style="height: 15px" />
  <div class="total d-flex flex-row justify-end">
    <div class="font-weight-bold text-h5">合計金額 : ￥46,000</div>
  </div>
  <div style="height: 15px" />
  <div style="width: 90%">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>
<style>
.total {
  height: 70px;
  padding-right: 8%;
  text-decoration: underline;
}
</style>
