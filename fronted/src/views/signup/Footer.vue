<template>
  <div id="mychart" :style="{width: '500px', height: '500px'}">{{msg}}</div>
</template>
<script>

export default {
  name: 'Footer',
  data () {
    return {
      msg: '【这里是外部页面传入的消息】'
    }
  },
  mounted(){
    this.drawLine();

  },
  methods: {

  }
}
</script>
