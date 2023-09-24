<template>
  <div class="not-found-container">
    <div class="bubble-wrapper-left">
      <div class="bubble-wrapper-center">
        <div class="bubble-wrapper-right">
          <img src="@/assets/404.jpg" alt="404 Not Found" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: '404View'
}
</script>

<style scoped>
.not-found-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #E2FFED;
  overflow: hidden;
}

.not-found-container img {
  max-width: 90%;
  max-height: 80%;
}

/* Common Bubble Styles */
.bubble-wrapper-left::before, .bubble-wrapper-left::after,
.bubble-wrapper-center::before, .bubble-wrapper-center::after,
.bubble-wrapper-right::before, .bubble-wrapper-right::after {
  content: "";
  position: absolute;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: rgba(250, 250, 250, 0.7);  /* Off-white with transparency */
  border: 3px;
  animation: moveBubble 5s linear infinite;
  z-index: 1;
}

/* For Left Bubbles */
.bubble-wrapper-left::before {
  top: 0;
  left: 10%;
  animation-delay: 1s;
}
.bubble-wrapper-left::after {
  top: 0;
  left: 15%;
  animation-delay: 2.5s;
}

/* For Center Bubbles */
.bubble-wrapper-center::before {
  top: 0;
  left: 50%;
  animation-delay: 2s;
}
.bubble-wrapper-center::after {
  top: 0;
  left: 55%;
  animation-delay: 3.5s;
}

/* For Right Bubbles */
.bubble-wrapper-right::before {
  top: 0;
  left: 85%;
  animation-delay: 0.5s;
}
.bubble-wrapper-right::after {
  top: 0;
  left: 90%;
  animation-delay: 4s;
}

@keyframes moveBubble {
  0% {
    transform: translateY(0);
  }
  100% {
    transform: translateY(100vh);
  }
}
</style>
