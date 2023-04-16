<script setup lang="ts">
import { onMounted, ref } from "vue";
import Chart from "chart.js/auto";
import type { ChartOptions, ChartData, ChartDataset } from "chart.js";
import "chartjs-adapter-date-fns";
import { createClient } from "@supabase/supabase-js";

const url = import.meta.env.VITE_SUPABASE_URL;
const key = import.meta.env.VITE_SUPABASE_KEY;
const supabase = createClient(url, key);

const transactions = ref([]);

const imgs = ref([]);
const coords = ref([]);
const sum_amount = ref(0);
const getLender = async () => {
  const data = await supabase
    .from("Transaction")
    .select()
    .eq("lender_id", sessionStorage.getItem("email"));

  transactions.value = data.data;
  for (const trans of transactions.value) {
    const userData = await supabase
      .from("User")
      .select("image_id, face_pattern")
      .eq("email", trans.borrower_id);

    const img_pattern = ref("");
    const diff = Math.ceil(
      (new Date(trans.limit_date) - new Date()) / (1000 + 60 * 60 * 24)
    );
    if (diff > 30000) {
      img_pattern.value = `pattern${userData.data[0].face_pattern}_lev1_path`;
    } else if (diff > 5000) {
      img_pattern.value = `pattern${userData.data[0].face_pattern}_lev2_path`;
    } else if (diff > -1000) {
      img_pattern.value = `pattern${userData.data[0].face_pattern}_lev3_path`;
    } else if (diff > -3000) {
      img_pattern.value = `pattern${userData.data[0].face_pattern}_lev4_path`;
    } else {
      img_pattern.value = `pattern${userData.data[0].face_pattern}_lev5_path`;
    }
    sum_amount.value = sum_amount.value + trans.amount;
    const pathData = await supabase
      .from("Image")
      .select(img_pattern.value)
      .eq("id", userData.data[0].image_id);
    const path = pathData.data[0][img_pattern.value];
    const url = supabase.storage.from("Images").getPublicUrl(path)
      .data.publicUrl;
    console.log(path, url);
    let size = trans.amount / 250;
    if (size < 20) {
      size = 20;
    } else if (size > 300) {
      size = 300;
    }
    const img = new Image(size, size);
    img.src = url;
    imgs.value.push(img);
    coords.value.push({
      x: new Date(trans.limit_date).valueOf(),
      y: trans.amount,
    });
  }
  console.log(imgs.value);
  console.log(coords.value);
  renderChart();
};

onMounted(() => {
  getLender();
});

const tab = ref("貸している相手");
const tabs = ["貸している相手", "借りている相手"];

const chartCanvas = ref<HTMLCanvasElement | null>(null);

const renderChart = () => {
  if (chartCanvas.value) {
    const ctx = chartCanvas.value.getContext("2d");

    if (ctx) {
      const chartData: ChartData<"scatter", ChartDataset<"scatter">["data"]> = {
        datasets: [
          {
            data: coords.value,
            pointStyle: imgs.value,
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
            ticks: {
              callback: (value) => {
                return "￥" + value.toString();
              },
            },
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
    <div class="font-weight-bold text-h5">合計金額 : ￥{{ sum_amount }}</div>
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
