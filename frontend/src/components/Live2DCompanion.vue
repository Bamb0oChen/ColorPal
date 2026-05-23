<script setup lang="ts">
defineProps<{
  accentColor: string
  mood?: 'idle' | 'happy'
}>()
</script>

<template>
  <div class="companion" :class="`is-${mood || 'idle'}`" :style="{ '--accent': accentColor }">
    <div class="halo" />
    <div class="avatar">
      <div class="hair hair-left" />
      <div class="hair hair-right" />
      <div class="face">
        <span class="eye eye-left" />
        <span class="eye eye-right" />
        <span class="mouth" />
      </div>
      <div class="body">
        <span class="gem" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.companion {
  position: relative;
  width: min(42vw, 260px);
  min-width: 188px;
  aspect-ratio: 1 / 1.24;
  display: grid;
  place-items: center;
  filter: drop-shadow(0 22px 34px color-mix(in srgb, var(--accent), transparent 68%));
}

.halo {
  position: absolute;
  width: 84%;
  aspect-ratio: 1;
  border-radius: 50%;
  background:
    radial-gradient(circle at 50% 50%, color-mix(in srgb, var(--accent), white 76%), transparent 63%),
    radial-gradient(circle at 70% 34%, #f7e4a2 0 9%, transparent 10%);
  opacity: 0.86;
}

.avatar {
  position: relative;
  width: 64%;
  height: 78%;
  animation: breathe 3.4s ease-in-out infinite;
}

.hair,
.face,
.body {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.hair {
  top: 9%;
  width: 45%;
  height: 31%;
  border-radius: 999px 999px 54px 54px;
  background: color-mix(in srgb, var(--accent), #111 16%);
  opacity: 0.92;
}

.hair-left {
  transform: translateX(-78%) rotate(-19deg);
}

.hair-right {
  transform: translateX(-22%) rotate(19deg);
}

.face {
  top: 20%;
  width: 74%;
  height: 36%;
  border-radius: 46% 46% 48% 48%;
  background: #fffaf6;
  box-shadow: inset 0 -12px 22px rgba(40, 35, 26, 0.05);
}

.eye {
  position: absolute;
  top: 45%;
  width: 10px;
  height: 14px;
  border-radius: 999px;
  background: #252525;
}

.eye-left {
  left: 30%;
}

.eye-right {
  right: 30%;
}

.mouth {
  position: absolute;
  left: 50%;
  bottom: 22%;
  width: 24px;
  height: 12px;
  border-bottom: 3px solid #252525;
  border-radius: 0 0 999px 999px;
  transform: translateX(-50%);
}

.body {
  bottom: 8%;
  width: 78%;
  height: 40%;
  border-radius: 42% 42% 34% 34%;
  background:
    linear-gradient(145deg, color-mix(in srgb, var(--accent), white 18%), var(--accent)),
    #e8f1ff;
}

.gem {
  position: absolute;
  left: 50%;
  top: 24%;
  width: 34px;
  height: 34px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.72);
  transform: translateX(-50%) rotate(45deg);
}

.is-happy .avatar {
  animation-duration: 2.5s;
}

@keyframes breathe {
  0%,
  100% {
    transform: translateY(0) scale(1);
  }

  50% {
    transform: translateY(-8px) scale(1.025);
  }
}
</style>
