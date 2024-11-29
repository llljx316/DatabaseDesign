<template>
  <div class="app-container">
    <el-input
      type="text"
      prefix-icon="el-icon-search"
      v-model="searchTextUser"
      placeholder="请输入用户名称"
      style="width: 270px; cursor: pointer"
      @enter="handleSearchUser"
    ></el-input>
    <el-button type="primary" icon="el-icon-search" @click="handleSearchUser">
    </el-button>

    <!-- <el-input
      type="text"
      prefix-icon="el-icon-search"
      v-model="searchTextShip"
      placeholder="请输入船只名称"
      style="width: 270px; cursor: pointer"
      @enter="handleSearchShip"
    ></el-input>
    <el-button type="primary" icon="el-icon-search" @click="handleSearchShip">
    </el-button> -->
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center"  label="编辑时间">
        <template slot-scope="scope">
          {{ scope.row.edittime }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="船只">
        <template slot-scope="scope">
          {{ scope.row.point.ship.name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="船只id">
        <template slot-scope="scope">
          {{ scope.row.point.ship.shipid }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="经度">
        <template slot-scope="scope">
          {{ scope.row.point.longtitude }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="纬度">
        <template slot-scope="scope">
          {{ scope.row.point.latitude }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="编辑用户">
        <template slot-scope="scope">
          {{ scope.row.user.username }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="职责">
        <template slot-scope="scope">
          {{ scope.row.user.typevalue }}
        </template>
      </el-table-column>

      <!-- <el-table-column class-name="status-col" label="Status" width="110" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status | statusFilter">{{ scope.row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column align="center" prop="created_at" label="Display_time" width="200">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.display_time }}</span>
        </template>
      </el-table-column> -->
    </el-table>
  </div>
</template>

<script>
// import { getShip, DeleteShip } from '@/api/table'
// import { ModifyShip, CreateShip, SearchShip } from '@/api/ship';

// import { GetEditShips, SearchEditShips } from '@/api/editships';
import { GetEditShipPoints, SearchEditShipPoints } from '@/api/editshippoints';

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'gray',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      list: null,
      listLoading: true,
      visible_edit: false,
      visible_create: false,
      searchTextUser: '',
      searchTextShip: '',
      // shipForm: {
      //   name: '',
      //   ship_type: '',
      //   capacity: '',
      //   length: '',
      //   width: '',
      //   height: '',
      //   draft: '',
      //   status: '',
      //   country: ''
      // },
      // ship_visible: [
      //   { key: 'name', label: '船只名称', prop: 'name', type: 'text' },
      //   { key: 'ship_type', label: '船只类型', prop: 'ship_type', type: 'text' },
      //   { key: 'capacity', label: '载重量', prop: 'capacity', type: 'number' },
      //   { key: 'length', label: '船只长度', prop: 'length', type: 'number' },
      //   { key: 'width', label: '船只宽度', prop: 'width', type: 'number' },
      //   { key: 'height', label: '船只高度', prop: 'height', type: 'number' },
      //   { key: 'draft', label: '船只吃水', prop: 'draft', type: 'number' },
      //   { key: 'status', label: '船只状态', prop: 'status', type: 'text' },
      //   { key: 'country', label: '船只所属国家', prop: 'country', type: 'text' }
      // ],
      nowid: ''
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    test(data) {
      console.log(data.row.shipid)
    },
    fetchData() {
      this.listLoading = true
      GetEditShipPoints().then(response => {
        this.list = response.data.results
        this.listLoading = false
      })
    },
    handleSearchUser() {
      SearchEditShipPoints(this.searchTextUser).then(res => {
        console.log(res)
        this.list = res.data.results
      })
    }
  }
}
</script>
