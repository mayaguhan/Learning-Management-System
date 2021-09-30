<template>
  <button 
    class="btn m-1" 
    type="button" 
    @click="clicked = !clicked" 
    :class="[ { 'clicked': clicked} ]" >
    {{ genre.name }}
  </button>
</template>

<script>
export default {
  name: 'CustomButton',
  props: {
    genre: Object,
  },
  data: () => ({
    clicked: false,
  })
}
</script>

<style scoped>
.clicked{
  background-color: red;
}
</style>