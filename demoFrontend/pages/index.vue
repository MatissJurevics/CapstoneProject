<template>
  <div class="h-[100vh] flex justify-start flex-col">
    <div class="relative h-[66vh] w-[100vw] overflow-hidden rounded-b-xl">
      <video
        class="w-full h-[66vh] object-cover bg-slate-600"
        ref="videoRef"
        autoplay
      ></video>
    </div>
    <select
      v-model="selectedDeviceId"
      placeholder="Select Camera"
      @change="startWebcam"
      class="select w-full max-w-xs mx-8 my-4"
    >
      <option disabled selected>Select Camera</option>
      <option
        :value="video.deviceId"
        v-for="video in videoStreams"
        :key="video.deviceId"
      >
        {{ video.label }}
      </option>
    </select>

    <div
      class="flex flex-row justify-between px-8 py-4 absolute bottom-0 w-full"
    >
      <button class="btn btn-primary" @click="startWebcam">Start Webcam</button>
      <button class="btn btn-secondary" @click="stopWebcam">Stop Webcam</button>
      <button class="btn btn-success" @click="sendStream">Send Stream</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";

const videoRef = ref(null);
const stream = ref(null);
const videoStreams = ref(null);
const selectedDeviceId = ref(null);

let socket

onMounted(async () => {
  console.log("mounting");
  let mediaDevices = (await navigator.mediaDevices.enumerateDevices()).filter(
    (el) => {
      return el.kind == "videoinput";
    }
  );
  videoStreams.value = mediaDevices;

  videoStreams.value.forEach((val) => {
    console.log(val);
  });
});

const startWebcam = async () => {
  try {
    if (selectedDeviceId) {
      stream.value = await navigator.mediaDevices.getUserMedia({
        video: { deviceId: { exact: selectedDeviceId.value } },
      });
    } else {
      stream.value = await navigator.mediaDevices.getUserMedia({ video: true });
    }

    if (videoRef.value) {
      videoRef.value.srcObject = stream.value;
    }
  } catch (error) {
    console.error("Error accessing webcam:", error);
  }
};

const sendStream = async () => {
  const serverUrl = "ws://localhost:8080";
  socket = new WebSocket(serverUrl);

  const mediaRecorder = new MediaRecorder(stream.value, {
    mimeType: "video/webm",
  });

  socket.onopen = () => {
    console.log("Connected to server");
    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        socket.send(event.data);
      }
    };
    mediaRecorder.start(1000); // Send chunks every 1000ms
  };

  socket.onclose = () => {
    console.log("WebSocket connection closed");
    mediaRecorder.stop();
  };

  socket.onerror = (error) => {
    console.error("WebSocket error:", error);
    mediaRecorder.stop();
  };
};

const stopWebcam = () => {
  if (stream.value) {
    if (socket) {
      socket.close();
    }
    const tracks = stream.value.getTracks();
    tracks.forEach((track) => track.stop());
    stream.value = null;
  }
};

// Cleanup on component unmount
onUnmounted(() => {
  stopWebcam();
});
</script>

<style scoped>
video {
  width: 100%;
  max-width: 600px;
  border: 1px solid #ccc;
}
</style>
