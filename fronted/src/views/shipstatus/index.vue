<template>
  <div>
    <div ref="chartContainer" style="width: 1280px; height: 720px;"></div>
    <el-button type="primary" icon="el-icon-plus" @click="visible_add=true; getShipListFunc();"></el-button>
    <el-button type="warning" icon="el-icon-delete" @click="visible_del=true; searchEndList();"></el-button>

    <el-dialog title="创建" :visible.sync="visible_add">
      <el-form :model="shipForm" status-icon ref="shipForm" label-width="100px" class="demo-shipForm">
        <el-form-item v-for="field in ship_point_visible" :key="field.key" :label="field.label" :prop="field.prop">
          <el-input v-if="field.type === 'text'" type="text" v-model="shipForm[field.prop]" autocomplete="off"></el-input>
          <el-select  v-else-if="field.type === 'relation'" v-model="shipForm[field.prop]" placeholder="请选择要添加船只的路径">
            <el-option
              v-for="item in shiplist"
              :key="item.shipid"
              :label="item.name"
              :value="item.shipid">
            </el-option>
          </el-select>
          <el-select  v-else-if="field.type === 'shippoint'" v-model="shipForm[field.prop]" placeholder="请选择要添加船只的路径">
            <el-option
              v-for="item in pointlist"
              :key="item.value"
              :label="item.name"
              :value="item.value">
            </el-option>
          </el-select>
          <el-input v-else type="number" v-model="shipForm[field.prop]" autocomplete="off"  step="0.01"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="visible_add = false; resetForm('shipForm')">取 消</el-button>
        <el-button type="primary" @click="visible_add = false; CreateShipPointFunc('shipForm')">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="删除" :visible.sync="visible_del">
      <el-select v-model="del_id" placeholder="请选择要删除的路径">
        <el-option
          v-for="item in pointlist"
          :key="item.value"
          :label="item.name"
          :value="item.value">
        </el-option>
      </el-select>
      <el-button @click="visible_del = false; del_id=''">取 消</el-button>
      <el-button type="primary" @click="visible_add = false; comformdelete(del_id); del_id=''">确 定</el-button>

    </el-dialog>
  </div>

</template>

<script>
import * as echarts from 'echarts'
import world from '@/map/world.json'
import { getShipPoints, getShipRoutes, CreateShipPoint, getShipPointsEnd, DeleteShipPoint, getShipPointsEndSearch } from '@/api/shippoints'
import { getShip } from '@/api/table'
import Vue from 'vue'

