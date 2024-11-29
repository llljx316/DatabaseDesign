<template>
  <div class="dashboard-container">
    <div class="dashboard-text">用户名: {{ user.name }}</div>
    <div class="dashboard-text">权限: {{ user.roles }}</div>
    <div class="dashboard-text">角色: {{ type1 }}</div>
    <div ref="chart" style="width: 600px; height: 400px;"></div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
// import store from '@/store'
import { getShip } from '@/api/table'
import { getShipPointsEnd, getShipPoints } from '@/api/shippoints';
import { GetEditShips } from '@/api/editships';
import { GetEditShipPoints } from '@/api/editshippoints';
import { GetEvents } from '@/api/event';
import * as echarts from 'echarts'
// import { get } from 'core-js/core/dict';

export default {
  name: 'Dashboard',
  data() {
    return {
      user: this.$store.state.user,
      type1: '',
      count_ship: '',
      count_shippoints: '',
      count_shiproutes: '',
      count_editships: '',
      count_editshippoints: '',
      data:[]
    }
  },
  created() {
    this.fetchData()
  },
  // computed: {
  //   ...mapGetters([
  //     'user'
  //   ])
  // },
  mounted() {
    // this.getdata();
    // this.fetchData()
    // this.initChart();
    this.init_dash()
  },
  methods: {
    fetchData() {
      // store.dispatch('getInfo').then(response => {
      //   this.user = response.data
      // })
      this.user = this.$store.state.user
      // this.user.typevalue = this.user.typevalue === 1 ? '管理员' : this.user.typevalue === 2 ? '船员' : '数据分析师'
      this.type1 = this.user.typevalue === 1 ? '管理员' : this.user.typevalue === 2 ? '船员' : '数据分析师'
    },
    async init_dash() {
      await getShip().then(response => {
        const count = response.data.count
        this.data.push(count)
      })
      await getShipPoints().then(response => {
        const count = response.data.count
        this.data.push(count)
      })
      await getShipPointsEnd().then(response => {
        const count = response.data.count
        this.data.push(count)
      })
      await GetEditShips().then(response => {
        const count = response.data.count
        this.data.push(count)
      })
      await GetEditShipPoints().then(response => {
        const count = response.data.count
        this.data.push(count)
      })
      await GetEvents().then(response => {
        const count = response.data.count
        this.data.push(count)
      })


      // 所有数据获取完成后进行下一步操作
      this.initChart()
    },
    fetchData1(dataName) {
      return new Promise((resolve, reject) => {
        // 模拟异步获取数据
        setTimeout(() => {
          resolve(`${dataName}的数据`);
        }, 1000);
      });
    },
    initChart() {
      const chartContainer = this.$refs.chart
      const myChart = echarts.init(chartContainer)

      const data = this.data

      const option = {
        title: {
          text: '统计数据'
        },
        xAxis: {
          type: 'category',
          data: ['船只', '轨迹点', '轨迹', '船只编辑', '轨迹编辑', '事件']
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          type: 'bar',
          data: data,
          itemStyle: {
            color: function(params) {
              // 设置不同的颜色
              var colorList = [
                '#c23531', '#2f4554', '#61a0a8', '#d48265', '#91c7ae','#749f83'
              ];
              return colorList[params.dataIndex];
            }
          }
        }]
      };

      myChart.setOption(option);
    }
  }

}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