export default {
  name: 'Chart',
  data() {
    return {
      list: '',
      listLoading: true,
      colorMap: {}, // 用于存储已分配的颜色.
      usedColors: new Set(),
      routelist: '',
      options: '',
      chart: '',
      visible_add: false,
      ship_point_visible: [
        { key: 'longtitude', label: '经度', prop: 'longtitude', type: 'number' },
        { key: 'latitude', label: '纬度', prop: 'latitude', type: 'number' },
        { key: 'ship', label: '船只', prop: 'ship', type: 'relation' },
        { key: 'next_node', label: '航迹', prop: 'next_node', type: 'shippoint' },
        { key: 'speed', label: '速度', prop: 'speed', type: 'number' },
        // { key: 'direction', label: '方向', prop: 'direction', type: 'text' }
      ],
      shipForm: {
        'longtitude': '',
        'latitude': '',
        'ship': '',
        'next_node': '',
        'speed': '',
        // 'direction': ''
      },
      shiplist: '',
      pointlist: '',
      visible_del: false,
      del_id: ''
    }
  },
  watch: {
    list: {
      handler(newvalue, oldvalue) {
        this.UpdateOption()
        this.UpdateChart()
      }
    },

    routelist: {
      handler(newvalue, oldvalue) {
        this.UpdateOption()
        this.UpdateChart()
      }
    },
    'shipForm.ship': {
      handler(newvalue, oldvalue) {
        // const ship = newvalue
        getShipPointsEndSearch(newvalue).then(res => {
          this.pointlist = res.data.results
          console.log(this.pointlist)
          this.pointlist = this.pointlist.map(item => {
            const point = {
              'value': item.id,
              'name': [item.longtitude, item.latitude]
            }
            return point
          })
          this.pointlist.push({ 'value': '', 'name': '新路线' })
          console.log(this.pointlist)
        })
      }
    }
  },
  // created() {
  //   this.fetchData()
  //   // this.getShipRoutes()
  // },
  mounted() {
    Vue.nextTick(() => {
      this.fetchData()
      // this.initChart()
    })
  },

  methods: {
    searchEndList(newvalue) {
      getShipPointsEnd().then(res => {
        this.pointlist = res.data.results
        console.log(this.pointlist)
        this.pointlist = this.pointlist.map(item => {
          const point = {
            'value': item.id,
            'name': [item.longtitude, item.latitude]
          }
          return point
        })
        // this.pointlist.push({ 'value': '', 'name': '新路线' })
        console.log(this.pointlist)
      })
    },
    getShipListFunc() {
      getShip().then(response => {
        this.shiplist = response.data.results
        // this.listLoading = false
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    fetchData() {
      this.listLoading = true
      getShipPoints().then(response => {
        this.list = response.data.results
        this.list = this.list.map(item => {
          const point = {
            'name': item.ship,
            'value': [item.longtitude, item.latitude]
          }
          return point
        })
        this.listLoading = false
        this.handleShipRoute()
      })
      this.searchEndList()
    },
    CreateShipPointFunc() {
      CreateShipPoint(this.shipForm).then(res => {
        console.log(res)
        // res1 = res
        if (res.status === 201) {
          // 判断是否创建其他的类型
          // console.log(this.shipForm.typevalue)
          this.fetchData()
          this.shipForm.ship = ''
          this.shipForm.point = ''

          // this.$message({
          //   message: '创建成功',
          //   type: 'success'
          // })
        } else {
          this.$message({
            message: '创建失败',
            type: 'error'
          })
          console.log('error submit!!')
          return false
        }
      }).catch(() => {
        this.$message({
          message: '创建失败',
          type: 'error'
        })
        console.log('error submit!!')
        return false
      })
    },
    comformdelete(data) {
      this.$confirm('此操作将永久删除该航迹点, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // console.log(this.list[1].shipid)
        const del_id = data
        DeleteShipPoint(del_id).then(response => {
          this.fetchData()
          this.$message({
            type: 'success',
            message: '删除成功!'
          })

        }).catch(() => {
          this.$message({
            type: 'warning',
            message: '删除失败!'
          })
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    pointProcess(item) {
      return {
        name: item.name,
        value: [item.value[0], item.value[1], 1] // 最后一个数字控制涟漪特效的大小
      }
    },
    handleShipRoute() {
      getShipRoutes().then(res => {
        this.routelist = []
        for (const route of res.data) {
          // const newroute = route.map(item => {
          //   const newitem = [item.longtitude, item.latitude]
          //   return newitem
          // })
          const newroute = []
          for (const r of route) {
            const nr = [r.longtitude, r.latitude]
            newroute.push(nr)
          }
          this.routelist.push({ 'coords': newroute })
        }
        this.initChart()
        // this.routelist = res.data.map(item => {
        //   const newitem = {
        //     coord: [item.longtitude, item.latitude],
        //     lineStyle: {
        //       width: 1,
        //       type: 'solid',
        //       color: '#3E3E3E'
        //     }
        //   }
        //   return newitem
        // })
      })
    },
    UpdateOption() {
      // const test = [
      //   {
      //     coords: [
      //       [55, 59],
      //       [50, 60]
      //     ]
      //   },
      //   {
      //     coords: [
      //       [2.6189462165178, 456.64349563895087],
      //       [124.10988522879458, 450.8570048730469],
      //       [123.9272226116071, 389.9520693708147]
      //     ]
      //   }
      // ]
      const nroutelist = JSON.parse(JSON.stringify(this.routelist))
      // console.log(test)
      console.log(this.routelist)
      console.log(nroutelist)

      this.option = {
        tooltip: {
          trigger: 'item',
          formatter: '{b}'
        },
        geo: {
          map: 'world',
          roam: true // 可以通过鼠标滚轮放大缩小地图
        },
        series: [{
          type: 'effectScatter',
          coordinateSystem: 'geo',
          data: this.list.map(point => ({
            name: point.name,
            value: point.value,
            itemStyle: {
              color: this.getColorByPointName(point.name)
            }
          })),
          symbolSize: 10, // 控制散点的大小
          label: {
            show: false // 不显示标点上的标签，避免重叠
          },
          emphasis: {
            itemStyle: {
              color: '#FF5733' // 鼠标悬停时的标点颜色
            }
          }
          // markline: {
          //   slient: false,
          //   symbol: 'none',
          //   data: this.routelist
          // }
        },
        {
          name: 'Route',
          type: 'lines',
          coordinateSystem: 'geo',
          geoIndex: 0,
          emphasis: {
            label: {
              show: false
            }
          },
          polyline: true,
          lineStyle: {
            color: '#black',
            width: 5,
            opacity: 1,
            type: 'dotted'
          },
          effect: {
            show: true,
            period: 8,
            color: '#a10000',
            constantSpeed: 80,
            trailLength: 0,
            symbolSize: [20, 12],
            symbol: 'triangle'
              // 'path://M10,60 L20,10 L40,10 L50,60 Z M20,60 L20,80 L40,80 L40,60 Z M25,10 L30,40 L35,10 Z M30,10 Q30,15 25,20 Q20,25 15,20 Q10,15 10,10'
            //   'path://M35.5 40.5c0-22.16 17.84-40 40-40s40 17.84 40 40c0 1.6939-.1042 3.3626-.3067 5H35.8067c-.2025-1.6374-.3067-3.3061-.3067-5zm90.9621-2.6663c-.62-1.4856-.9621-3.1182-.9621-4.8337 0-6.925 5.575-12.5 12.5-12.5s12.5 5.575 12.5 12.5a12.685 12.685 0 0 1-.1529 1.9691l.9537.5506-15.6454 27.0986-.1554-.0897V65.5h-28.7285c-7.318 9.1548-18.587 15-31.2715 15s-23.9535-5.8452-31.2715-15H15.5v-2.8059l-.0937.0437-8.8727-19.0274C2.912 41.5258.5 37.5549.5 33c0-6.925 5.575-12.5 12.5-12.5S25.5 26.075 25.5 33c0 .9035-.0949 1.784-.2753 2.6321L29.8262 45.5h92.2098z'
          },
          data: nroutelist
          // data: this.routelist
          // data:test
          // data: [
          //   {
          //     coords: [
          //       [55, 59],
          //       [50, 60]
          //     ]
          //   },
          //   {
          //     coords: [
          //       [2.6189462165178, 456.64349563895087],
          //       [124.10988522879458, 450.8570048730469],
          //       [123.9272226116071, 389.9520693708147]
          //     ]
          //   }
          // ]
        }]
      }
    },
    UpdateChart() {
      // const chartContainer = this.$refs.chartContainer
      // this.chart = echarts.init(chartContainer)
      // echarts.registerMap('world', world)
      this.UpdateOption()
      this.chart.setOption(this.option)
    },
    initChart() {
      const chartContainer = this.$refs.chartContainer
      this.chart = echarts.init(chartContainer)
      echarts.registerMap('world', world)
      // this.handleShipRoute()
      // const points = this.list

      // // 处理list
      // for (const result of this.list) {
      //   const point = {
      //     'name': result['ship'],
      //     'value': [result['longtitude'], result['latitude']]
      //   }
      //   points.push(point)
      // }

      // const option = {
      //   tooltip: {
      //     trigger: 'item',
      //     formatter: '{b}'
      //   },
      //   geo: {
      //     map: 'world',
      //     roam: true // 可以通过鼠标滚轮放大缩小地图
      //   },
      //   series: [{
      //     type: 'effectScatter',
      //     coordinateSystem: 'geo',
      //     data: points.map(point => ({
      //       name: point.name,
      //       value: point.value,
      //       itemStyle: {
      //         color: this.getColorByPointName(point.name)
      //       }
      //     })),
      //     symbolSize: 10, // 控制散点的大小
      //     label: {
      //       show: false // 不显示标点上的标签，避免重叠
      //     },
      //     emphasis: {
      //       itemStyle: {
      //         color: '#FF5733' // 鼠标悬停时的标点颜色
      //       }
      //     },
      //     markline: {
      //       slient: false,
      //       symbol: 'none',
      //       data: this.routelist
      //     }
      //   }]
      // }
      this.UpdateOption()
      this.chart.setOption(this.option)
      this.UpdateChart()
    },
    getColorByPointName(name) {
      if (this.colorMap[name]) {
        return this.colorMap[name];
      } else {
        let color;
        do {
          color = this.getRandomColor();
        } while (this.usedColors.has(color)); // 确保颜色不重复
        this.colorMap[name] = color;
        this.usedColors.add(color); // 添加到已使用的颜色集合
        return color;
      }
    },
    getRandomColor() {
      // 生成随机颜色
      return '#' + Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0');
    }
  }
}
</script>
